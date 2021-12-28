import collections

if 'Iterable' in dir(collections):
    from collections import Iterable
else:
    from collections.abc import Iterable

from functools import reduce
from operator import iconcat
from typing import List, Any, Iterable


def flatten(input_iter: Iterable[Any]) -> List[Any]:
    list_of_lists = (element if isinstance(element, Iterable)
                     else [element]
                     for element in input_iter)

    return reduce(iconcat, list_of_lists, [])
