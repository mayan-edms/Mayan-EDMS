from __future__ import absolute_import

import sys
import platform

from pbs import CommandNotFound

try:
    from pbs import lsb_release, uname
except CommandNotFound:
    POSIX = False
else:
    POSIX = True

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.db.models.loading import get_model
from django.http import Http404
from django.core.exceptions import PermissionDenied

from permissions.models import Permission

from .permissions import PERMISSION_INSTALLATION_DETAILS

def installation_details(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_INSTALLATION_DETAILS])

    paragraphs = []
    
    if POSIX:
        paragraphs.append(_(u'POSIX OS'))
        paragraphs.append(_(u'Distributor ID: %s') % lsb_release('-i','-s'))
        paragraphs.append(_(u'Description: %s') % lsb_release('-d','-s'))
        paragraphs.append(_(u'Release: %s') % lsb_release('-r','-s'))
        paragraphs.append(_(u'Codename: %s') % lsb_release('-c','-s'))
        paragraphs.append(_(u'System info: %s') % uname('-a'))
        
    paragraphs.append(_(u'Platform: %s') % sys.platform)
    paragraphs.append(_(u'Processor: %s') % platform.processor())
        
    return render_to_response('generic_template.html', {
        'paragraphs': paragraphs,
        'title': _(u'Installation environment details')
    }, context_instance=RequestContext(request))   
