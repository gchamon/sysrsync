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
           if any((private_key, rsh_port, strict_host_key_checking))
           else [])

    if options is None:
        options = []

    return ['rsync',
            *options,
            *rsh,
            source,
            destination,
            *exclusions_options]
