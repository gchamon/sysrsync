import os
from pathlib import Path
from typing import Iterable, List, Optional

from sysrsync.exceptions import PrivateKeyError
from sysrsync.helpers.iterators import flatten


def get_exclusions(exclusions: Iterable[str]) -> Iterable[str]:
    return flatten((('--exclude', exclusion)
                    for exclusion in exclusions
                    if exclusion != '--exclude'))


def get_rsh_command(private_key: Optional[str] = None, port: Optional[int] = None, strict_host_key_checking: Optional[bool] = None):

    args: List[str] = []

    if private_key is not None:
        expanded_key_file = os.path.expandvars(os.path.expanduser(private_key))

        if not Path(expanded_key_file).exists():
            raise PrivateKeyError(expanded_key_file)

        args.extend(["-i", expanded_key_file])

    if port is not None:
        args.extend(["-p", str(port)])

    if strict_host_key_checking is not None:
        args.extend(["-o", f'"StrictHostKeyChecking {"yes" if strict_host_key_checking else "no"}"'])

    string_args = " ".join(args)

    return ["--rsh", f"ssh {string_args}"]
