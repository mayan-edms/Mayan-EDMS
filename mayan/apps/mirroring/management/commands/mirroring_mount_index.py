from django.core import management

from mayan.apps.document_indexing.models.index_instance_models import IndexInstance

from ..base import MountCommandMixin


class Command(MountCommandMixin, management.BaseCommand):
    help = 'Mount an index as a filesystem.'
    node_identifier_argument = 'slug'
    node_identifier_help_text = 'Index slug'
    node_text_attribute = 'value'

    def factory_func_document_container_node(self, *args, **options):
        index_instance = IndexInstance.objects.get(
            **{
                self.node_identifier_argument: options[self.node_identifier_argument]
            }
        )

        def func_document_container_node():
            return index_instance.get_root()

        return func_document_container_node
