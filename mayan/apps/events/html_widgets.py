from django.apps import apps
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from mayan.apps.templating.classes import Template

from .classes import EventType


def widget_event_actor_link(context, attribute=None):
    entry = context['object']

    ContentType = apps.get_model(
        app_label='contenttypes', model_name='ContentType'
    )

    if attribute:
        entry = getattr(entry, attribute)

    if entry.actor == entry.target:
        label = _('System')
        url = None
    else:
        label = entry.actor
        content_type = ContentType.objects.get_for_model(model=entry.actor)

        url = reverse(
            viewname='events:events_for_object', kwargs={
                'app_label': content_type.app_label,
                'model_name': content_type.model,
                'object_id': entry.actor.pk
            }
        )

    if url:
        return Template(
            template_string='<a href="{{ url }}">{{ label }}</a>'
        ).render(context={'label': entry.actor, 'url': url})
    else:
        return label


def widget_event_type_link(context, attribute=None):
    entry = context['object']

    if attribute:
        entry = getattr(entry, attribute)

    return mark_safe(
        '<a href="%(url)s">%(label)s</a>' % {
            'url': reverse(viewname='events:events_by_verb', kwargs={'verb': entry.verb}),
            'label': EventType.get(name=entry.verb)
        }
    )
