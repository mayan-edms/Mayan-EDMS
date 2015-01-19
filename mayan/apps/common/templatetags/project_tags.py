from django.conf import settings
from django.template import Library

register = Library()


@register.simple_tag
def project_name():
    return settings.PROJECT_TITLE
