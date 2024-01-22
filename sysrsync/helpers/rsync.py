"""Generates rsync arguments based on the provided options for sysrsync."""
import os
from pathlib import Path
from typing import Iterable, List, Optional

from sysrsync.exceptions import PrivateKeyError
from sysrsync.helpers.iterators import flatten


def get_exclusions(exclusions: Iterable[str]) -> Iterable[str]:
    """Generate a list of rsync exclusion arguments based on the provided exclusions.

    Args:
        exclusions (Iterable[str]): The exclusions to be used for generating the rsync
            exclusion arguments.

    Returns:
        Iterable[str]: A list of rsync exclusion arguments, where each exclusion is
            prefixed with '--exclude'.
    """
    return flatten((('--exclude', exclusion)
                    for exclusion in exclusions
                    if exclusion != '--exclude'))


def get_rsh_command(private_key: Optional[str] = None, port: Optional[int] = None, strict_host_key_checking: Optional[bool] = None):
    """Generate rsync remote shell (rsh) command with the specified options.

    Args:
        private_key (Optional[str], optional): The path to the private key file.
            Defaults to None.
        port (Optional[int], optional): The port number to use for the SSH connection.
            Defaults to None.
        strict_host_key_checking (Optional[bool], optional): Whether to perform strict
            host key checking. Defaults to None.

    Returns:
        List[str]: A list containing the rsync rsh command and its options.
    """
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
