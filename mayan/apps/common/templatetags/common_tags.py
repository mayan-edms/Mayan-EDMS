from __future__ import unicode_literals

from json import dumps

from django.template import Context, Library
from django.template.loader import get_template
from django.utils.encoding import force_text

import mayan

from ..classes import Collection, Dashboard
from ..literals import MESSAGE_SQLITE_WARNING
from ..utils import check_for_sqlite, return_attrib

register = Library()


@register.simple_tag
def check_sqlite():
    if check_for_sqlite():
        return MESSAGE_SQLITE_WARNING


@register.simple_tag
def get_collections():
    return Collection.get_all()


@register.filter
def get_encoded_parameter(item, parameters_dict):
    result = {}
    for attrib_name, attrib in parameters_dict.items():
        result[attrib_name] = return_attrib(item, attrib)
    return dumps(result)


@register.filter
def get_type(value):
    return force_text(type(value))


@register.filter
def object_property(value, arg):
    return return_attrib(value, arg)


@register.simple_tag
def project_information(attribute_name):
    return getattr(mayan, attribute_name)


@register.simple_tag(takes_context=True)
def render_dashboard(context, name):
    return Dashboard.get(name=name).render(request=context.request)


@register.simple_tag(takes_context=True)
def render_subtemplate(context, template_name, template_context):
    """
    Renders the specified template with the mixed parent and
    subtemplate contexts
    """
    new_context = Context(context.flatten())
    new_context.update(Context(template_context))
    return get_template(template_name).render(new_context.flatten())
