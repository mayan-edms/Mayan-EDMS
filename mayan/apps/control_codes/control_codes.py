from __future__ import unicode_literals

from .classes import ControlCode

__all__ = ('ControlCodeAttributeEdit',)


class ControlCodeAttributeEdit(ControlCode):
    arguments = ('name', 'value')
    label = 'Change document property'
    name = 'document_property_edit_v1'

    def execute(self, context):
        document = context['document_page'].document
        user = context.get('user', None)

        setattr(document, self.kwargs['name'], self.kwargs['value'])
        document.save(_user=user)


ControlCode.register(control_code=ControlCodeAttributeEdit)
