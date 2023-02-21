# For creating elasticsearch indexes.  Should only be run once if the volumes are working properly
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


async def init_indexes(es):
    return (
        await create_labels_index(es),
        await create_substitutions_index(es),
        await init_data(es),
    )

    # return asyncio.gather(
    #     [
    #         create_labels_index(es),
    #         create_substitutions_index(es),
    #         init_data(es),
    #     ]
    # )


# labels index mapping
async def create_labels_index(es):
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
                    "subCategory": {"type": "keyword"},
                    "tag": {"type": "text"},
                    "description": {"type": "text"},
                    "text": {"type": "text"},
                    "short_description": {"type": "text"},
                    "instructions": {"type": "text"},
                }
            }
        }

        return await es.indices.create(index="label", body=mapping)


async def create_substitutions_index(es):
    if not await es.indices.exists(index="substitution"):
        mapping = {
            "mappings": {
                "properties": {
                    "name": {"type": "keyword"},
                    "uuid": {"type": "keyword"},
                    "category": {"type": "keyword"},
                    "subCategory": {"type": "keyword"},
                    "items": {"type": "text"},
                }
            }
        }
        return await es.indices.create(index="substitution", body=mapping)


def get_index(name):
    # Get the absolute path of the directory containing the current file
    current_dir = Path(__file__).resolve().parent

    # Move up the directory tree to the ".data" directory
    data_dir = current_dir.parents[1]

    # Construct the path to the "labels.json" file
    file_path = data_dir / "assets" / "data" / "dictionaries" / f"{name}.json"

    # current_dir = Path(__file__).parent
    # file_path = current_dir.parent.joinpath("assets/data/dictionaries/", f"{name}.json")
    with open(file_path) as f:
        data = json.load(f)
    return data


async def init_data(es):
    # Check if any documents exist in the "substitution" index
    substitution_count = await es.count(index="substitution")
    if substitution_count["count"] == 0:
        # If no documents are found, initialize the index
        return await asyncio.gather(
            _create_labels(es),
            _create_contacts(es),
            _create_ids(es),
            _create_locations(es),
            _create_names(es),
            _create_professions(es),
        )
    else:
        # If documents exist, don't run initialization logic
        log.info("Data already initialized")


async def _create_labels(es):
    try:
        labels = get_index("labels")
        return await bulk_create_documents("label", labels, es)
        # for label in labels:
        #     create_document("label", label["uuid"], label, es)
    except Exception as e:
        log.error(e)


async def _create_ids(es):
    responses = []
    try:
        ids = get_index("ids")
        for id in ids:
            _res = await create_document("substitution", id["uuid"], id, es)
            responses.append(_res)
        return responses
    except Exception as e:
        log.error(e)


async def _create_contacts(es):
    responses = []
    try:
        contacts = get_index("contacts")
        for contact in contacts:
            _res = await create_document("substitution", contact["uuid"], contact, es)
            responses.append(_res)
        return responses
    except Exception as e:
        log.error(e)


async def _create_locations(es):
    responses = []
    try:
        locations = get_index("locations")
        for location in locations:
            _res = await create_document("substitution", location["uuid"], location, es)
            responses.append(_res)
        return responses
    except Exception as e:
        log.error(e)


async def _create_professions(es):
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


async def _create_names(es):
    responses = []
    try:
        names = get_index("names")
        for name in names:
            _res = await create_document("substitution", name["uuid"], name, es)
            responses.append(_res)
        return responses
    except Exception as e:
        log.error(e)
