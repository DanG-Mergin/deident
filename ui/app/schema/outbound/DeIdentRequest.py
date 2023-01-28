import sys
sys.path.append("..")
from ._PostRequest import _PostRequest

class DeIdentRequest(_PostRequest):
    service_name = 'deident'
    # TODO: do this properly based on the request parameters and ENV variable
    url = "http://localhost:8083/deident/"

    
    