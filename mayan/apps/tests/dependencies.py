from mayan.apps.dependencies.classes import (
    BinaryDependency, PythonDependency
)
from mayan.apps.dependencies.environments import environment_testing

from .literals import DEFAULT_FIREFOX_GECKODRIVER_PATH

BinaryDependency(
    environment=environment_testing, label='firefox-geckodriver',
    module=__name__, name='geckodriver',
    path=DEFAULT_FIREFOX_GECKODRIVER_PATH
)
PythonDependency(
    environment=environment_testing, module=__name__, name='coverage',
    version_string='==5.1'
)
PythonDependency(
    environment=environment_testing, module=__name__, name='coveralls',
    version_string='==2.0.0'
)
PythonDependency(
    environment=environment_testing, module=__name__,
    name='django-test-migrations', version_string='==0.2.0'
)
PythonDependency(
    environment=environment_testing,
    module=__name__, name='django-test-without-migrations',
    version_string='==0.6'
)
# Mock is set to production so that it is available in the Docker image
# and allows running the test suit in production.
PythonDependency(
    module=__name__, name='mock', version_string='==4.0.2'
)
PythonDependency(
    environment=environment_testing, module=__name__, name='selenium',
    version_string='==3.141.0'
)
PythonDependency(
    environment=environment_testing, module=__name__, name='tox',
    version_string='==3.14.6'
)
PythonDependency(
    environment=environment_testing, module=__name__, name='psutil',
    version_string='==5.7.0'
)
