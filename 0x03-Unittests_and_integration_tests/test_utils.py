print(__name__)

# Familiarize yourself with the utils.access_nested_map function and understand its purpose. Play with it in the Python console to make sure you understand.
# In this task you will write the first unit test for utils.access_nested_map.
# Create a TestAccessNestedMap class that inherits from unittest.TestCase.
# Implement the TestAccessNestedMap.test_access_nested_map method to test that the method returns what it is supposed to.
# Decorate the method with @parameterized.expand to test the function for following inputs:

import unittest
from parameterized import parameterized
from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)


# Implement TestAccessNestedMap.test_access_nested_map_exception. Use the assertRaises context manager to test that a KeyError is raised for the following inputs (use @parameterized.expand):
# nested_map={}, path=("a",)
# nested_map={"a": 1}, path=("a", "b")
# Also make sure that the exception message is as expected.

    @parameterized.expand([
        ({}, ("a",)),             # missing 'a'
        ({"a": 1}, ("a", "b")),   # missing 'b'
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises((KeyError,TypeError)) as error:
            access_nested_map(nested_map, path)

        # Verify the KeyError message (should match the missing key)
        self.assertEqual(str(error.exception), repr(path[-1]))