from __future__ import unicode_literals

from django.http import QueryDict
from django.utils.encoding import force_bytes
from django.utils.six import PY3


class URL(object):
    def __init__(self, path=None, query_string=None):
        self._path = path
        self._query_string = query_string
        kwargs = {'mutable': True}
        if query_string:
            kwargs['query_string'] = query_string.encode('utf-8')

        self._args = QueryDict(**kwargs)

    @property
    def args(self):
        return self._args

    def to_string(self):
        if self._args.keys():
            query = '?{}'.format(self._args.urlencode())
        else:
            query = ''

        if self._path:
            path = self._path
        else:
            path = ''

        result = '{}{}'.format(path, query)

        if PY3:
            return result
        else:
            return force_bytes(result)
