from typing import Iterable, List, Optional

from .exceptions import RemotesError
from .helpers.directories import (get_directory_with_ssh,
                                  sanitize_trailing_slash)
from .helpers.files import is_path_to_file
from .helpers.iterators import flatten


def get_rsync_command(source: str,
                      destination: str,
                      source_ssh: Optional[str] = None,
                      target_ssh: Optional[str] = None,
                      exclusions: Iterable[str] = [],
                      sync_source_contents: bool = True,
                      options: Iterable[str] = []) -> List[str]:
    if (source_ssh is not None and target_ssh is not None):
        raise RemotesError()

    source = get_directory_with_ssh(source, source_ssh)
    target = get_directory_with_ssh(destination, target_ssh)

    if is_path_to_file(source, (source_ssh is not None)):
        sync_source_contents = False

    source, destination = sanitize_trailing_slash(
        source, destination, sync_source_contents)

    exclusions = get_exclusions(exclusions)

    return ['rsync',
            *options,
            source,
            target,
            *exclusions]


def get_exclusions(exclusions: Iterable[str]) -> Iterable[str]:
    return flatten((('--exclude', exclusion) for exclusion in exclusions if exclusion != '--exclude'))
