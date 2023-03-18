import json, os
from uuid import uuid4
from pathlib import Path
from . import label as label_svc

# NOTE: for this to work you need to have the i2b2_2014 data
# in the secrets directory.  This is not included in the repo
# except as a submodule if you have permission to access it.
# if so then you will need to go to the private/i2b2 directory
# and run the run_spacy.sh script to generate the data.
async def get_i2b2(subdirectory: str = "train"):
    directory_path = f"{get_base_path()}/{subdirectory}"
    i2b2_docs = []
    # TODO: we may want to stream this, and will definitely want to do it in parallel
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):

            with open(os.path.join(directory_path, filename), "r") as json_file:
                _doc = json.load(json_file)
                _doc["annotations"] = await label_svc.get_labels_by_props(
                    _doc["annotations"]
                )
                _doc["uuid"] = str(uuid4())
                i2b2_docs.append(_doc)
    return i2b2_docs


def get_base_path():
    # Get the absolute path of the directory containing the current file
    current_dir = Path(__file__).resolve().parent
    # Move up the directory tree to the ".data" directory
    data_dir = current_dir.parents[1]
    return f"{data_dir}/app/assets/data/secret/i2b2_2014"