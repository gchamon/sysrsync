"""Generates the rsync command."""
import os
import os.path
from typing import Iterable, List, Optional

from sysrsync.exceptions import RemotesError
from sysrsync.helpers.directories import get_directory_with_ssh, sanitize_trailing_slash
from sysrsync.helpers.rsync import get_exclusions, get_rsh_command


def get_rsync_command(source: str,
                      destination: str,
                      source_ssh: Optional[str] = None,
                      destination_ssh: Optional[str] = None,
                      exclusions: Optional[Iterable[str]] = None,
                      sync_source_contents: bool = True,
                      options: Optional[Iterable[str]] = None,
                      private_key: Optional[str] = None,
                      rsh_port: Optional[int] = None,
                      strict_host_key_checking: Optional[bool] = None) -> List[str]:
    """Generate rsync command with the specified options for synchronizing files and directories.

    Args:
        source (str): The source directory or file path.
        destination (str): The destination directory or file path.
        source_ssh (Optional[str], optional): The SSH prefix for the source. Defaults
            to None.
        destination_ssh (Optional[str], optional): The SSH prefix for the destination.
            Defaults to None.
        exclusions (Optional[Iterable[str]], optional): The exclusions to be applied
            during synchronization. Defaults to None.
        sync_source_contents (bool, optional): Whether to sync the contents of the
            source directory. Defaults to True.
        options (Optional[Iterable[str]], optional): Additional rsync options. Defaults
            to None.
        private_key (Optional[str], optional): The path to the private key file for SSH
            authentication. Defaults to None.
        rsh_port (Optional[int], optional): The port number to use for the SSH
            connection. Defaults to None.
        strict_host_key_checking (Optional[bool], optional): Whether to perform strict
            host key checking. Defaults to None.

    Returns:
        List[str]: A list containing the rsync command and its options for
            synchronizing files and directories.
    """
    if source_ssh is not None and destination_ssh is not None:
        raise RemotesError()

    source = get_directory_with_ssh(source, source_ssh)
    destination = get_directory_with_ssh(destination, destination_ssh)

    # override sync_source_contents if local source is a file
    if (source_ssh is None) and os.path.isfile(source):
        sync_source_contents = False

    source, destination = sanitize_trailing_slash(source, destination, sync_source_contents)

    exclusions_options = (get_exclusions(exclusions)
                          if exclusions
                          else [])

    rsh = (get_rsh_command(private_key, rsh_port, strict_host_key_checking)
           if any((private_key, rsh_port, (strict_host_key_checking is not None)))
           else [])

    if options is None:
        options = []

    return ['rsync',
            *options,
            *rsh,
            source,
            destination,
            *exclusions_options]
