from tempfile import TemporaryFile

from nose.tools import eq_, raises

from sysrsync import get_exclusions
from sysrsync.command_maker import get_rsync_command
from sysrsync.exceptions import RemotesError, PrivateKeyError


def test_get_exclusions():
    """should map list of exclusions to a list with each element following a --exclude statement"""
    exclusions = ['a', 'b']
    expect = ['--exclude', 'a', '--exclude', 'b']
    result = get_exclusions(exclusions)

    eq_(expect, result)


def test_get_exclusions_already_in_rsync_format():
    """should ignore --exclude in exclusions"""
    exclusions = ['--exclude', 'a', '--exclude', 'b']
    expect = ['--exclude', 'a', '--exclude', 'b']
    result = get_exclusions(exclusions)

    eq_(expect, result)


def test_simple_rsync_command():
    source = '/a'
    target = '/b'
    expect = 'rsync /a/ /b'.split()
    result = get_rsync_command(source, target)

    eq_(expect, result)


def test_rsync_options():
    source = '/a'
    target = '/b'
    options = ['-a', '--verbose']
    expect = 'rsync -a --verbose /a/ /b'.split()
    result = get_rsync_command(source, target, options=options)

    eq_(expect, result)


def test_simple_rsync_command_content_false():
    source = '/a'
    target = '/b'
    expect = 'rsync /a /b'.split()
    result = get_rsync_command(source, target, sync_source_contents=False)

    eq_(expect, result)


def test_rsync_exclusions():
    source = '/a'
    target = '/b'
    exclusions = ['file1', 'file2']
    expect = 'rsync /a/ /b --exclude file1 --exclude file2'.split()
    result = get_rsync_command(source, target, exclusions=exclusions)

    eq_(expect, result)


def test_rsync_exclusions_source_ssh():
    source = '/a'
    source_ssh = 'host1'
    target = '/b'
    exclusions = ['file1', 'file2']
    expect = 'rsync host1:/a/ /b --exclude file1 --exclude file2'.split()
    result = get_rsync_command(source, target, exclusions=exclusions, source_ssh=source_ssh)

    eq_(expect, result)


def test_rsync_exclusions_target_ssh():
    source = '/a'
    target_ssh = 'host1'
    target = '/b'
    exclusions = ['file1', 'file2']
    expect = 'rsync /a/ host1:/b --exclude file1 --exclude file2'.split()
    result = get_rsync_command(source, target, exclusions=exclusions, destination_ssh=target_ssh)

    eq_(expect, result)


@raises(RemotesError)
def test_rsync_throws_both_remotes():
    """raises RemotesError when both source and destination are remotes"""
    source_ssh = 'host1'
    source = '/a'
    target_ssh = 'host2'
    target = '/b'
    get_rsync_command(source, target, source_ssh=source_ssh, destination_ssh=target_ssh)


def test_rsync_private_key():
    """test if correctly creates rsh option when passing a private key"""
    with TemporaryFile() as temp_file:
        source_dir = '/home/user/files/'
        target_dir = '/home/server/files'
        destination_ssh = 'myserver'
        port = 2222
        strict_host_key_checking = False
        expect = ['rsync', f"--rsh='ssh -i {temp_file} -p {port} -o \"StrictHostKeyChecking no\"'", source_dir, f'{destination_ssh}:{target_dir}']
        actual = get_rsync_command(source=source_dir,
                                   destination=target_dir,
                                   destination_ssh=destination_ssh,
                                   private_key=temp_file,
                                   rsh_port=port,
                                   strict_host_key_checking=strict_host_key_checking)
        eq_(expect, actual)

@raises(PrivateKeyError)
def test_rsync_private_key():
    """test if get_rsync_command raises PrivateKeyError when key missing"""
    source_dir = '/home/user/files/'
    target_dir = '/home/server/files'
    destination_ssh = 'myserver'
    private_key = 'this_file_does_not_exist'
    actual = get_rsync_command(source=source_dir,
                               destination=target_dir,
                               destination_ssh=destination_ssh,
                               private_key=private_key)
