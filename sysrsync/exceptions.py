"""Exceptions for sysrsync."""
class RemotesError(Exception):
    """
    Exception raised when both the source and destination are remote.

    Attributes:
        message: The error message indicating that the source and destination cannot
            both be remote.
    """

    def __init__(self):
        """Initialize the RemotesError exception."""
        message = 'source and destination cannot both be remote'
        super().__init__(message)


class RsyncError(Exception):
    """Exception raised for errors related to rsync operations."""

    pass


class PrivateKeyError(Exception):
    """
    Exception raised when a private key file does not exist.

    Args:
        key_file: The path to the non-existent private key file.

    Attributes:
        message: The error message indicating that the private key file does not exist.
    """

    def __init__(self, key_file):
        """Initialize the PrivateKeyError exception."""
        message = f'Private Key File "{key_file}" does not exist'
        super().__init__(message)
