import sys
import unittest
import mock
import pylint_patcher.main

class Cli(unittest.TestCase):
    @mock.patch.object(pylint_patcher.patcher, "Patcher")
    @mock.patch.object(pylint_patcher.main.pylint.lint, "Run")
    def test_no_args(self, mock_run, mock_patcher):
        """
        If no arguments/options are provided, check that only pylint is
        called.
        """
        pylint_patcher.main.main([])
        mock_run.assert_called_with([])
        self.assertFalse(mock_patcher.called)

    @mock.patch.object(pylint_patcher.patcher, "Patcher")
    @mock.patch.object(pylint_patcher.main.pylint.lint, "Run")
    def test_help_option_is_passed_to_pylint(self, mock_run, mock_patcher):
        """
        If a single option is provided, check that only pylint is
        called.
        """
        pylint_patcher.main.main(["--help"])
        mock_run.assert_called_with(["--help"])
        self.assertFalse(mock_patcher.called)

    @mock.patch.object(pylint_patcher.patcher, "Patcher")
    @mock.patch.object(pylint_patcher.main.pylint.lint, "Run")
    def test_version_option_is_passed_to_pylint(self, mock_run, mock_patcher):
        """
        If the version option is specified, check that Pylint is called
        with sys.argv[0]="pylint"
        """
        self.assertNotEqual(sys.argv[0], "pylint")
        pylint_patcher.main.main(["--version"])
        mock_run.assert_called_with(["--version"])
        self.assertEqual(sys.argv[0], "pylint")
        self.assertFalse(mock_patcher.called)

    @mock.patch.object(pylint_patcher.patcher, "Patcher")
    @mock.patch.object(pylint_patcher.main.pylint.lint, "Run")
    def test_with_target(self, mock_run, mock_patcher):
        """
        If a target argument is provided, check that both patch and
        pylint are called.
        """
        pylint_patcher.main.main(["target", "--option"])
        mock_run.assert_called_with(["target", "--option"])
        mock_patcher.assert_called_with("target")

    @mock.patch.object(pylint_patcher.patcher, "Patcher")
    @mock.patch.object(pylint_patcher.main.pylint.lint, "Run")
    def test_with_target_and_keyword(self, mock_run, mock_patcher):
        """
        Check that keywords are passed on to pylint.
        """
        pylint_patcher.main.main(["target", "--option"], foo="bar")
        mock_run.assert_called_with(["target", "--option"], foo="bar")
        mock_patcher.assert_called_with("target")
