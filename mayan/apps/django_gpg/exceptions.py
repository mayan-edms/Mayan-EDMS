__all__ = (
    'GPGException', 'GPGVerificationError', 'GPGSigningError',
    'GPGDecryptionError', 'KeyDeleteError', 'KeyGenerationError',
    'KeyFetchingError', 'KeyDoesNotExist', 'KeyImportError'
)


class GPGException(Exception):
    pass


class GPGVerificationError(GPGException):
    pass


class GPGSigningError(GPGException):
    pass


class GPGDecryptionError(GPGException):
    pass


class KeyDeleteError(GPGException):
    pass


class KeyGenerationError(GPGException):
    pass


class KeyFetchingError(GPGException):
    pass


class KeyDoesNotExist(GPGException):
    pass


class KeyImportError(GPGException):
    pass
