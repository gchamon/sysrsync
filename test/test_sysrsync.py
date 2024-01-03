import unittest
from tempfile import NamedTemporaryFile

from sysrsync import get_exclusions
from sysrsync.command_maker import get_rsync_command
from sysrsync.exceptions import RemotesError, PrivateKeyError


class TestPackage(unittest.TestCase):
    def test_get_exclusions(self) -> None:
        """should map list of exclusions to a list with each element following a --exclude statement"""
        exclusions = ['a', 'b']
        expect = ['--exclude', 'a', '--exclude', 'b']
        result = get_exclusions(exclusions)

        self.assertEqual(expect, result)

    def test_get_exclusions_already_in_rsync_format(self) -> None:
        """should ignore --exclude in exclusions"""
        exclusions = ['--exclude', 'a', '--exclude', 'b']
        expect = ['--exclude', 'a', '--exclude', 'b']
        result = get_exclusions(exclusions)

        self.assertEqual(expect, result)

    def test_simple_rsync_command(self) -> None:
        source = '/a'
        target = '/b'
        expect = 'rsync /a/ /b'.split()
        result = get_rsync_command(source, target)

        self.assertEqual(expect, result)

    def test_rsync_options(self) -> None:
        source = '/a'
        target = '/b'
        options = ['-a', '--verbose']
        expect = 'rsync -a --verbose /a/ /b'.split()
        result = get_rsync_command(source, target, options=options)

        self.assertEqual(expect, result)

    def test_simple_rsync_command_content_false(self) -> None:
        source = '/a'
        target = '/b'
        expect = 'rsync /a /b'.split()
        result = get_rsync_command(source, target, sync_source_contents=False)

        self.assertEqual(expect, result)

    def test_rsync_exclusions(self) -> None:
        source = '/a'
        target = '/b'
        exclusions = ['file1', 'file2']
        expect = 'rsync /a/ /b --exclude file1 --exclude file2'.split()
        result = get_rsync_command(source, target, exclusions=exclusions)

        self.assertEqual(expect, result)

    def test_rsync_exclusions_source_ssh(self) -> None:
        source = '/a'
        source_ssh = 'host1'
        target = '/b'
        exclusions = ['file1', 'file2']
        expect = 'rsync host1:/a/ /b --exclude file1 --exclude file2'.split()
        result = get_rsync_command(source, target, exclusions=exclusions, source_ssh=source_ssh)

        self.assertEqual(expect, result)

    def test_rsync_exclusions_target_ssh(self) -> None:
        source = '/a'
        target_ssh = 'host1'
        target = '/b'
        exclusions = ['file1', 'file2']
        expect = 'rsync /a/ host1:/b --exclude file1 --exclude file2'.split()
        result = get_rsync_command(source, target, exclusions=exclusions, destination_ssh=target_ssh)

        self.assertEqual(expect, result)

    def test_rsync_throws_both_remotes(self) -> None:
        """raises RemotesError when both source and destination are remotes"""
        source_ssh = 'host1'
        source = '/a'
        target_ssh = 'host2'
        target = '/b'
        with self.assertRaises(RemotesError):
            get_rsync_command(source, target, source_ssh=source_ssh, destination_ssh=target_ssh)

    def test_rsync_private_key(self) -> None:
        """test if correctly creates rsh option when passing a private key"""
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

    def test_rsync_private_key_missing(self) -> None:
        """test if get_rsync_command raises PrivateKeyError when key missing"""
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
