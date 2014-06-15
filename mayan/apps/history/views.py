from __future__ import absolute_import

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.db.models.loading import get_model
from django.http import Http404
from django.core.exceptions import PermissionDenied

from permissions.models import Permission
from common.utils import encapsulate
from acls.models import AccessEntry

from .models import History, HistoryType
from .forms import HistoryDetailForm
from .permissions import PERMISSION_HISTORY_VIEW
from .widgets import history_entry_object_link, history_entry_summary


def history_list(request, object_list=None, title=None, extra_context=None):
    pre_object_list = object_list if not (object_list is None) else History.objects.all()

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_HISTORY_VIEW])
    except PermissionDenied:
        # If user doesn't have global permission, get a list of document
        # for which he/she does hace access use it to filter the
        # provided object_list
        final_object_list = AccessEntry.objects.filter_objects_by_access(PERMISSION_HISTORY_VIEW, request.user, pre_object_list, related='content_object')
    else:
        final_object_list = pre_object_list

    context = {
        'object_list': final_object_list,
        'title': title if title else _(u'history events'),
        'extra_columns': [
            {
                'name': _(u'object link'),
                'attribute': encapsulate(lambda x: history_entry_object_link(x))
            },
        ],
        'hide_object': True,
    }

    if extra_context:
        context.update(extra_context)

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))


def history_for_object(request, app_label, module_name, object_id):
    model = get_model(app_label, module_name)
    if not model:
        raise Http404
    content_object = get_object_or_404(model, pk=object_id)
    content_type = ContentType.objects.get_for_model(model)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_HISTORY_VIEW])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_HISTORY_VIEW, request.user, content_object)

    context = {
        'object_list': History.objects.filter(content_type=content_type, object_id=object_id),
        'title': _(u'history events for: %s') % content_object,
        'object': content_object,
        'hide_object': True,
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))


def history_view(request, object_id):
    history = get_object_or_404(History, pk=object_id)
    
    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_HISTORY_VIEW])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_HISTORY_VIEW, request.user, history.content_object)    

    form = HistoryDetailForm(instance=history, extra_fields=[
        {'label': _(u'Date'), 'field': lambda x: x.datetime.date()},
        {'label': _(u'Time'), 'field': lambda x: unicode(x.datetime.time()).split('.')[0]},
        {'label': _(u'Object'), 'field': 'content_object'},
        {'label': _(u'Event type'), 'field': lambda x: x.get_label()},
        {'label': _(u'Additional details'), 'field': lambda x: x.get_processed_details() or _(u'None')},
    ])

    return render_to_response('generic_detail.html', {
        'title': _(u'details for: %s') % history.get_processed_summary(),
        'form': form,
    },
    context_instance=RequestContext(request))


def history_type_list(request, history_type_pk):
    history_type = get_object_or_404(HistoryType, pk=history_type_pk)
    
    return history_list(
        request,
        object_list=History.objects.filter(history_type=history_type),
        title=_(u'history events of type: %s') % history_type,
    )
