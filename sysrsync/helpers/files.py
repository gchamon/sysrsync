import subprocess
import pipes
import os


def is_path_to_file(path, is_remote) -> bool:
    if is_remote is True:
        return exists_remote(path)

    return os.path.isfile(path)


def exists_remote(host_with_path):
    "Test if a file exists at path on a host accessible with SSH."
    host, path = host_with_path.split(':', 1)
    return subprocess.call(['ssh', host, 'test -f {}'.format(pipes.quote(path))]) == 0
