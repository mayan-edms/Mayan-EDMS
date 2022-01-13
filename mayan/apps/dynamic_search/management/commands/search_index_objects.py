from django.core.management.base import BaseCommand

from mayan.apps.common.utils import parse_range

from ...classes import SearchModel
from ...tasks import task_index_search_model


class Command(BaseCommand):
    help = 'Index a list of objects.'
    missing_args_message = 'You must provide a search model name and an ID range.'

    def add_arguments(self, parser):
        parser.add_argument(
            dest='model_name', help='Name of search model to index.',
            metavar='<model name>'
        )
        parser.add_argument(
            dest='id_range_string', help='Range of IDs to index.',
            metavar='<ID range>'
        )

    def handle(self, model_name, id_range_string, **options):
        try:
            search_model = SearchModel.get(name=model_name)
        except KeyError:
            self.stderr.write(
                msg='Unknown search model `{}`'.format(model_name)
            )
            exit(1)

        try:
            id_range = parse_range(range_string=id_range_string)
        except Exception as exception:
            self.stderr.write(
                msg='Unknown or invalid range format `{}`; {}'.format(
                    id_range_string, exception
                )
            )
            exit(1)

        task_index_search_model.apply_async(
            kwargs={
                'range_string': id_range_string,
                'search_model_full_name': search_model.get_full_name()
            }
        )

        self.stdout.write(
            msg='\nInstances queued for indexing: {}'.format(
                len(list(id_range))
            )
        )
