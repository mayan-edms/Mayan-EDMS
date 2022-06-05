from mayan.apps.dependencies.environments import environment_build

from .classes import PythonDependency

PythonDependency(
    module=__name__, name='node-semver', version_string='==0.8.1'
)
PythonDependency(
    environment=environment_build, module=__name__, name='packaging',
    version_string='==21.3'
)
