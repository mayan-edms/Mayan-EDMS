from __future__ import unicode_literals

from django.apps import apps

from mayan.apps.control_codes.classes import ControlCode

__all__ = ('ControlCodeCabinetDocumentAdd',)


class ControlCodeCabinetDocumentAdd(ControlCode):
    arguments = ('label_path',)
    label = 'Add document to cabinet'
    name = 'cabinet_document_add_v1'

    def execute(self, context):
        Cabinet = apps.get_model(
            app_label='cabinets', model_name='Cabinet'
        )

        document = context['document_page'].document
        user = context.get('user', None)

        queryset = Cabinet.objects.all()
        for label in self.kwargs['label_path']:
            cabinet = queryset.get(label=label)
            queryset = cabinet.get_children()

        cabinet.document_add(document=document, _user=user)


ControlCode.register(control_code=ControlCodeCabinetDocumentAdd)
