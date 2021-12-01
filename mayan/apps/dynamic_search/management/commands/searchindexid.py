from django.core.management.base import BaseCommand

from mayan.apps.common.utils import ProgressBar, parse_range

from ...classes import SearchModel
from ...tasks import task_index_instance


class Command(BaseCommand):
    help = 'Index a list of objects.'
    missing_args_message = 'You must provide a search model name and an ID range.'

    def add_arguments(self, parser):
        parser.add_argument(
            'model_name', help='Name of search model to index.',
            metavar='model name', nargs='+',
        )
        parser.add_argument(
            'id_range', help='Range of IDs to index.', metavar='ID range',
            nargs='+'
        )

    def handle(self, model_name, id_range, **options):
        search_model = SearchModel.get(name=model_name[0])
        results = parse_range(astr=id_range[0])

        self.stdout.write('\nSearch model: {}'.format(search_model))

        progress_bar = ProgressBar(
            decimal_places=2, length=40, prefix='Queuing instances:',
            suffix='complete', total=len(results)
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
