from __future__ import unicode_literals

from django import forms


class WorkflowImageWidget(forms.widgets.Widget):
    template_name = 'document_states/forms/widgets/workflow_image.html'

    def format_value(self, value):
        if value == '' or value is None:
            return None
        return value
