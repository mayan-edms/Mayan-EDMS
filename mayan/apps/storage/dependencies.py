from __future__ import absolute_import, unicode_literals

from mayan.apps.dependencies.classes import PythonDependency

PythonDependency(
    module=__name__, name='pycryptodome', version_string='==3.9.7'
)
