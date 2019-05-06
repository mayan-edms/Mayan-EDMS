from __future__ import unicode_literals

import errno
import os
import warnings

from pathlib2 import Path

from django.conf import settings
from django.core import management
from django.core.management.base import CommandError
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.models import DocumentType
from mayan.apps.storage.utils import fs_cleanup

from ...literals import MESSAGE_DEPRECATION_WARNING
from ...warnings import DeprecationWarning

CONVERTDB_FOLDER = 'convertdb'
CONVERTDB_OUTPUT_FILENAME = 'migrate.json'


class Command(management.BaseCommand):
    help = 'Convert from a database backend to another one.'

    def __init__(self, *args, **kwargs):
        warnings.warn(
            category=DeprecationWarning,
            message=force_text(MESSAGE_DEPRECATION_WARNING)
        )

        super(Command, self).__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument(
            'args', metavar='app_label[.ModelName]', nargs='*',
            help=_(
                'Restricts dumped data to the specified app_label or '
                'app_label.ModelName.'
            )
        )
        parser.add_argument(
            '--from', action='store', default='default', dest='from',
            help=_(
                'The database from which data will be exported. If omitted '
                'the database named "default" will be used.'
            ),
        )
        parser.add_argument(
            '--to', action='store', default='default', dest='to',
            help=_(
                'The database to which data will be imported. If omitted '
                'the database named "default" will be used.'
            ),
        )
        parser.add_argument(
            '--force', action='store_true', dest='force',
            help=_(
                'Force the conversion of the database even if the receiving '
                'database is not empty.'
            ),
        )

    def handle(self, *app_labels, **options):
        # Create the media/convertdb folder
        convertdb_folder_path = force_text(
            Path(
                settings.MEDIA_ROOT, CONVERTDB_FOLDER
            )
        )

        try:
            os.makedirs(convertdb_folder_path)
        except OSError as exception:
            if exception.errno == errno.EEXIST:
                pass

        convertdb_file_path = force_text(
            Path(
                convertdb_folder_path, CONVERTDB_OUTPUT_FILENAME
            )
        )

        management.call_command(command_name='purgeperiodictasks')

        management.call_command(
            'dumpdata', *app_labels, all=True,
            database=options['from'], natural_primary=True,
            natural_foreign=True, output=convertdb_file_path,
            interactive=False, format='json'
        )

        if DocumentType.objects.using(options['to']).count() and not options['force']:
            fs_cleanup(convertdb_file_path)
            raise CommandError(
                'There is existing data in the database that will be '
                'used for the import. If you proceed with the conversion '
                'you might lose data. Please check your settings.'
            )

        management.call_command(
            'loaddata', convertdb_file_path, database=options['to'], interactive=False,
            verbosity=3
        )
        fs_cleanup(convertdb_file_path)
