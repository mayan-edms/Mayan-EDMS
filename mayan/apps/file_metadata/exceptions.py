
class FileMetadataError(Exception):
    """Base file metadata driver exception"""


class FileMetadataDriverError(FileMetadataError):
    """Exception raised when a driver encounters an unexpected error"""
