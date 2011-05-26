from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.http import urlencode
from django.contrib.contenttypes.models import ContentType

from permissions.api import check_permissions

from history.models import History
from history.api import history_types_dict
from history.forms import HistoryDetailForm
from history import PERMISSION_HISTORY_VIEW


def history_list(request):
    check_permissions(request.user, [PERMISSION_HISTORY_VIEW])

    context = {
        'object_list': History.objects.all(),
        'title': _(u'history events'),
        'extra_columns': [
            {
                'name': _(u'date and time'),
                'attribute': 'datetime'
            },
            {
                'name': _(u'summary'),
                'attribute': lambda x: '<a href="%(url)s">%(label)s</a>' % {
                    'url': x.get_absolute_url(),
                    'label': unicode(x.get_processed_summary())
                }
            }
        ],
        'hide_object': True,
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))


def history_for_object(request, content_type_id, object_id):
    check_permissions(request.user, [PERMISSION_HISTORY_VIEW])

    content_type = get_object_or_404(ContentType, pk=content_type_id)
    content_object = get_object_or_404(content_type.model_class(), pk=object_id)

    context = {
        'object_list': History.objects.filter(content_type=content_type_id, object_id=object_id),
        'title': _(u'history for: %s') % content_object,
        'extra_columns': [
            {
                'name': _(u'date and time'),
                'attribute': 'datetime'
            },
            {
                'name': _(u'summary'),
                'attribute': lambda x: '<a href="%(url)s">%(label)s</a>' % {
                    'url': x.get_absolute_url(),
                    'label': unicode(x.get_processed_summary())
                }
            }
        ],
        'hide_object': True,
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))


def history_view(request, object_id):
    check_permissions(request.user, [PERMISSION_HISTORY_VIEW])

    history = get_object_or_404(History, pk=object_id)
    
    
    form = HistoryDetailForm(instance=history, extra_fields=[
        {'label': _(u'Date'), 'field':lambda x: x.datetime.date()},
        {'label': _(u'Time'), 'field':lambda x: unicode(x.datetime.time()).split('.')[0]},
        {'label': _(u'Object'), 'field': 'content_object'},
        {'label': _(u'Event type'), 'field': lambda x: x.get_label()},
        {'label': _(u'Event details'), 'field': lambda x: x.get_processed_details()},
    ])
    
    return render_to_response('generic_detail.html', {
        'title': _(u'details for: %s') % history.get_processed_summary(),
        'form': form,
        'object': history,
    },
    context_instance=RequestContext(request))
