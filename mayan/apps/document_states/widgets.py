from __future__ import unicode_literals

from django import forms
from django.urls import reverse
from django.utils.html import format_html_join, mark_safe


def widget_transition_events(transition):
    return format_html_join(
        sep='\n', format_string='<div class="">{}</div>', args_generator=(
            (
                transition_trigger.event_type.label,
            ) for transition_trigger in transition.trigger_events.all()
        )
    )


def widget_workflow_diagram(workflow):
    return mark_safe(
        '<img alt="{}" class="img-responsive" src="{}" style="margin:auto;">'.format(
            _('Workflow preview'), reverse(
                viewname='document_states:workflow_image', kwargs={
                    'pk': workflow.pk
                }
            )
        )
    )


class WorkflowImageWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None):
        if value:
            output = []
            output.append(widget_workflow_diagram(value))
            return mark_safe(''.join(output))
        else:
            return ''
