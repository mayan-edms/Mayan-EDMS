from __future__ import unicode_literals


class DependenciesException(Exception):
    """
    Base exception for the dependencies app
    """


class NotLatestVersion(DependenciesException):
    """
    The installed version is not the latest available version
    """
    def __init__(self, upstream_version):
        self.upstream_version = upstream_version


class UnknownLatestVersion(DependenciesException):
    """
    It is not possible to determine what is the latest upstream version.
    """
