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
    help = 'Call the collectstatic command with some specific defaults.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--noinput', '--no-input',
            action='store_false', dest='interactive', default=True,
            help='Do NOT prompt the user for input of any kind.',
        )
        parser.add_argument(
            '-n', '--dry-run',
            action='store_true', dest='dry_run', default=False,
            help='Do everything except modify the filesystem.',
        )
        parser.add_argument(
            '-c', '--clear',
            action='store_true', dest='clear', default=False,
            help='Clear the existing files using the storage '
                 'before trying to copy or link the original file.',
        )
        parser.add_argument(
            '-l', '--link',
            action='store_true', dest='link', default=False,
            help='Create a symbolic link to each file instead of copying.',
        )

    def handle(self, *app_labels, **options):
        management.call_command(
            command_name='collectstatic',
            clear=options['clear'],
            dry_run=options['dry_run'],
            ignore=IGNORE_LIST,
            interactive=options['interactive'],
            link=options['link'],
        )
