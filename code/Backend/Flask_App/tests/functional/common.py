from typing import List
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
