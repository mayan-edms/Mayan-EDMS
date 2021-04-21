class GPGException(Exception):
    """
    Base app exception.
    """


class DecryptionError(GPGException):
    """
    Raised when an error occurs while trying to decrypt and encrypted file.
    """


class KeyFetchingError(GPGException):
    """
    Unable to receive key or key not found.
    """


class KeyDoesNotExist(GPGException):
    """
    Raised when attempting to decrypt or verify a file, and then key used to
    encrypt or sign the file is not found.
    """


class NeedPassphrase(GPGException):
    """
    A passphrase is needed but none was provided.
    """


class PassphraseError(GPGException):
    """
    Passphrase provided is incorrect.
    """


class VerificationError(GPGException):
    """
    Raised when a file is not signed.
    """
