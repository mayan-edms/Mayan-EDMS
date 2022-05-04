import logging

from fuse import FUSE

from django.core.management.base import CommandError

from ..filesystems import MirrorFilesystem

logger = logging.getLogger(name=__name__)


class MountCommandMixin:
    node_identifier_argument = None
    node_identifier_help_text = None
    node_text_attribute = None

    def add_arguments(self, parser):
        parser.add_argument(
            self.node_identifier_argument, nargs='?',
            help=self.node_identifier_help_text
        )
        parser.add_argument('mount_point', nargs='?', help='Mount point')
        parser.add_argument(
            '--allow-other', action='store_true', dest='allow_other',
            default=False,
            help='All users (including root) can access the files.'
        )
        parser.add_argument(
            '--allow-root', action='store_true', dest='allow_root',
            default=False,
            help='Mount access is limited to the user mounting the '
            'documents and root. This option and --allow-other are '
            'mutually exclusive.'
        )
        parser.add_argument(
            '--background', action='store_true', dest='background',
            default=False,
            help='Mounts the documents and serves them as a background '
            'process.'
        )
        parser.add_argument(
            '--log-level', action='store', dest='log_level',
            default='ERROR',
            help='Changes the level of logging. Options: CRITICAL, '
            'ERROR, WARNING, INFO, DEBUG, NOTSET. Default is ERROR.'
        )
        self.add_extra_arguments(parser)

    def add_extra_arguments(self, parser):
        """
        Optional method to allow subclasses to add their own arguments.
        """

    def factory_func_document_container_node(self, *args, **options):
        raise NotImplementedError

    def handle(self, *args, **options):
        if not options.get(self.node_identifier_argument) or not options.get('mount_point'):
            self.stderr.write(msg='Incorrect number of arguments')
            exit(1)

        foreground = not options['background']

        if foreground:
            self.stdout.write(
                msg='Mounting documents in the foreground. No further '
                'output will be generated.'
            )

        level = getattr(logging, options['log_level'], None)
        if not level:
            self.stderr.write(
                msg='Unknown log level {}'.format(level)
            )
            exit(1)

        logging.basicConfig(level=level)

        try:
            operations = MirrorFilesystem(
                func_document_container_node=self.factory_func_document_container_node(
                    *args, **options
                ), node_text_attribute=self.node_text_attribute
            )
        except Exception as exception:
            self.stderr.write(
                msg='Unable to initialize filesystem operations; {}'.format(
                    exception
                )
            )
            exit(1)

        try:
            FUSE(
                operations=operations, mountpoint=options['mount_point'],
                nothreads=True, foreground=not options['background'],
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
