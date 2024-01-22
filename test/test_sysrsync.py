"""Unit tests for the sysrsync."""
import unittest
from tempfile import NamedTemporaryFile

from sysrsync.helpers.rsync import get_exclusions
from sysrsync.command_maker import get_rsync_command
from sysrsync.exceptions import RemotesError, PrivateKeyError


class TestPackage(unittest.TestCase):
    """Unit tests for the sysrsync package."""

    def test_get_exclusions(self):
        """Test the get_exclusions function."""
        exclusions = ['a', 'b']
        expect = ['--exclude', 'a', '--exclude', 'b']
        result = get_exclusions(exclusions)

        self.assertEqual(expect, result)

    def test_get_exclusions_already_in_rsync_format(self):
        """Test ignoring --exclude in exclusions."""
        exclusions = ['--exclude', 'a', '--exclude', 'b']
        expect = ['--exclude', 'a', '--exclude', 'b']
        result = get_exclusions(exclusions)

        self.assertEqual(expect, result)

    def test_simple_rsync_command(self):
        """Test generating a simple rsync command."""
        source = '/a'
        target = '/b'
        expect = 'rsync /a/ /b'.split()
        result = get_rsync_command(source, target)

        self.assertEqual(expect, result)

    def test_rsync_options(self):
        """Test generating an rsync command with options."""
        source = '/a'
        target = '/b'
        options = ['-a', '--verbose']
        expect = 'rsync -a --verbose /a/ /b'.split()
        result = get_rsync_command(source, target, options=options)

        self.assertEqual(expect, result)

    def test_simple_rsync_command_content_false(self):
        """Test generating a simple rsync command with sync_source_contents set to False."""
        source = '/a'
        target = '/b'
        expect = 'rsync /a /b'.split()
        result = get_rsync_command(source, target, sync_source_contents=False)

        self.assertEqual(expect, result)

    def test_rsync_exclusions(self):
        """Test generating an rsync command with exclusions."""
        source = '/a'
        target = '/b'
        exclusions = ['file1', 'file2']
        expect = 'rsync /a/ /b --exclude file1 --exclude file2'.split()
        result = get_rsync_command(source, target, exclusions=exclusions)

        self.assertEqual(expect, result)

    def test_rsync_exclusions_source_ssh(self):
        """Test generating an rsync command with exclusions and source SSH."""
        source = '/a'
        source_ssh = 'host1'
        target = '/b'
        exclusions = ['file1', 'file2']
        expect = 'rsync host1:/a/ /b --exclude file1 --exclude file2'.split()
        result = get_rsync_command(source, target, exclusions=exclusions, source_ssh=source_ssh)

        self.assertEqual(expect, result)

    def test_rsync_exclusions_target_ssh(self):
        """Test generating an rsync command with exclusions and destination SSH."""
        source = '/a'
        target_ssh = 'host1'
        target = '/b'
        exclusions = ['file1', 'file2']
        expect = 'rsync /a/ host1:/b --exclude file1 --exclude file2'.split()
        result = get_rsync_command(source, target, exclusions=exclusions, destination_ssh=target_ssh)

        self.assertEqual(expect, result)

    def test_rsync_throws_both_remotes(self):
        """Test raising RemotesError when both source and destination are remotes."""
        source_ssh = 'host1'
        source = '/a'
        target_ssh = 'host2'
        target = '/b'
        with self.assertRaises(RemotesError):
            get_rsync_command(source, target, source_ssh=source_ssh, destination_ssh=target_ssh)

    def test_rsync_private_key(self):
        """Test generating an rsync command with a private key."""
        with NamedTemporaryFile() as temp_file:
            source_dir = '/home/user/files/'
            target_dir = '/home/server/files'
            destination_ssh = 'myserver'
            temp_file_name = temp_file.name
            port = 2222
            strict_host_key_checking = False
            expect = ['rsync',
                      "--rsh",
                      f'ssh -i {temp_file_name} -p {port} -o "StrictHostKeyChecking no"',
                      source_dir,
                      f'{destination_ssh}:{target_dir}']
            actual = get_rsync_command(source=source_dir,
                                       destination=target_dir,
                                       destination_ssh=destination_ssh,
                                       private_key=temp_file_name,
                                       rsh_port=port,
                                       strict_host_key_checking=strict_host_key_checking)
            self.assertEqual(expect, actual)

    def test_rsync_private_key_missing(self):
        """Test raising PrivateKeyError when the private key file is missing."""
        source_dir = '/home/user/files/'
        target_dir = '/home/server/files'
        destination_ssh = 'myserver'
        private_key = 'this_file_does_not_exist'
        with self.assertRaises(PrivateKeyError):
            get_rsync_command(source=source_dir,
                              destination=target_dir,
                              destination_ssh=destination_ssh,
                              private_key=private_key)


if __name__ == '__main__':
    unittest.main()
