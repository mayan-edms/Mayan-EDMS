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
    """
    Unable to receive key or key not found
    """


class KeyDoesNotExist(GPGException):
    pass


class KeyImportError(GPGException):
    pass


class NeedPassphrase(GPGException):
    """
    Passphrase is needed but none was provided
    """


class PassphraseError(GPGException):
    """
    Passphrase provided is incorrect
    """
