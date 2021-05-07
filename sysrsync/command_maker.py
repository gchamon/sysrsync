import os
from typing import Iterable, List, Optional

from .exceptions import RemotesError
from .helpers.directories import (get_directory_with_ssh,
                                  sanitize_trailing_slash)
from .helpers.iterators import flatten


def get_rsync_command(source: str,
                      destination: str,
                      source_ssh: Optional[str] = None,
                      destination_ssh: Optional[str] = None,
                      exclusions: Iterable[str] = [],
                      sync_source_contents: bool = True,
                      options: Iterable[str] = []) -> List[str]:
    if (source_ssh is not None and destination_ssh is not None):
        raise RemotesError()

    source = get_directory_with_ssh(source, source_ssh)
    destination = get_directory_with_ssh(destination, destination_ssh)

    # override sync_source_contents if local source is a file
    if (source_ssh is None) and os.path.isfile(source):
        sync_source_contents = False

    source, destination = sanitize_trailing_slash(
        source, destination, sync_source_contents)

    exclusions = get_exclusions(exclusions)

    return ['rsync',
            *options,
            source,
            destination,
            *exclusions]


def get_exclusions(exclusions: Iterable[str]) -> Iterable[str]:
    return flatten((('--exclude', exclusion) for exclusion in exclusions if exclusion != '--exclude'))
