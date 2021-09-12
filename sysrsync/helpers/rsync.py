import os
from pathlib import Path
from typing import Iterable

from sysrsync.exceptions import PrivateKeyError
from sysrsync.helpers.iterators import flatten


def get_exclusions(exclusions: Iterable[str]) -> Iterable[str]:
    return flatten((('--exclude', exclusion)
                    for exclusion in exclusions
                    if exclusion != '--exclude'))


def get_rsh_command(private_key):
    expanded_key_file = os.path.expandvars(os.path.expanduser(private_key))
    if Path(expanded_key_file).exists():
        rsh = [f"--rsh='ssh -i {expanded_key_file}'"]
    else:
        raise PrivateKeyError(expanded_key_file)
    return rsh
