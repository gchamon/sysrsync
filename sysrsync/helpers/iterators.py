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
    """
    Flattens an iterable by converting nested iterables into a single flat list.

    Args:
        input_iter (Iterable[Any]): The input iterable.

    Returns:
        List[Any]: A list containing all the elements from the input iterable, with
            nested iterables flattened.
    """

    return reduce(iconcat, list_of_lists, [])
