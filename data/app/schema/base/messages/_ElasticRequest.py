import os
from pydantic import BaseModel, ValidationError, validator, root_validator, Extra
from typing import List, Dict, Union, Optional

from ._Request import _Request
from ._MessageEnums import (
    ElasticTasks,
    ElasticIndexes,
    ElasticMethod,
)
from ._Data import _Data


class _ElasticsearchFilter(BaseModel):
    """
    A Pydantic model representing a filter to be applied to an Elasticsearch query.

    Attributes:
    -----------
    term : dict, optional
        A dictionary representing a "term" filter. The key is the name of the field to match on, and the value is the term to match.
    terms : dict, optional
        A dictionary representing a "terms" filter. The key is the name of the field to match on, and the value is a list of terms to match.
    range : dict, optional
        A dictionary representing a "range" filter. The key is the name of the field to match on, and the value is a dictionary representing the range of values to match.
    exists : dict, optional
        A dictionary representing an "exists" filter. The key is the name of the field to check for existence.
    missing : dict, optional
        A dictionary representing a "missing" filter. The key is the name of the field to check for absence.
    bool : dict, optional
        A dictionary representing a "bool" filter. The dictionary should include one or more sub-filters, each represented as a dictionary. See the Elasticsearch Query DSL documentation for details.
    must : List[dict], optional
        A list of filters to be combined with a "must" boolean operator. Each filter should be represented as a dictionary.
    should : List[dict], optional
        A list of filters to be combined with a "should" boolean operator. Each filter should be represented as a dictionary.
    must_not : List[dict], optional
        A list of filters to be combined with a "must_not" boolean operator. Each filter should be represented as a dictionary.
    """

    term: dict = None
    terms: dict = None
    range: dict = None
    exists: dict = None
    missing: dict = None
    bool: dict = None
    must: Union[List[dict], List["_ElasticsearchFilter"]] = []
    should: Union[List[dict], List["_ElasticsearchFilter"]] = []
    must_not: Union[List[dict], List["_ElasticsearchFilter"]] = []

    @validator("must", "should", "must_not", pre=True)
    def unpack_nested_filters(cls, value):
        """
        Unpacks nested _ElasticsearchFilter models to dicts.
        """
        if isinstance(value, list) and all(
            isinstance(item, _ElasticsearchFilter) for item in value
        ):
            return [item.dict() for item in value]
        else:
            return value


class _ElasticsearchQuery(BaseModel):
    """
    query to be executed against an Elasticsearch index.

    Attributes:
    -----------
    query : str
        A string representing the text to search for in the Elasticsearch index.
    filters : List[dict]
        A list of Elasticsearch filters to apply to the query. Each filter should be a dictionary that follows the format specified by the Elasticsearch Query DSL.
    sort_by : str, optional
        A string representing the field to sort the results by. If `None`, no sorting is applied.
    page_size : int, optional
        An integer representing the number of results to return per page. Default is 10.
    page_number : int, optional
        An integer representing the page number to retrieve. Default is 1.
    """

    query: str
    filters: List[_ElasticsearchFilter] = []
    sort_by: str = None
    page_size: int = 10
    page_number: int = 1

    # def dict(self, *args, **kwargs):
    #     """
    #     Overrides the default dict() method to unpack nested filters.
    #     """
    #     # json_out = super().dict(*args, **kwargs, exclude_none=True)
    #     json_out = {"query": {"match_all": {}}}
    #     # json_out['query']['match_all'] = [self.filters]

    #     # for f in self.filters:
    #     #     # json_out["query"]["bool"] = f.dict()
    #     #     if f.term is not None:
    #     #         json_out["query"]["match_all"]["bool"] = f.term
    #     #     elif f.terms is not None:
    #     return json_out


class _ElasticRequest(_Request, extra=Extra.ignore):
    index: str
    msg_task: str = ElasticTasks.deid.value
    msg_entity: str
    # query: Union[_ElasticsearchQuery, Dict, None] = None
    query: Optional[Dict] = None
    # data: Optional[Dict[str, List[Dict]]] = None

    @property
    def url(this):
        query = this.query
        if query is not None:
            return f"{this.base_url}/search/{this.index}"
        elif this.data.item_ids is not None:
            # TODO: currently only handles one id
            return (
                f"{os.environ['DATA_URL']}/elastic/{this.index}/{this.data.item_ids[0]}"
            )
        return f"{os.environ['DATA_URL']}/elastic/{this.index}"

    @validator("method")
    def map_method(cls, value):
        if value is not None:
            return ElasticMethod[value.lower()].value

    @validator("index")
    def map_index(cls, value):
        if value is not None:
            return ElasticIndexes[value.lower()].value

    @validator("msg_task")
    def map_task(cls, value):
        if value is not None:
            return ElasticTasks[value.lower()].value

    @root_validator(pre=True)
    def convert_fields(cls, values):
        _action = values.get("msg_action", None)
        if _action is not None:

            values["method"] = _action

        _entity = values.get("msg_entity", None)
        if _entity and _entity is not None:
            values["index"] = _entity

        return values
