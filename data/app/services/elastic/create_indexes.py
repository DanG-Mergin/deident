# For creating elasticsearch indexes.  Should only be run once if the volumes are working properly

from .dependencies import get_elasticsearch_client
import json, logging, asyncio
from pathlib import Path
from .request import (
    create_document,
    bulk_create_documents,
    update_document,
    get_document,
    delete_document,
    search_documents,
)

log = logging.getLogger(__name__)
_es = get_elasticsearch_client()


async def init_indexes(es=_es):
    return (
        await create_labels_index(es),
        await create_substitutions_index(es),
        await create_corpus_index(es),
        await create_doc_index(es),
        await create_annotation_index(es),
        await init_data(es),
    )


# labels index mapping
async def create_labels_index(es=_es):
    if not await es.indices.exists(index="label"):
        mapping = {
            "mappings": {
                "properties": {
                    "uuid": {"type": "keyword"},
                    "kb_id": {"type": "keyword"},
                    "types": {"type": "keyword"},
                    "tasks": {"type": "keyword"},
                    "substitutionId": {"type": "keyword"},
                    "category": {"type": "keyword"},
                    "subcategory": {"type": "keyword"},
                    "tag": {"type": "text"},
                    "description": {"type": "text"},
                    "text": {"type": "text"},
                    "short_description": {"type": "text"},
                    "instructions": {"type": "text"},
                    "badgeName": {"type": "text"},
                    "icon": {"type": "text"},
                }
            }
        }

        return await es.indices.create(index="label", body=mapping)


async def create_substitutions_index(es=_es):
    if not await es.indices.exists(index="substitution"):
        mapping = {
            "mappings": {
                "properties": {
                    "name": {"type": "keyword"},
                    "uuid": {"type": "keyword"},
                    "category": {"type": "keyword"},
                    "subcategory": {"type": "keyword"},
                    "items": {"type": "text"},
                }
            }
        }
        return await es.indices.create(index="substitution", body=mapping)


async def create_corpus_index(es=_es):
    if not await es.indices.exists(index="corpus"):
        mapping = {
            "mappings": {
                "properties": {
                    "uuid": {"type": "keyword"},
                    "created_at": {"type": "date"},
                    "doc_types": {"type": "keyword"},
                    "tasks": {"type": "keyword"},
                    "patient_classes": {"type": "keyword"},
                    "doc_ids": {"type": "text"},
                }
            }
        }
        return await es.indices.create(index="corpus", body=mapping)


async def create_doc_index(es=_es):
    if not await es.indices.exists(index="doc"):
        mapping = {
            "mappings": {
                "properties": {
                    "uuid": {"type": "keyword"},
                    "title": {"type": "text"},
                    "doc_types": {"type": "keyword"},
                    "patient_classes": {"type": "keyword"},
                    "text": {"type": "text"},
                    "created_at": {"type": "date"},
                    "entities": {
                        "type": "nested",
                        "properties": {
                            "uuid": {"type": "keyword"},
                            "label_id": {"type": "keyword"},
                            # if there are two named entities in a document with the label "PERSON" and the same start and end character positions, spaCy will assign each entity a unique id value to distinguish between them
                            "id": {"type": "text"},
                            "start_index": {"type": "integer"},
                            "end_index": {"type": "integer"},
                        },
                    },
                    "tokens": {
                        "type": "nested",
                        "properties": {
                            # "label_id": {"type": "keyword"},
                            # ner is the BILUO label
                            # note that ATOW spacy only supports one entity label per span
                            # to use multiple labels the sentence/doc can be stored multiple times
                            # and used to train separate models built to identify each type
                            # ATOW using entities to represent BILUO so we can handle
                            # nested entities.  BILUO will be constructed as a view
                            # "ner": {"type": "keyword"},
                            # depencency label (e.g. nsubj, dobj, etc.)
                            # "dep": {"type": "keyword"},
                            # part of speech tag
                            # "tag": {"type": "keyword"},
                            # index of the token in the document
                            "index": {"type": "integer"},
                            "start_char": {"type": "integer"},
                            "end_char": {"type": "integer"},
                            # orth is the raw text
                            "orth": {"type": "text"},
                            "whitespace": {"type": "text"},
                        },
                    },
                },
            }
        }

        return await es.indices.create(index="doc", body=mapping)


async def create_annotation_index(es=_es):
    if not await es.indices.exists(index="annotation"):
        mapping = {
            "mappings": {
                "properties": {
                    "uuid": {"type": "keyword"},
                    "doc_id": {"type": "keyword"},
                    "author_id": {"type": "keyword"},
                    "timestamp": {"type": "date"},
                    "entities": {
                        "type": "nested",
                        "properties": {
                            "uuid": {"type": "keyword"},
                            "label_id": {"type": "keyword"},
                            # if there are two named entities in a document with the label "PERSON" and the same start and end character positions, spaCy will assign each entity a unique id value to distinguish between them
                            "id": {"type": "text"},
                            "start_index": {"type": "integer"},
                            "end_index": {"type": "integer"},
                        },
                    },
                },
            }
        }

        return await es.indices.create(index="annotation", body=mapping)


def get_index(name):
    # Get the absolute path of the directory containing the current file
    current_dir = Path(__file__).resolve().parent

    # Move up the directory tree to the ".data" directory
    data_dir = current_dir.parents[1]

    # Construct the path to the "labels.json" file
    file_path = data_dir / "assets" / "data" / "dictionaries" / f"{name}.json"

    with open(file_path) as f:
        data = json.load(f)
    return data


async def init_data(es=_es):
    labels_count = await es.count(index="label")
    if labels_count["count"] == 0:
        await _create_labels(es)
    # Check if any documents exist in the "substitution" index
    substitution_count = await es.count(index="substitution")
    if substitution_count["count"] == 0:
        # If no documents are found, initialize the index
        await asyncio.gather(
            _create_contacts(es),
            _create_ids(es),
            _create_locations(es),
            _create_names(es),
            _create_professions(es),
        )
    return None


async def _create_labels(es=_es):
    try:
        labels = get_index("labels")
        return await bulk_create_documents("label", labels, es)
    except Exception as e:
        log.error(e)


async def _create_ids(es=_es):
    responses = []
    try:
        ids = get_index("ids")
        for id in ids:
            _res = await create_document("substitution", id["uuid"], id, es)
            responses.append(_res)
        return responses
    except Exception as e:
        log.error(e)


async def _create_contacts(es=_es):
    responses = []
    try:
        contacts = get_index("contacts")
        for contact in contacts:
            _res = await create_document("substitution", contact["uuid"], contact, es)
            responses.append(_res)
        return responses
    except Exception as e:
        log.error(e)


async def _create_locations(es=_es):
    responses = []
    try:
        locations = get_index("locations")
        for location in locations:
            _res = await create_document("substitution", location["uuid"], location, es)
            responses.append(_res)
        return responses
    except Exception as e:
        log.error(e)


async def _create_professions(es=_es):
    responses = []
    try:
        professions = get_index("professions")
        for profession in professions:
            _res = await create_document(
                "substitution", profession["uuid"], profession, es
            )
            responses.append(_res)
        return responses
    except Exception as e:
        log.error(e)


async def _create_names(es=_es):
    responses = []
    try:
        names = get_index("names")
        for name in names:
            _res = await create_document("substitution", name["uuid"], name, es)
            responses.append(_res)
        return responses
    except Exception as e:
        log.error(e)
