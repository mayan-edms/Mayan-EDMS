from __future__ import unicode_literals

from ..classes import Dependency, Provider


class TestProvider(Provider):
    """Test provider"""


class TestDependency(Dependency):
    provider_class = TestProvider
