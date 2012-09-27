from __future__ import absolute_import

from django.template import Library

from ..models import AutoAdminSingleton

register = Library()


@register.simple_tag(takes_context=True)
def auto_admin_properties(context):
    context['auto_admin_properties'] = AutoAdminSingleton.singleton.get()
    return u''
