from __future__ import unicode_literals

import logging
import types

from django.conf import settings
from django.urls import resolve as django_resolve
from django.urls.base import get_script_prefix
from django.utils.datastructures import MultiValueDict
from django.utils.http import (
    urlencode as django_urlencode, urlquote as django_urlquote
)
from django.utils.six.moves import reduce as reduce_function, xmlrpc_client
from django.utils.translation import ugettext_lazy as _

import mayan
from mayan.apps.common.compat import dict_type, dictionary_type

from .exceptions import NotLatestVersion, UnknownLatestVersion
from .literals import DJANGO_SQLITE_BACKEND, MAYAN_PYPI_NAME, PYPI_URL

logger = logging.getLogger(__name__)


def check_for_sqlite():
    return settings.DATABASES['default']['ENGINE'] == DJANGO_SQLITE_BACKEND and settings.DEBUG is False


def check_version():
    pypi = xmlrpc_client.ServerProxy(PYPI_URL)
    versions = pypi.package_releases(MAYAN_PYPI_NAME)
    if not versions:
        raise UnknownLatestVersion
    else:
        if versions[0] != mayan.__version__:
            raise NotLatestVersion(upstream_version=versions[0])


def encapsulate(function):
    # Workaround Django ticket 15791
    # Changeset 16045
    # http://stackoverflow.com/questions/6861601/
    # cannot-resolve-callable-context-variable/6955045#6955045
    return lambda: function


def get_user_label_text(context):
    if not context['request'].user.is_authenticated:
        return _('Anonymous')
    else:
        return context['request'].user.get_full_name() or context['request'].user


def resolve(path, urlconf=None):
    path = '/{}'.format(path.replace(get_script_prefix(), '', 1))
    return django_resolve(path=path, urlconf=urlconf)


def return_attrib(obj, attrib, arguments=None):
    if isinstance(attrib, types.FunctionType):
        return attrib(obj)
    elif isinstance(
        obj, dict_type
    ) or isinstance(obj, dictionary_type):
        return obj[attrib]
    else:
        result = reduce_function(getattr, attrib.split('.'), obj)
        if isinstance(result, types.MethodType):
            if arguments:
                return result(**arguments)
            else:
                return result()
        else:
            return result


def return_related(instance, related_field):
    """
    This functions works in a similar method to return_attrib but is
    meant for related models. Support multiple levels of relationship
    using double underscore.
    """
    return reduce_function(getattr, related_field.split('__'), instance)


def urlquote(link=None, get=None):
    """
    This method does both: urlquote() and urlencode()

    urlqoute(): Quote special characters in 'link'

    urlencode(): Map dictionary to query string key=value&...

    HTML escaping is not done.

    Example:

    urlquote('/wiki/Python_(programming_language)')
        --> '/wiki/Python_%28programming_language%29'
    urlquote('/mypath/', {'key': 'value'})
        --> '/mypath/?key=value'
    urlquote('/mypath/', {'key': ['value1', 'value2']})
        --> '/mypath/?key=value1&key=value2'
    urlquote({'key': ['value1', 'value2']})
        --> 'key=value1&key=value2'
    """
    if get is None:
        get = []

    assert link or get
    if isinstance(link, dict):
        # urlqoute({'key': 'value', 'key2': 'value2'}) -->
        # key=value&key2=value2
        assert not get, get
        get = link
        link = ''
    assert isinstance(get, dict), 'wrong type "%s", dict required' % type(get)
    # assert not (link.startswith('http://') or link.startswith('https://')),
    #    'This method should only quote the url path.
    #    It should not start with http(s)://  (%s)' % (
    #    link)
    if get:
        # http://code.djangoproject.com/ticket/9089
        if isinstance(get, MultiValueDict):
            get = get.lists()
        if link:
            link = '%s?' % django_urlquote(link)
        return '%s%s' % (link, django_urlencode(get, doseq=True))
    else:
        return django_urlquote(link)
