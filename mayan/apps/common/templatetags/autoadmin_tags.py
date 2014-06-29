from django.template import Library

from common.models import AutoAdminSingleton

register = Library()


@register.simple_tag(takes_context=True)
def auto_admin_properties(context):
    context['auto_admin_properties'] = AutoAdminSingleton.objects.get()
    return u''
