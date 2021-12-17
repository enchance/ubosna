from typing import Union, List, Optional, Any
from ast import literal_eval
from limeutils import Red

from app import settings as s, ic



# Redis
red = Red(**s.CACHE_CONFIG.get('default'))


def makesafe(val: Any) -> Union[str, int]:
    """
    Make data safe for redis.
    :param val: Item to make into a string
    :return:    str
    """
    if isinstance(val, (list, set, tuple, dict)):
        return repr(val)
    elif isinstance(val, bool):
        return int(val)
    else:
        return str(val)
    
def makesafe_dict(data: dict):
    """
    Make an entire dict safe for redis.
    :param data: dict to modify
    :return:
    """
    d = {}
    for k, v in data.items():
        d[k] = makesafe(v)
    return d

def prepareuser_dict(user_dict: dict, exclude: Optional[List[str]] = None) -> dict:
    """
    Prepare the dict before saving it to redis. Converts data to str or int.
    :param user_dict:   User data taken from user.to_dict()
    :param exclude:     Exclude from the final dict
    :return:            dict
    """
    d = {}
    exclude = exclude or []
    for k, v in user_dict.items():
        if k not in exclude:
            d[k] = makesafe(v)
    return d

def restoreuser_dict(user_dict: dict) -> dict:
    """
    Restores the user to its native python data types
    :param user_dict:   Dict from red.get()
    :return:            dict
    """
    d = user_dict.copy()
    for k, v in d.items():
        if k in ['groups', 'perms']:
            d[k] = literal_eval(d.get(k))
        elif k in ['is_active', 'is_superuser', 'is_verified']:
            d[k] = bool(d.get(k))
        elif k in ['options']:
            d[k] = dict(literal_eval(d.get(k)))
    return d