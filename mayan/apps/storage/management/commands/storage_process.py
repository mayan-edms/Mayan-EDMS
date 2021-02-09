from django.core import management
from django.utils.translation import ugettext_lazy as _

from ...utils import PassthroughStorageProcessor


class Command(management.BaseCommand):
    help = 'Process model files over a storage pipeline.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--app', action='store', dest='app_label',
            help=_('Name of the app to process.'),
            required=True,
        )
        parser.add_argument(
            '--log', action='store', dest='log_file',
            help=_(
                'Path of the database (.dbm) file that will be created/read '
                'to keep track of items processed.'
            ),
            required=True,
        )
        parser.add_argument(
            '--model', action='store', dest='model_name',
            help=_('Process a specific model.'),
            required=True,
        )
        parser.add_argument(
            '--reverse', action='store_true', dest='reverse',
            help=_(
                'Process the files in reverse to undo the storage '
                'pipeline transformations.'
            )
        )
        parser.add_argument(
            '--storage_name', action='store', dest='defined_storage_name',
            help=_('Name of the storage to process.'),
            required=True,
        )

    def handle(self, *args, **options):
        processor = PassthroughStorageProcessor(
            app_label=options['app_label'],
            defined_storage_name=options['defined_storage_name'],
            log_file=options['log_file'], model_name=options['model_name'],
        )
        processor.execute(reverse=options['reverse'])
