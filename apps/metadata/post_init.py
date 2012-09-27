from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .settings import (AVAILABLE_MODELS, AVAILABLE_FUNCTIONS)
from .models import MetadataType

available_models_string = (_(u' Available models: %s') % u','.join([name for name, model in AVAILABLE_MODELS.items()])) if AVAILABLE_MODELS else u''
available_functions_string = (_(u' Available functions: %s') % u','.join([u'%s()' % name for name, function in AVAILABLE_FUNCTIONS.items()])) if AVAILABLE_FUNCTIONS else u''

MetadataType._meta.get_field('default').help_text=_(u'Enter a string to be evaluated.%s') % available_functions_string
MetadataType._meta.get_field('lookup').help_text=_(u'Enter a string to be evaluated.  Example: [user.get_full_name() for user in User.objects.all()].%s') % available_models_string
