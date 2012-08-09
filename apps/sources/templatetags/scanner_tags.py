from django.template import Library
from django.utils.translation import ugettext_lazy as _

from sources.models import LocalScanner

register = Library()


@register.assignment_tag
def scanner_list():
    list_of_scanners = LocalScanner.get_scanner_choices(description_only=True)
    if list_of_scanners:
        return list_of_scanners
    else:
        return [_(u'No scanners found.')]
    
