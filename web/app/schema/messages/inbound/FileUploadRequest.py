import os
import sys
from pydantic import ValidationError, validator, root_validator

sys.path.append("..")
from ._Request import _Request


class FileUploadRequest(_Request):
    type = "dictionary"  # TODO: store a reference to an actual class here
