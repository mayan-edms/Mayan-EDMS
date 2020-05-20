from django.template import Library

from ..models import AutoAdminSingleton

register = Library()


@register.inclusion_tag('autoadmin/credentials.html')
def autoadmin_partial():
    try:
        return {'autoadmin_properties': AutoAdminSingleton.objects.get()}
    except AutoAdminSingleton.DoesNotExist:
        return {'autoadmin_properties': None}


@register.simple_tag(takes_context=True)
def autoadmin_properties(context):
    try:
        context['autoadmin_properties'] = AutoAdminSingleton.objects.get()
    except AutoAdminSingleton.DoesNotExist:
        context['autoadmin_properties'] = None

    return ''
