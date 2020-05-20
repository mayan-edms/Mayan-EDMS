from django.http import QueryDict
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.six import PY3


class URL(object):
    def __init__(
        self, path=None, query_string=None, query=None, viewname=None
    ):
        if viewname:
            path = reverse(viewname=viewname)
        self._path = path
        self._query_string = query_string
        self._query = query

        kwargs = {'mutable': True}
        if self._query_string:
            kwargs['query_string'] = self._query_string.encode('utf-8')

        self._args = QueryDict(**kwargs)

        if self._query:
            self.args.update(self._query)

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
