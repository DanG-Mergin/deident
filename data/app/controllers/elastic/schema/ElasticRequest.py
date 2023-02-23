import os
import sys
from pydantic import BaseModel, ValidationError, validator, root_validator, Extra
from typing import List, Dict, Union, Optional

# TODO: do I only need to append .. once?
# from ._Request import _Request
from ....schema.inbound import _Request
from ElasticEnums import ElasticTasks, ElasticIndexes, ElasticMethod


class ElasticsearchFilter(BaseModel):
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
    must: Union[List[dict], List["ElasticsearchFilter"]] = []
    should: Union[List[dict], List["ElasticsearchFilter"]] = []
    must_not: Union[List[dict], List["ElasticsearchFilter"]] = []

    @validator("must", "should", "must_not", pre=True)
    def unpack_nested_filters(cls, value):
        """
        Unpacks nested ElasticsearchFilter models to dicts.
        """
        if isinstance(value, list) and all(
            isinstance(item, ElasticsearchFilter) for item in value
        ):
            return [item.dict() for item in value]
        else:
            return value


class ElasticsearchQuery(BaseModel):
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
    filters: List[ElasticsearchFilter] = []
    sort_by: str = None
    page_size: int = 10
    page_number: int = 1


# class ElasticTypes(str, Enum):
#     label = "label"
#     substitution = "substitution"
class ElasticRequest(_Request, extra=Extra.ignore):
    method: str
    # url: str
    index: str
    task: str = ElasticTasks.deID.value
    # the elastic search document ID
    item_ids: Optional[List[str]] = None
    entity: str
    data: Optional[Dict[str, List[Dict]]] = None

    @property
    def url(this):
        query = this.query
        if this.item_ids is not None:
            # TODO: currently only handles one id
            return f"{os.environ['DATA_URL']}/elastic/{this.index}/{this.item_ids[0]}"
        if query is not None:
            return f"{os.environ['DATA_URL']}/elastic/{this.index}/{query}"
        return f"{os.environ['DATA_URL']}/elastic/{this.index}"

    @property
    def query(this):
        # TODO: add support for filters
        return None

    @validator("method")
    def map_method(cls, value):
        return ElasticMethod[value].value

    @validator("index")
    def map_index(cls, value):
        return ElasticIndexes[value].value

    @validator("task")
    def map_task(cls, value):
        return ElasticTasks[value].value

    @root_validator(pre=True)
    def consume_observable(cls, values):
        # _status = values.pop("status", None)
        # if _status and _status is not None:
        #     values["o_status"] = _status
        _data = values.pop("data", None)
        if _data and _data is not None:
            if "item_ids" in _data:
                values["item_ids"] = _data["item_ids"]

        _action = values.pop("o_action", None)
        if _action is not None:
            # values["action"] = _action
            # values["method"] = ElasticMethod[_action]
            values["method"] = _action

        _task = values.pop("task", None)
        if _task and _task is not None:
            values["task"] = _task

        _entity = values.pop("entity", None)
        if _entity and _entity is not None:
            values["entity"] = _entity
            values["index"] = _entity

        # _entityType = values.pop("entityType", None)
        # if _entityType and _entityType is not None:
        #     values["index"] = _entityType

        return values
