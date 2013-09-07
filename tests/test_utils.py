import unittest
import os

from pylint_patcher import utils

class PatcherUtils(unittest.TestCase):
    def test_get_path_containing(self):
        """
        The get_path_containing function should return the directory
        containing the specified target.
        """
        input_path = os.path.join(os.getcwd(), "tests/data")
        # Target is a directory
        self.assertEqual(input_path, utils.get_path_containing("tests/data"));
        # Target is a file
        self.assertEqual(input_path, utils.get_path_containing("tests/data/dummy_module.py"));
        # Target is a module
        self.assertEqual(input_path, utils.get_path_containing("tests.data.dummy_module"));

