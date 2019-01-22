class RemotesError(Exception):
    def __init__(self):
        message = 'source and destination cannot both be remote'
        super().__init__(message)


class RsyncError(Exception):
    pass
