from django.utils.html import format_html_join

from mayan.apps.navigation.html_widgets import SourceColumnWidget


def widget_transition_events(transition):
    return format_html_join(
        sep='\n', format_string='<div class="">{}</div>', args_generator=(
            (
                transition_trigger.event_type.label,
            ) for transition_trigger in transition.trigger_events.all()
        )
    )


class WorkflowLogExtraDataWidget(SourceColumnWidget):
    template_name = 'document_states/extra_data.html'
