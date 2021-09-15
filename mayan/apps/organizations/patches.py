from django.http.request import HttpRequest
from django.utils.functional import cached_property

from .settings import setting_organization_installation_url


def patch_HttpRequest():
    class MockClass:
        @cached_property
        def _patched_current_scheme_host(self):
            if setting_organization_installation_url.value:
                return setting_organization_installation_url.value
            else:
                return self._original_current_scheme_host

    _original_current_scheme_host = HttpRequest._current_scheme_host

    HttpRequest._current_scheme_host = MockClass._patched_current_scheme_host
    HttpRequest._original_current_scheme_host = _original_current_scheme_host
