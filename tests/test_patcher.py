import unittest
import os
import shutil
import tempfile

from pylint_patcher import PATCHFILENAME, patcher
from tests.data import dummy_module

class Patcher(unittest.TestCase):
    def setUp(self):
        """Copy test data to a temporary location"""
        data_path = os.path.dirname(dummy_module.__file__)
        self.temp_path = tempfile.mkdtemp(prefix="pylinttest_")
        os.rmdir(self.temp_path)
        shutil.copytree(data_path, self.temp_path)

        self.test_file = os.path.join(self.temp_path, "dummy_module.py")
        self.patch_file = os.path.join(self.temp_path, PATCHFILENAME)
        self.patched_file = os.path.join(self.temp_path, "dummy_module_patched.py")

    def tearDown(self):
        """Remove the temporary test data"""
        if os.path.exists(self.temp_path):
            shutil.rmtree(self.temp_path)

    def test_no_patchfile_returns_false(self):
        os.remove(self.patch_file)
        self.assertFalse(patcher.Patcher(self.test_file).patch())
        self.assertFalse(patcher.Patcher(self.patched_file).unpatch())

    def test_patcher(self):
        self.assertTrue(patcher.Patcher(self.test_file).patch())
        self.assertEqual(open(self.test_file).read(),
                         open(self.patched_file).read())

    def test_patcher_then_unpatcher(self):
        # Backup the test file for later comparison
        test_file_backup = os.path.join(self.temp_path, "backup.py")
        shutil.copy(self.test_file, test_file_backup)

        patch = patcher.Patcher(self.test_file)
        self.assertTrue(patch.patch())
        self.assertTrue(patch.unpatch())
        self.assertEqual(open(self.test_file).read(),
                         open(test_file_backup).read())
