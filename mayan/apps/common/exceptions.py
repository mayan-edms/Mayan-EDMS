from __future__ import unicode_literals


class BaseCommonException(Exception):
    """
    Base exception for the common app
    """
    pass


class NotLatestVersion(BaseCommonException):
    """
    The installed version is not the latest available version
    """
    def __init__(self, upstream_version):
        self.upstream_version = upstream_version


class UnknownLatestVersion(BaseCommonException):
    """
    It is not possible to determine what is the latest upstream version.
    """


class NPMException(BaseCommonException):
    """Base exception for the NPM registry client"""


class NPMPackgeIntegrityError(NPMException):
    """Hash mismatch exception"""
