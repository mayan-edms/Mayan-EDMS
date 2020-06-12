import logging

from fuse import FUSE

from django.core import management
from django.core.management.base import CommandError

from ...filesystems import IndexFilesystem

logger = logging.getLogger(name=__name__)


class Command(management.BaseCommand):
    help = 'Mount an index as a FUSE filesystem.'

    def add_arguments(self, parser):
        parser.add_argument('slug', nargs='?', help='Index slug')
        parser.add_argument('mount_point', nargs='?', help='Mount point')
        parser.add_argument(
            '--allow-other', action='store_true', dest='allow_other',
            default=False,
            help='All users (including root) can access the index files.'
        )
        parser.add_argument(
            '--allow-root', action='store_true', dest='allow_root',
            default=False,
            help='Mount access is limited to the user mounting the index and '
            'root. This option and --allow-other are mutually exclusive.'
        )
        parser.add_argument(
            '--background', action='store_true', dest='background',
            default=False,
            help='Mounts and serves the index as a background process.'
        )
        parser.add_argument(
            '--log-level', action='store', dest='log_level',
            default='ERROR',
            help='Changes the level of logging. Options: CRITICAL, '
            'ERROR, WARNING, INFO, DEBUG, NOTSET. Default is ERROR.'
        )

    def handle(self, *args, **options):
        if not options.get('slug') or not options.get('mount_point'):
            self.stderr.write(self.style.ERROR('Incorrect number of arguments'))
            exit(1)

        foreground = not options['background']

        if foreground:
            self.stdout.write(
                'Mounting index in the foreground. No further '
                'output will be generated.'
            )

        level = getattr(logging, options['log_level'], None)
        if not level:
            self.stderr.write(self.style.ERROR('Unknown log level {}'.format(level)))
            exit(1)

        logging.basicConfig(level=level)

        try:
            FUSE(
                operations=IndexFilesystem(index_slug=options['slug']),
                mountpoint=options['mount_point'], nothreads=True,
                foreground=not options['background'],
                allow_other=options['allow_other'],
                allow_root=options['allow_root']
            )
        except RuntimeError:
            if options['allow_other'] or options['allow_root']:
                raise CommandError(
                    'Make sure \'user_allow_other\' is set in /etc/fuse.conf'
                )
            else:
                raise
