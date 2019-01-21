import collections
from functools import reduce
from operator import iconcat
from typing import List, Any, Iterable


def flatten(input_iter: Iterable[Any]) -> List[Any]:
    list_of_lists = (element if isinstance(element, collections.Iterable)
                     else [element]
                     for element in input_iter)

    return reduce(iconcat, list_of_lists, [])
