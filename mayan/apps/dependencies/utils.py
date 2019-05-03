from __future__ import unicode_literals

from django.utils.six.moves import xmlrpc_client

import mayan

from .exceptions import NotLatestVersion, UnknownLatestVersion
from .literals import MAYAN_PYPI_NAME, PYPI_URL


def check_version():
    pypi = xmlrpc_client.ServerProxy(PYPI_URL)
    versions = pypi.package_releases(MAYAN_PYPI_NAME)
    if not versions:
        raise UnknownLatestVersion
    else:
        if versions[0] != mayan.__version__:
            raise NotLatestVersion(upstream_version=versions[0])
