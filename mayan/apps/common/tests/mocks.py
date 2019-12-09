from __future__ import unicode_literals

import requests

from .http_adapters import TestClientAdapter


def request_method_factory(test_case):
    def request(method, url, **kwargs):
        with requests.sessions.Session() as session:
            session.mount(
                prefix=test_case.testserver_prefix,
                adapter=TestClientAdapter(test_case=test_case)
            )
            return session.request(method=method, url=url, **kwargs)

    return request
