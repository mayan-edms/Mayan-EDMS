from __future__ import absolute_import

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import PermissionDenied

from permissions.models import Permission
from common.utils import encapsulate

from .permissions import PERMISSION_VIEW_JOB_LIST
from .api import get_job_list


def job_list(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_VIEW_JOB_LIST])

    context = {
        'object_list': get_job_list(),
        'title': _(u'interval jobs'),
        'extra_columns': [
            {
                'name': _(u'label'),
                'attribute': encapsulate(lambda job: job['title'])
            },
            {
                'name': _(u'start date time'),
                'attribute': encapsulate(lambda job: job['job'].trigger.start_date)
            },
            {
                'name': _(u'interval'),
                'attribute': encapsulate(lambda job: job['job'].trigger.interval)
            },
        ],
        'hide_object': True,
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))
