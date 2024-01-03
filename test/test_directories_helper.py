import unittest

from sysrsync.helpers import directories


class TestDirectoriesHelper(unittest.TestCase):
    """
    Unit tests for the directories helper module.
    """
    def test_strip_trailing_slash(self):
        """Test the strip_trailing_slash function."""
        test_dir = '/a/'
        expect = '/a'
        result = directories.strip_trailing_slash(test_dir)

        self.assertEqual(expect, result)

    def test_skip_strip_trailing_slash(self):
        """Test skipping strip_trailing_slash when not necessary."""
        test_dir = '/a'
        result = directories.strip_trailing_slash(test_dir)

        self.assertEqual(result, test_dir)

    def test_add_trailing_slash(self):
        """Test the add_trailing_slash function."""
        test_dir = '/a'
        expect = '/a/'
        result = directories.add_trailing_slash(test_dir)

        self.assertEqual(expect, result)

    def test_skip_add_trailing_slash(self):
        """Test skipping add_trailing_slash when not necessary."""
        test_dir = '/a/'
        result = directories.add_trailing_slash(test_dir)

        self.assertEqual(result, test_dir)

    def test_sanitize_trailing_slash(self):
        """Test sanitizing trailing slash when syncing source contents."""
        source, target = '/a', '/b/'
        expect_source, expect_target = '/a/', '/b'
        result_source, result_target = directories.sanitize_trailing_slash(
            source, target)

        self.assertEqual(expect_source, result_source)
        self.assertEqual(expect_target, result_target)

    def test_sanitize_trailing_slash_no_action_needed(self):
        """Test sanitizing trailing slash when syncing source contents when already sanitized."""
        source, target = '/a/', '/b'
        expect_source, expect_target = '/a/', '/b'
        result_source, result_target = directories.sanitize_trailing_slash(
            source, target)

        self.assertEqual(expect_source, result_source)
        self.assertEqual(expect_target, result_target)

    def test_sanitize_trailing_slash_whole_source(self):
        """Test sanitizing trailing slash when syncing whole source."""
        source, target = '/a/', '/b/'
        expect_source, expect_target = '/a', '/b'
        result_source, result_target = directories.sanitize_trailing_slash(
            source, target, sync_sourcedir_contents=False)

        self.assertEqual(expect_source, result_source)
        self.assertEqual(expect_target, result_target)

    def test_sanitize_trailing_slash_whole_source_no_action_needed(self):
        """Test sanitizing trailing slash when syncing whole source when already sanitized."""
        source, target = '/a', '/b/'
        expect_source, expect_target = '/a', '/b'
        result_source, result_target = directories.sanitize_trailing_slash(
            source, target, sync_sourcedir_contents=False)

        self.assertEqual(expect_source, result_source)
        self.assertEqual(expect_target, result_target)

    def test_dir_with_ssh(self):
        """Test composing string with ssh for rsync connection."""
        directory = '/a'
        ssh = 'host'
        expect = 'host:/a'
        result = directories.get_directory_with_ssh(directory, ssh)

        self.assertEqual(result, expect)

    def test_dir_without_ssh(self):
        """Test returning directory when ssh is None."""
        directory = '/a'
        ssh = None
        result = directories.get_directory_with_ssh(directory, ssh)

        self.assertEqual(result, directory)


if __name__ == '__main__':
    unittest.main()
