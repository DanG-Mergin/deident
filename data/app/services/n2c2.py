import json, os
from uuid import uuid4
from pathlib import Path
from . import label as label_svc


# async def get_n2c2(subdirectory: str, labels: list):
#     directory_path = f"{get_base_path()}/{subdirectory}"
async def get_n2c2(labels: list):
    if not isinstance(labels, list):
        labels = list(labels)
    n2c2_docs = []
    for label in labels:
        directory_path = f"{get_base_path()}/{label}"

        # TODO: we may want to stream this, and will definitely want to do it in parallel
        for filename in os.listdir(directory_path):
            if filename.endswith(".json"):
                with open(
                    os.path.join(directory_path, filename), "r", encoding="UTF-8"
                ) as json_file:
                    _doc = json.load(json_file)
                    _doc["entities"] = await label_svc.set_labels_by_props(
                        _doc["annotations"]
                    )
                    _doc.pop("annotations", None)
                    _doc["uuid"] = str(uuid4())
                    n2c2_docs.append(_doc)
    _res_obj = [{"docs": n2c2_docs, "uuid": str(uuid4())}]
    return _res_obj


def get_base_path():
    # Get the absolute path of the directory containing the current file
    current_dir = Path(__file__).resolve().parent
    # Move up the directory tree to the ".data" directory
    data_dir = current_dir.parents[1]
    return f"{data_dir}/app/assets/data/secret/n2c2_2018"
