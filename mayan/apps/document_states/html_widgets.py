from __future__ import unicode_literals

from django.template.loader import render_to_string
from django.utils.html import format_html_join


def widget_transition_events(transition):
    return format_html_join(
        sep='\n', format_string='<div class="">{}</div>', args_generator=(
            (
                transition_trigger.event_type.label,
            ) for transition_trigger in transition.trigger_events.all()
        )
    )


class WorkflowLogExtraDataWidget(object):
    template_name = 'document_states/extra_data.html'

    def render(self, name=None, value=None):
        return render_to_string(
            template_name=self.template_name, context={
                'value': value
            }
        )
