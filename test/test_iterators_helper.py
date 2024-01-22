import unittest

from sysrsync.helpers import iterators


class TestIteratorsHelper(unittest.TestCase):
    def test_list_flatten(self) -> None:
        list_input = [1, [2, 3], [4]]
        expect = [1, 2, 3, 4]
        result = iterators.flatten(list_input)

        self.assertEqual(expect, result)

    def test_tuple_flatten(self) -> None:
        tuple_input = (1, [2, 3], [4])
        expect = [1, 2, 3, 4]
        result = iterators.flatten(tuple_input)

        self.assertEqual(expect, result)

    def test_tuples_and_lists_list_flatten(self) -> None:
        tuple_input = (1, (2, 3), [4])
        expect = [1, 2, 3, 4]
        result = iterators.flatten(tuple_input)

        self.assertEqual(expect, result)


if __name__ == '__main__':
    unittest.main()
