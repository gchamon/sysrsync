from sysrsync.helpers import iterators
from nose.tools import eq_


def test_list_flatten():
    list_input = [1, [2, 3], [4]]
    expect = [1, 2, 3, 4]
    result = iterators.flatten(list_input)

    eq_(expect, result)


def test_tuple_flatten():
    tuple_input = (1, [2, 3], [4])
    expect = [1, 2, 3, 4]
    result = iterators.flatten(tuple_input)

    eq_(expect, result)


def test_tuples_and_lists_list_flatten():
    tuple_input = (1, (2, 3), [4])
    expect = [1, 2, 3, 4]
    result = iterators.flatten(tuple_input)

    eq_(expect, result)
