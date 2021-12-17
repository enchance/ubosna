from typing import List, Dict

from app import ic


def flatten_query_result(key: str, query_result: List[dict], unique: bool = True) -> list:
    """
    Used for list of dict taken from db results. Get only the values of the key supplied.
    :param key:             Dict key ot extract.
    :param query_result:    List of values from the key specified
    :param unique:          Only return unique values
    :return:                list
    """
    flattened = [i[key] for i in query_result]
    if unique:
        return list(set(flattened))
    return flattened