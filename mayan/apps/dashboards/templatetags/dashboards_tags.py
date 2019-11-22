from __future__ import unicode_literals

from django.template import Library

from ..classes import Dashboard

register = Library()


@register.simple_tag(takes_context=True)
def dashboards_render_dashboard(context, name):
    return Dashboard.get(name=name).render(request=context.request)
