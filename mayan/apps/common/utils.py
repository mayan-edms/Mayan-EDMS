# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import os
import tempfile
import types

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils.datastructures import MultiValueDict
from django.utils.http import urlquote as django_urlquote
from django.utils.http import urlencode as django_urlencode
from django.utils.importlib import import_module
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)


def urlquote(link=None, get=None):
    """
    This method does both: urlquote() and urlencode()

    urlqoute(): Quote special characters in 'link'

    urlencode(): Map dictionary to query string key=value&...

    HTML escaping is not done.

    Example:

      urlquote('/wiki/Python_(programming_language)')     --> '/wiki/Python_%28programming_language%29'
      urlquote('/mypath/', {'key': 'value'})              --> '/mypath/?key=value'
      urlquote('/mypath/', {'key': ['value1', 'value2']}) --> '/mypath/?key=value1&key=value2'
      urlquote({'key': ['value1', 'value2']})             --> 'key=value1&key=value2'
    """
    if get is None:
        get = []

    assert link or get
    if isinstance(link, dict):
        # urlqoute({'key': 'value', 'key2': 'value2'}) --> key=value&key2=value2
        assert not get, get
        get = link
        link = ''
    assert isinstance(get, dict), 'wrong type "%s", dict required' % type(get)
    # assert not (link.startswith('http://') or link.startswith('https://')), \
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


def return_attrib(obj, attrib, arguments=None):
    try:
        if isinstance(attrib, types.FunctionType):
            return attrib(obj)
        elif isinstance(obj, types.DictType) or isinstance(obj, types.DictionaryType):
            return obj[attrib]
        else:
            result = reduce(getattr, attrib.split('.'), obj)
            if isinstance(result, types.MethodType):
                if arguments:
                    return result(**arguments)
                else:
                    return result()
            else:
                return result
    except Exception as exception:
        if settings.DEBUG:
            return 'Attribute error: %s; %s' % (attrib, exception)
        else:
            pass


# http://snippets.dzone.com/posts/show/5434
# http://snippets.dzone.com/user/jakob
def pretty_size(size, suffixes=None):
    suffixes = suffixes or [
        ('B', 1024L), ('K', 1048576L), ('M', 1073741824L),
        ('G', 1099511627776L), ('T', 1125899906842624L)
    ]

    for suf, lim in suffixes:
        if size > lim:
            continue
        else:
            try:
                return round(size / float(lim / 1024L), 2).__str__() + suf
            except ZeroDivisionError:
                return 0


def pretty_size_10(size):
    return pretty_size(
        size,
        suffixes=[
            ('B', 1000L), ('K', 1000000L), ('M', 1000000000L),
            ('G', 1000000000000L), ('T', 1000000000000000L)
        ])


def return_type(value):
    if isinstance(value, types.FunctionType):
        return value.__doc__ if value.__doc__ else _('Function found')
    elif isinstance(value, types.ClassType):
        return '%s.%s' % (value.__class__.__module__, value.__class__.__name__)
    elif isinstance(value, types.TypeType):
        return '%s.%s' % (value.__module__, value.__name__)
    elif isinstance(value, types.DictType) or isinstance(value, types.DictionaryType):
        return ', '.join(list(value))
    else:
        return value


# http://stackoverflow.com/questions/4248399/page-range-for-printing-algorithm
def parse_range(astr):
    result = set()
    for part in astr.split(','):
        x = part.split('-')
        result.update(range(int(x[0]), int(x[-1]) + 1))
    return sorted(result)


def generate_choices_w_labels(choices, display_object_type=True):
    results = []
    for choice in choices:
        ct = ContentType.objects.get_for_model(choice)
        label = unicode(choice)
        if isinstance(choice, User):
            label = choice.get_full_name() if choice.get_full_name() else choice

        if display_object_type:
            verbose_name = unicode(getattr(choice._meta, 'verbose_name', ct.name))
            results.append(('%s,%s' % (ct.model, choice.pk), '%s: %s' % (verbose_name, label)))
        else:
            results.append(('%s,%s' % (ct.model, choice.pk), '%s' % (label)))

    # Sort results by the label not the key value
    return sorted(results, key=lambda x: x[1])


def get_object_name(obj, display_object_type=True):
    ct_label = ContentType.objects.get_for_model(obj).name
    if isinstance(obj, User):
        label = obj.get_full_name() if obj.get_full_name() else obj
    else:
        label = unicode(obj)

    if display_object_type:
        try:
            verbose_name = unicode(obj._meta.verbose_name)
        except AttributeError:
            verbose_name = ct_label

        return '%s: %s' % (verbose_name, label)
    else:
        return '%s' % (label)


def validate_path(path):
    if not os.path.exists(path):
        # If doesn't exist try to create it
        try:
            os.mkdir(path)
        except Exception as exception:
            logger.debug('unhandled exception: %s', exception)
            return False

    # Check if it is writable
    try:
        fd, test_filepath = tempfile.mkstemp(dir=path)
        os.close(fd)
        os.unlink(test_filepath)
    except Exception as exception:
        logger.debug('unhandled exception: %s', exception)
        return False

    return True


def encapsulate(function):
    # Workaround Django ticket 15791
    # Changeset 16045
    # http://stackoverflow.com/questions/6861601/cannot-resolve-callable-context-variable/6955045#6955045
    return lambda: function


def get_descriptor(file_input, read=True):
    try:
        # Is it a file like object?
        file_input.seek(0)
    except AttributeError:
        # If not, try open it.
        if read:
            return open(file_input, 'rb')
        else:
            return open(file_input, 'wb')
    else:
        return file_input


# http://stackoverflow.com/questions/123198/how-do-i-copy-a-file-in-python
def copyfile(source, destination, buffer_size=1024 * 1024):
    """
    Copy a file from source to dest. source and dest
    can either be strings or any object with a read or
    write method, like StringIO for example.
    """
    source_descriptor = get_descriptor(source)
    destination_descriptor = get_descriptor(destination, read=False)

    while True:
        copy_buffer = source_descriptor.read(buffer_size)
        if copy_buffer:
            destination_descriptor.write(copy_buffer)
        else:
            break

    source_descriptor.close()
    destination_descriptor.close()


def load_backend(backend_string):
    logger.debug('loading: %s', backend_string)
    module_name, klass = backend_string.rsplit('.', 1)

    try:
        return getattr(import_module(module_name), klass)
    except ImportError as exception:
        logger.debug('error importing: %s; %s', backend_string, exception)
        raise


def fs_cleanup(filename, suppress_exceptions=True):
    """
    Tries to remove the given filename. Ignores non-existent files
    """
    try:
        os.remove(filename)
    except OSError:
        if suppress_exceptions:
            pass
        else:
            raise
