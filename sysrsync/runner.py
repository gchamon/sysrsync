import os
import subprocess

from sysrsync.command_maker import get_rsync_command
from sysrsync.exceptions import RsyncError


def run(cwd=os.getcwd(), strict=True, verbose=False, **kwargs):
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
    if return_code != 0:
        raise RsyncError(f"[sysrsync runner] {action} exited with code {return_code}")
