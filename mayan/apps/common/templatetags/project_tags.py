from django.conf import settings
from django.template import Library

import mayan

register = Library()


@register.simple_tag
def project_name():
    return settings.PROJECT_TITLE


@register.simple_tag
def project_version():
    return mayan.__version__

