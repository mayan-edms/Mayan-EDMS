from django.core.management.base import BaseCommand

from mayan.apps.common.utils import ProgressBar, parse_range

from ...classes import SearchModel
from ...tasks import task_index_instance


class Command(BaseCommand):
    help = 'Index a list of objects.'
    missing_args_message = 'You must provide a search model name and an ID range.'

    def add_arguments(self, parser):
        parser.add_argument(
            dest='model_name', help='Name of search model to index.',
            metavar='<model name>'
        )
        parser.add_argument(
            dest='id_range', help='Range of IDs to index.',
            metavar='ID range'
        )

    def handle(self, model_name, id_range, **options):
        try:
            search_model = SearchModel.get(name=model_name)
        except KeyError:
            self.stderr.write('Unknown search model `{}`'.format(model_name))
            exit(1)

        try:
            results = parse_range(astr=id_range)
        except Exception as exception:
            self.stderr.write(
                'Unknown or invalid range format `{}`; {}'.format(
                    id_range, exception
                )
            )
            exit(1)

        self.stdout.write('\nSearch model: {}'.format(search_model))

        progress_bar = ProgressBar(
            decimal_places=2, length=40,
            prefix='Queuing instances indexing:', suffix='complete',
            total=len(results)
        )

        for id_number_index, id_number in enumerate(results):
            progress_bar.update(index=id_number_index + 1)

            task_index_instance.apply_async(
                kwargs={
                    'app_label': search_model.app_label,
                    'model_name': search_model.model_name,
                    'object_id': int(id_number)
                }
            )
