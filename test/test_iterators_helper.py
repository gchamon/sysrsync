import unittest

from sysrsync.helpers import iterators


class TestIteratorsHelper(unittest.TestCase):
    """
    Unit tests for the iterators helper module.
    """
    def test_list_flatten(self):
        """Test the flatten function with a list input."""
        list_input = [1, [2, 3], [4]]
        expect = [1, 2, 3, 4]
        result = iterators.flatten(list_input)

        self.assertEqual(expect, result)

    def test_tuple_flatten(self):
        """Test the flatten function with a tuple input."""
        tuple_input = (1, [2, 3], [4])
        expect = [1, 2, 3, 4]
        result = iterators.flatten(tuple_input)

        self.assertEqual(expect, result)

    def test_tuples_and_lists_list_flatten(self):
        """Test the flatten function with a tuple input containing tuples and lists."""
        tuple_input = (1, (2, 3), [4])
        expect = [1, 2, 3, 4]
        result = iterators.flatten(tuple_input)

        self.assertEqual(expect, result)


if __name__ == '__main__':
    unittest.main()
