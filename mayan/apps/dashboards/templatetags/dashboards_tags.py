from django.template import Library

from ..classes import Dashboard
from ..settings import setting_default_dashboard_name

register = Library()


@register.simple_tag(takes_context=True)
def dashboards_render_dashboard(context, name):
    return Dashboard.get(name=name).render(request=context.request)


@register.simple_tag(takes_context=True)
def dashboards_render_default_dashboard(context):
    dashboard_name = setting_default_dashboard_name.value

    if dashboard_name:
        return Dashboard.get(name=dashboard_name).render(
            request=context.request
        )
    else:
        return ''
