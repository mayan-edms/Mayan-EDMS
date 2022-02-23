from django.apps import apps

from ..classes import DuplicateBackend


class TestDuplicateBackend(DuplicateBackend):
    label = 'Test_duplicate_backend'

    def process(self, document):
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        return Document.objects.exclude(pk=document.pk)
