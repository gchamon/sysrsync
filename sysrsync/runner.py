"""Runs the rsync command with the specified options."""
import os
import subprocess

from sysrsync.command_maker import get_rsync_command
from sysrsync.exceptions import RsyncError


def run(cwd=os.getcwd(), strict=True, verbose=False, **kwargs):
    """Run the rsync command with the specified options.

    Args:
        cwd (str, optional): The current working directory. Defaults to the current
            directory.
        strict (bool, optional): Whether to raise an exception if the rsync command
            returns a non-zero exit code. Defaults to True.
        verbose (bool, optional): Whether to print the rsync command before executing
            it. Defaults to False.
        **kwargs: Additional options to be passed to the `get_rsync_command` function.

    Returns:
        subprocess.CompletedProcess: The completed process object representing the
            execution of the rsync command.
    """
    rsync_command = get_rsync_command(**kwargs)

    rsync_string = ' '.join(rsync_command)

    if verbose is True:
        print(f'[sysrsync runner] running command on "{cwd}":')
        print(rsync_string)
    process = subprocess.run(rsync_command, cwd=cwd, shell=False)

    if strict is True:
        code = process.returncode
        _check_return_code(code, rsync_string)

    return process


def _check_return_code(return_code: int, action: str):
    """Check the return code of an action and raises an exception if it is non-zero.

    Args:
        return_code (int): The return code of the action.
        action (str): The description of the action.

    Raises:
        RsyncError: If the return code is non-zero, an exception is raised with an
            error message indicating the action and the return code.
    """
    if return_code != 0:
        raise RsyncError(f"[sysrsync runner] {action} exited with code {return_code}")
