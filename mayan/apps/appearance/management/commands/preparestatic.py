from __future__ import unicode_literals

from django.core import management

IGNORE_LIST = [
    'AUTHORS*', 'CHANGE*', 'CONTRIBUT*', 'CODE_OF_CONDUCT*', 'Grunt*',
    'LICENSE*', 'MAINTAIN*', 'README*', '*.html*', '*.less', '*.md', '*.nupkg',
    '*.nuspec', '*.scss*', '*.sh', '*tests*', 'bower*', 'composer.json*',
    'demo*', 'docs', 'grunt*', 'gulp*', 'install', 'less', 'package.json*',
    'package-lock*', 'test', 'tests', 'variable*',
]


class Command(management.BaseCommand):
    help = 'Call the collectstatic command with some sane defaults.'

    def handle(self, *app_labels, **options):
        management.call_command(
            command_name='collectstatic', ignore=IGNORE_LIST,
            clear=True
        )
