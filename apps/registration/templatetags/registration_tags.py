from __future__ import absolute_import 

from django.core.urlresolvers import reverse, NoReverseMatch
from django.template import (TemplateSyntaxError, Library,
    VariableDoesNotExist, Node, Variable)
from django.utils.translation import ugettext as _

from ..models import RegistrationSingleton

register = Library()


@register.simple_tag
def registered_name():
    if RegistrationSingleton.registration_state():
        return RegistrationSingleton.registered_name()
    else:
        return _(u'Unregistered')
