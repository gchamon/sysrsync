class RemotesError(Exception):
    def __init__(self) -> None:
        message = 'source and destination cannot both be remote'
        super().__init__(message)


class RsyncError(Exception):
    pass


class PrivateKeyError(Exception):
    def __init__(self, key_file: str) -> None:
        message = f'Private Key File "{key_file}" does not exist'
        super().__init__(message)
