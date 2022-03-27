"""
Utilities that may come in handy when using this library.
"""
from typing import Optional
from functools import singledispatch


@singledispatch
def optional_len(obj) -> Optional[int]:
    """
    Get an object's length (`len`) if it has one, `None` otherwise.

    Not strictly in the scope of this project but often comes in handy in
    situations where one would use it, so included here for convenience.
    """
    try:
        return len(obj)
    except TypeError:
        return None
