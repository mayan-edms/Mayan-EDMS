from __future__ import unicode_literals

from django.apps import apps

from mayan.apps.control_codes.classes import ControlCode

__all__ = ('ControlCodeDocumentMetadataAdd',)


class ControlCodeDocumentMetadataAdd(ControlCode):
    arguments = ('name', 'value')
    label = 'Add document metadata'
    name = 'document_metadata_add_v1'

    def execute(self, context):
        DocumentMetadata = apps.get_model(
            app_label='metadata', model_name='DocumentMetadata'
        )
        MetadataType = apps.get_model(
            app_label='metadata', model_name='MetadataType'
        )

        document = context['document_page'].document
        user = context.get('user', None)

        metadata_type = MetadataType.objects.get(name=self.kwargs['name'])
        document_metadata = DocumentMetadata(
            document=document, metadata_type=metadata_type,
            value=self.kwargs['value']
        )
        document_metadata.save(_user=user)


ControlCode.register(control_code=ControlCodeDocumentMetadataAdd)
