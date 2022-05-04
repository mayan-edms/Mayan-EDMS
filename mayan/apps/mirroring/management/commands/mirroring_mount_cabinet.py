from django.core import management

from mayan.apps.cabinets.models import Cabinet

from ..base import MountCommandMixin

DEFAULT_DELIMITER = ','


class Command(MountCommandMixin, management.BaseCommand):
    help = 'Mount a cabinet as a filesystem.'
    node_identifier_argument = 'label'
    node_identifier_help_text = 'Cabinet label'
    node_text_attribute = 'label'

    def add_extra_arguments(self, parser):
        parser.add_argument(
            '--delimiter', action='store', dest='delimiter',
            default=DEFAULT_DELIMITER, help='Character used to separate '
            'the cabinet levels. Defaults to "{}".'.format(DEFAULT_DELIMITER)
        )

    def factory_func_document_container_node(self, *args, **options):
        levels = options[self.node_identifier_argument].split(options['delimiter'])

        cabinet = None
        for level in levels:
            try:
                if cabinet is None:
                    cabinet = Cabinet.objects.get(label=level)
                else:
                    cabinet = Cabinet.objects.get(label=level, parent=cabinet)
            except Cabinet.DoesNotExist as exception:
                self.stderr.write(
                    msg='Cabinet level "{}" not found; {}'.format(
                        level, exception
                    )
                )
                exit(1)

        def func_document_container_node():
            return cabinet

        return func_document_container_node
