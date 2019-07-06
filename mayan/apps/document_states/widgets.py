from __future__ import unicode_literals

from django import forms
from django.utils.html import format_html_join


def widget_transition_events(transition):
    return format_html_join(
        sep='\n', format_string='<div class="">{}</div>', args_generator=(
            (
                transition_trigger.event_type.label,
            ) for transition_trigger in transition.trigger_events.all()
        )
    )


class WorkflowImageWidget(forms.widgets.Widget):
    template_name = 'document_states/forms/widgets/workflow_image.html'

    def format_value(self, value):
        if value == '' or value is None:
            return None
        return value
