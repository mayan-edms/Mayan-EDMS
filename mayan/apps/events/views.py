from __future__ import absolute_import, unicode_literals

from django.core.exceptions import PermissionDenied
from django.db.models.loading import get_model
from django.http import Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from actstream.models import Action, any_stream

from acls.models import AccessEntry
from common.utils import encapsulate
from permissions.models import Permission

from .classes import Event
from .permissions import PERMISSION_EVENTS_VIEW
from .widgets import event_object_link


def events_list(request, app_label=None, module_name=None, object_id=None, verb=None):
    extra_columns = []

    context = {
        'extra_columns': extra_columns,
        'hide_object': True,
    }

    if app_label and module_name and object_id:
        model = get_model(app_label, module_name)
        if not model:
            raise Http404
        content_object = get_object_or_404(model, pk=object_id)

        try:
            Permission.objects.check_permissions(request.user, [PERMISSION_EVENTS_VIEW])
        except PermissionDenied:
            AccessEntry.objects.check_access(PERMISSION_EVENTS_VIEW, request.user, content_object)

        context.update({
            'object_list': any_stream(content_object),
            'title': _('Events for: %s') % content_object,
            'object': content_object
        })
    elif verb:
        pre_object_list = Action.objects.filter(verb=verb)

        try:
            Permission.objects.check_permissions(request.user, [PERMISSION_EVENTS_VIEW])
        except PermissionDenied:
            # If user doesn't have global permission, get a list of document
            # for which he/she does hace access use it to filter the
            # provided object_list
            object_list = AccessEntry.objects.filter_objects_by_access(PERMISSION_EVENTS_VIEW, request.user, pre_object_list, related='content_object')
        else:
            object_list = pre_object_list

        context.update({
            'title': _('Events of type: %s') % Event.get_label(verb),
            'object_list': object_list
        })
    else:
        pre_object_list = Action.objects.all()

        try:
            Permission.objects.check_permissions(request.user, [PERMISSION_EVENTS_VIEW])
        except PermissionDenied:
            # If user doesn't have global permission, get a list of document
            # for which he/she does hace access use it to filter the
            # provided object_list
            object_list = AccessEntry.objects.filter_objects_by_access(PERMISSION_EVENTS_VIEW, request.user, pre_object_list, related='content_object')
        else:
            object_list = pre_object_list

        context.update({
            'title': _('Events'),
            'object_list': object_list
        })

    if not (app_label and module_name and object_id):
        extra_columns.append(
            {
                'name': _('Target'),
                'attribute': encapsulate(lambda entry: event_object_link(entry))
            }
        )
    return render_to_response('main/generic_list.html', context,
                              context_instance=RequestContext(request))
