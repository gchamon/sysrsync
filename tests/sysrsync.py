from sysrsync.command_maker import get_exclusions, get_rsync_command
from sysrsync.exceptions import RemotesError
from nose.tools import eq_, raises


def test_get_exclusions():
    "should map list of exclusions to a list with each element following a --exclude statement"
    exclusions = ['a', 'b']
    expect = ['--exclude', 'a', '--exclude', 'b']
    result = get_exclusions(exclusions)

    eq_(expect, result)


def test_get_exclusions_already_in_rsync_format():
    "should ignore --exclude in exclusions"
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
    "raises RemotesError when both source and destination are remotes"
    source_ssh = 'host1'
    source = '/a'
    target_ssh = 'host2'
    target = '/b'
    get_rsync_command(source, target, source_ssh=source_ssh, destination_ssh=target_ssh)
