import unittest

from sysrsync.helpers import directories


class TestDirectoriesHelper(unittest.TestCase):
    def test_strip_trailing_slash(self) -> None:
        """test strip trailing slash"""
        test_dir = '/a/'
        expect = '/a'
        result = directories.strip_trailing_slash(test_dir)

        self.assertEqual(expect, result)

    def test_skip_strip_trailing_slash(self) -> None:
        """test skip strip trailing slash when not necessary"""
        test_dir = '/a'
        result = directories.strip_trailing_slash(test_dir)

        self.assertEqual(result, test_dir)

    def test_add_trailing_slash(self) -> None:
        """test add trailing slash"""
        test_dir = '/a'
        expect = '/a/'
        result = directories.add_trailing_slash(test_dir)

        self.assertEqual(expect, result)

    def test_skip_add_trailing_slash(self) -> None:
        """test skip add trailing slash when not necessary"""
        test_dir = '/a/'
        result = directories.add_trailing_slash(test_dir)

        self.assertEqual(result, test_dir)

    def test_sanitize_trailing_slash(self) -> None:
        """test sanitize trailing slash when syncing source contents"""
        source, target = '/a', '/b/'
        expect_source, expect_target = '/a/', '/b'
        result_source, result_target = directories.sanitize_trailing_slash(
            source, target)

        self.assertEqual(expect_source, result_source)
        self.assertEqual(expect_target, result_target)

    def test_sanitize_trailing_slash_no_action_needed(self) -> None:
        """test sanitize trailing slash when syncing source contents when already sanitized"""
        source, target = '/a/', '/b'
        expect_source, expect_target = '/a/', '/b'
        result_source, result_target = directories.sanitize_trailing_slash(
            source, target)

        self.assertEqual(expect_source, result_source)
        self.assertEqual(expect_target, result_target)

    def test_sanitize_trailing_slash_whole_source(self) -> None:
        """test sanitize trailing slash when syncing whole source"""
        source, target = '/a/', '/b/'
        expect_source, expect_target = '/a', '/b'
        result_source, result_target = directories.sanitize_trailing_slash(
            source, target, sync_sourcedir_contents=False)

        self.assertEqual(expect_source, result_source)
        self.assertEqual(expect_target, result_target)

    def test_sanitize_trailing_slash_whole_source_no_action_needed(self) -> None:
        """test sanitize trailing slash when syncing whole source when already sanitized"""
        source, target = '/a', '/b/'
        expect_source, expect_target = '/a', '/b'
        result_source, result_target = directories.sanitize_trailing_slash(
            source, target, sync_sourcedir_contents=False)

        self.assertEqual(expect_source, result_source)
        self.assertEqual(expect_target, result_target)

    def test_dir_with_ssh(self) -> None:
        """should compose string with ssh for rsync connection"""
        directory = '/a'
        ssh = 'host'
        expect = 'host:/a'
        result = directories.get_directory_with_ssh(directory, ssh)

        self.assertEqual(result, expect)

    def test_dir_without_ssh(self) -> None:
        """should return directory when ssh is None"""
        directory = '/a'
        ssh = None
        result = directories.get_directory_with_ssh(directory, ssh)

        self.assertEqual(result, directory)


if __name__ == '__main__':
    unittest.main()
