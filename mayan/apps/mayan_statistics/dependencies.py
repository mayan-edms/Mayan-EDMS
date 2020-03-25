from mayan.apps.dependencies.classes import JavaScriptDependency

JavaScriptDependency(
    module=__name__, name='chart.js', static_folder='statistics',
    version_string='=2.7.2'
)
