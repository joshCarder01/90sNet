from typing import List, overload, Dict, Union
from Backend.Models import Models

from sqlalchemy import inspect

def find_id_in_json(json: List[dict], id: int) -> int:
    """
    @param json - Json to search through
    @param id - id of whatever is being searched to find
    @return offset - offset of said id in json list
    """

    for i in range(len(json)):
        print(f"Comparing json.id ({json[i]['id']}) == ({id}) input")
        if json[i]['id'] == id:
            return i

    raise KeyError(f"Couldn't find id: {id} in response json")

@overload
def assert_all_values(test1: Dict[str, any], test2: Models, match_columns = True) -> None: ...
@overload
def assert_all_values(test1: Models, test2: Models, match_columns = True) -> None: ...
@overload
def assert_all_values(test1: Models, test2: Dict[str, any], match_columns = True) -> None: ...

def assert_all_values(test1: Union[Models, Dict[str, any]], test2: Union[Models, Dict[str, any]], match_columns = True) -> None:

    tester = None
    model = None
    if isinstance(test1, Models) and isinstance(test2, Models):
        # Simple case, SQLAlchemy does nice things so can test equality
        assert test1 == test2
        return
    elif isinstance(test1, Models) and isinstance(test2, dict):
        model = test1
        tester = test2
    elif isinstance(test1, dict) and isinstance(test2, Models):
        tester = test1
        model = test2
    else:
        raise TypeError(f"[{assert_all_values.__name__}] Wrong types: <{type(test1)}> - <{type(test2)}>)")

    if match_columns:
        model.json_col_match(tester)

    # for i in test_col:
        # assert getattr(model, i) == tester[i], f"Failed on {i}: {tester[i]} == {getattr(model, i)}"
    
    model.json_comp(tester)
