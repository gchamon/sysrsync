from typing import Tuple, Optional


def get_directory_with_ssh(directory: str, ssh: Optional[str]) -> str:
    if ssh is None:
        return directory

    return f'{ssh}:{directory}'


def sanitize_trailing_slash(source_dir, target_dir, sync_sourcedir_contents=True):
    # type: (str, str, bool) -> Tuple[str, str]
    target_dir = strip_trailing_slash(target_dir)

    if sync_sourcedir_contents is True:
        source_dir = add_trailing_slash(source_dir)
    else:
        source_dir = strip_trailing_slash(source_dir)

    return source_dir, target_dir


def strip_trailing_slash(directory: str) -> str:
    return (directory[:-1]
            if directory.endswith('/')
            else directory)


def add_trailing_slash(directory: str) -> str:
    return (directory
            if directory.endswith('/')
            else f'{directory}/')
