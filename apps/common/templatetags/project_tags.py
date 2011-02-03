from django.template import TemplateSyntaxError, Library, VariableDoesNotExist
from django.conf import settings

register = Library()

@register.simple_tag
def project_name():
    return settings.PROJECT_TITLE
