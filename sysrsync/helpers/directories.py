from typing import Tuple, Optional


def get_directory_with_ssh(directory: str, ssh: Optional[str]) -> str:
    """
    Returns the directory path with SSH prefix if SSH is provided.

    Args:
        directory (str): The directory path.
        ssh (Optional[str]): The SSH prefix. Defaults to None.

    Returns:
        str: The directory path with SSH prefix if SSH is provided, otherwise the
            directory path itself.
    """
    if ssh is None:
        return directory

    return f'{ssh}:{directory}'


def sanitize_trailing_slash(source_dir, target_dir, sync_sourcedir_contents=True):
    # type: (str, str, bool) -> Tuple[str, str]
    """
    Sanitizes the trailing slashes in the source and target directories.

    Args:
        source_dir (str): The source directory path.
        target_dir (str): The target directory path.
        sync_sourcedir_contents (bool, optional): Whether to sync the contents of the
            source directory. Defaults to True.

    Returns:
        Tuple[str, str]: A tuple containing the sanitized source directory path and the
            sanitized target directory path.
    """
    target_dir = strip_trailing_slash(target_dir)

    if sync_sourcedir_contents is True:
        source_dir = add_trailing_slash(source_dir)
    else:
        source_dir = strip_trailing_slash(source_dir)

    return source_dir, target_dir


def strip_trailing_slash(directory: str) -> str:
    """
    Strips the trailing slash from the directory path if it exists.

    Args:
        directory (str): The directory path.

    Returns:
        str: The directory path without the trailing slash, if present. Otherwise,
            returns the directory path as is.
    """

    return (directory[:-1]
            if directory.endswith('/')
            else directory)

def add_trailing_slash(directory: str) -> str:
    """
    Adds a trailing slash to the directory path if it doesn't already have one.

    Args:
        directory (str): The directory path.

    Returns:
        str: The directory path with a trailing slash, if it doesn't already have one.
            Otherwise, returns the directory path as is.
    """

    return (directory
            if directory.endswith('/')
            else f'{directory}/')
