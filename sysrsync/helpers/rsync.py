import os
from pathlib import Path
from typing import Iterable

from sysrsync.exceptions import PrivateKeyError
from sysrsync.helpers.iterators import flatten


def get_exclusions(exclusions: Iterable[str]) -> Iterable[str]:
    return flatten((('--exclude', exclusion)
                    for exclusion in exclusions
                    if exclusion != '--exclude'))


def get_rsh_command(private_key: str, port: int, strict_host_key_checking: bool):
    expanded_key_file = os.path.expandvars(os.path.expanduser(private_key))

    strict_host_key_checking_str: str = "yes" if strict_host_key_checking else "no"

    if not Path(expanded_key_file).exists():
        raise PrivateKeyError(expanded_key_file)

    return [f"--rsh='ssh -i {expanded_key_file} -p {str(port)} -o \"StrictHostKeyChecking {strict_host_key_checking_str}\"'"]
