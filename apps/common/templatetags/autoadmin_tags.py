from django.template import Library
from django.utils.importlib import import_module

from common.models import AutoAdminSingleton

register = Library()


@register.simple_tag(takes_context=True)
def auto_admin_properties(context):
    context['auto_admin_properties'] = AutoAdminSingleton.objects.get()
    return u''
