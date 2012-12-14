from __future__ import absolute_import

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from permissions.models import Permission

from .permissions import PERMISSION_INSTALLATION_DETAILS
from .models import Installation


def installation_details(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_INSTALLATION_DETAILS])

    paragraphs = []
    for instance in Installation().get_properties():
        paragraphs.append('%s: %s' % (unicode(instance.label), instance.value))

    return render_to_response('generic_template.html', {
        'paragraphs': paragraphs,
        'title': _(u'Installation environment details')
    }, context_instance=RequestContext(request))
