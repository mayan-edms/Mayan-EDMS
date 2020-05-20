from django.utils.six.moves import xmlrpc_client
from django.utils.translation import ugettext_lazy as _

import mayan

from .exceptions import DependenciesException
from .literals import MAYAN_PYPI_NAME, PYPI_URL

MESSAGE_NOT_LATEST = '''The version you are using is outdated. The latest
version is %s'''
MESSAGE_UNKNOWN_VERSION = '''It is not possible to determine the latest
version available.'''
MESSAGE_UNEXPECTED_ERROR = '''Unexpected error trying to determine the
latest version available. Make sure your installation has a connection to
the internet; %s'''
MESSAGE_UP_TO_DATE = 'Your version is up-to-date.'


class PyPIClient(object):
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

    def check_version(self):
        versions = self.get_versions()
        if not versions:
            raise PyPIClient.UnknownLatestVersion
        else:
            if versions[0] != mayan.__version__:
                raise PyPIClient.NotLatestVersion(
                    upstream_version=versions[0]
                )

    def check_version_verbose(self):
        try:
            self.check_version()
        except PyPIClient.NotLatestVersion as exception:
            message = _(MESSAGE_NOT_LATEST) % exception.upstream_version
        except PyPIClient.UnknownLatestVersion:
            message = _(MESSAGE_UNKNOWN_VERSION)
        except Exception as exception:
            message = _(MESSAGE_UNEXPECTED_ERROR) % exception
        else:
            message = _(MESSAGE_UP_TO_DATE)

        return message

    def get_server_proxy(self):
        return xmlrpc_client.ServerProxy(PYPI_URL)

    def get_versions(self):
        server_proxy = self.get_server_proxy()
        return server_proxy.package_releases(MAYAN_PYPI_NAME)
