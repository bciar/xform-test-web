"""Tests for Xform Test Suite"""
import ntpath
import os
import unittest
from glob import glob

TEST_DIR = os.path.dirname(os.path.realpath(__file__)) + '/'
TEST_STATIC_DIR = TEST_DIR + 'static/'
PROJECT_ROOT_DIR = TEST_DIR + '../'


# TODO: I haven't actually finished these tests yet
# Need to emulate server or do unit tests on server upload function.
class SuperClass(unittest.TestCase):
    """Base class for running simple CLI tests."""

    @classmethod
    def files_dir(cls):
        """Return name of test class."""
        return TEST_STATIC_DIR + cls.__name__

    def input_path(self):
        """Return path of input file folder for test class."""
        return self.files_dir() + '/input/'

    def input_files(self):
        """Return paths of input files for test class."""
        all_files = glob(self.input_path() + '*')
        # With "sans_temps", you can have Excel files open while testing.
        sans_temps_and_dirs = [x for x in all_files if
                               not x[len(self.input_path()):].startswith('~$')
                               and not os.path.isdir(x)]
        return sans_temps_and_dirs

    @staticmethod
    def _dict_options_to_list(options):
        """Converts a dictionary of options to a list.

        Args:
            options (dict): Options in dictionary form, e.g. {
                'OPTION_NAME': 'VALUE',
                'OPTION_2_NAME': ...
            }

        Returns:
            list: A single list of strings of all options of the form
            ['--OPTION_NAME', 'VALUE', '--OPTION_NAME', ...]

        """
        new_options = []

        for k, v in options.items():
            new_options += ['--'+k, v]

        return new_options

    def standard_run(self, options=[]):
        """Runs CLI.

        Args:
            options (list): A single list of strings of all options of the form
            ['--OPTION_NAME', 'VALUE', '--OPTION_NAME', ...]

        Returns:
            1. str: Expected error message (empty string).
            2. str: Actual error message, if any.
        """
        msg = 'TestFailure: Error occurred while running test.\n\n' \
              'Details:\n{}'
        expected_err = ''
        in_files = self.input_files()

        try:
            # TODO
            pass
        except Exception as err_msg:
            err_msg = str(err_msg)
        if err_msg:
            self.assertEqual(expected_err, err_msg, msg.format(err_msg))

        return expected_err, err_msg

    def standard_run_test(self, options={}):
        """Checks CLI success.

        Args:
            options (dict): Options in dictionary form, e.g. {
                'OPTION_NAME': 'VALUE',
                'OPTION_2_NAME': ...
            }

        Side effects:
            assertEqual()
        """
        for file in self.input_files():  # temp until xform-test doesn't make
            if file.endswith('-modified.xml'):
                os.remove(file)

        options_list = SuperClass._dict_options_to_list(options)

        expected, actual = self.standard_run(options_list)
        self.assertEqual(expected, actual)

        for file in self.input_files():  # temp until xform-test doesn't make
            if file.endswith('-modified.xml'):
                os.remove(file)


class XFormsTest(SuperClass):
    """Augments SuperClass with methods for handling XForms and XLSForms."""

    @staticmethod
    def input_src_files(path):
        """Return paths of input files for test class.

        Args:
            path (str): Path to dir with input files.

        Returns:
            list: Of files.
        """
        all_files = glob(path + '*')
        # With "sans_temps", you can have Excel files open while testing.
        sans_temps_and_dirs = [x for x in all_files if
                               not x[len(path):].startswith('~$')
                               and not os.path.isdir(x)]
        return sans_temps_and_dirs

    def update_xml_files(self):
        """Update XML files."""
        path = self.input_path() + 'src/'
        for in_file in self.input_src_files(path):
            in_filename = ntpath.basename(in_file)
            out_filename = in_filename.replace('.xlsx', '.xml')
            out_file = in_file.replace(in_filename, '../'+out_filename)
            command = ['xls2xform', in_file, out_file]
            process = subprocess.Popen(command)
            process.wait()

    @staticmethod
    def delete_if_bad_extension(files, ok_extensions):
        """Remove files with bad extension

        Args:
            files (list): List of paths of files.
            ok_extensions (list): List of extensions that are ok to keep.

        Side Effects:
            Removes non-xml files from file system, not simply from an
            in-memory array of references to test files.
        """
        for file in files:
            if not any([file.endswith(x) for x in ok_extensions]):
                os.remove(file)

    def setUp(self):
        """setUp"""
        self.update_xml_files()
        XFormsTest.delete_if_bad_extension(files=self.input_files(),
                                           ok_extensions=['.xml'])


class MultipleFiles(XFormsTest):
    """Can run CLI on multiple files at once?"""

    def test_cli(self):
        """Simple smoke test to see that CLI runs without error."""
        super(XFormsTest, self).setUp()
        self.standard_run_test()


class MultipleTestCases(XFormsTest):
    """Can run CLI on multiple files at once?"""

    def test_cli(self):
        """Simple smoke test to see that CLI runs without error."""
        self.standard_run_test()


if __name__ == '__main__':
    unittest.main()
