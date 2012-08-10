from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse

from permissions.models import Permission

from .api import ModuleBackup
#from .permissions import 


def backup_view(request):
    #Permission.objects.check_permissions(request.user, [])

    context = {
        'object_list': ModuleBackup.get_all(),
        'title': _(u'apps registered for backup'),
        'hide_link': True,
        #'extra_columns': [
        #    {'name': _(u'description'), 'attribute': 'description'},
        #],
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))
