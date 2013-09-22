import tempfile
import shutil
import unittest
import os

from pylint_patcher import differ, PATCHFILENAME
from tests.data import dummy_module

class Differ(unittest.TestCase):
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

    def test_cleanup(self):
        """Check that the cleanup function removes all temporary files"""
        diff = differ.Differ()
        self.assertTrue(os.path.exists(diff._temp_path))
        diff.cleanup()
        self.assertFalse(os.path.exists(diff._temp_path))

    def test_patchfile_is_applied_during_setup(self):
        """
        Check that an existing patchfile is applied during the
        setup routine.
        """
        diff = differ.Differ()
        try:
            diff.setup(self.test_file)
            # Move the existing patchfile to a backup
            patch_file_backup = os.path.join(self.temp_path, "backup.patch")
            os.rename(self.patch_file, patch_file_backup)
            # Run the diff and check that the new patchfile matches the old one
            diff.diff()
        finally:
            diff.cleanup()

        self.assertEqual(open(self.patch_file).read(),
                         open(patch_file_backup).read())

    def test_new_disable_pragma(self):
        """Check that new disable pragmas can be added."""
        diff = differ.Differ()
        try:
            diff.setup(self.test_file)
            diff.add_disable_pragma(self.test_file, 3, "Test123")
            diff.diff()
        finally:
            diff.cleanup()

        expected_file = os.path.join(self.temp_path,
                                     ".pylint-disable-twice.patch")
        self.assertEqual(open(self.patch_file).read(),
                         open(expected_file).read())

    def test_new_disable_pragma_on_same_line(self):
        """
        Check that new disable pragmas can be added to the same line
        as an existing pragma.
        """
        diff = differ.Differ()
        try:
            diff.setup(self.test_file)
            diff.add_disable_pragma(self.test_file, 8, "Test123")
            diff.diff()
        finally:
            diff.cleanup()

        expected_file = os.path.join(self.temp_path,
                                     ".pylint-disable-sameline.patch")
        self.assertEqual(open(self.patch_file).read(),
                         open(expected_file).read())

    def test_disable_pragma_with_invalid_path(self):
        """
        Check that an exception is raised if a disable pragma is
        inserted on a file outside of the target directory.
        """
        diff = differ.Differ()
        try:
            diff.setup(self.test_file)
            invalid_file = os.path.join(self.temp_path, os.pardir)
            with self.assertRaises(ValueError):
                diff.add_disable_pragma(invalid_file, 8, "Test123")
        finally:
            diff.cleanup()

