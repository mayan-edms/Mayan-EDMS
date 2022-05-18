from mayan.apps.dependencies.classes import (
    JavaScriptDependency, PythonDependency
)

JavaScriptDependency(
    module=__name__, name='signature_pad', version_string='=4.0.4'
)
PythonDependency(
    module=__name__, name='CairoSVG', version_string='==2.5.2'
)
