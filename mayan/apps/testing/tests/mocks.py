from .http_adapters import TestClientAdapter


def request_method_factory(test_case):
    def get_adapter(url):
        return TestClientAdapter(test_case=test_case)

    return get_adapter
