from __future__ import unicode_literals

from .classes import ControlCode


class ControlCodeAttributeEdit(ControlCode):
    arguments = ('attribute', 'value')
    label = 'Change document attribute'
    name = 'document_attribute_edit'

    def execute(self, context):
        document = context['document_page'].document
        print("!@#@", self.attribute, self.value)
        setattr(document, self.attribute, self.value)
        print("!!", document.label)

        document.save()


ControlCode.register(control_code=ControlCodeAttributeEdit)
