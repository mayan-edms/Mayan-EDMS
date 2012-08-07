from __future__ import absolute_import

from django.contrib import messages
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

#from permissions.models import Permission
#from common.utils import encapsulate

#from .permissions import PERMISSION_VIEW_SCHEDULER_LIST, PERMISSION_VIEW_JOB_LIST

from .models import TrashCan, TrashCanItem


def trash_can_list(request):
    #Permission.objects.check_permissions(request.user, [PERMISSION_VIEW_JOB_LIST])

    context = {
        'object_list': TrashCan.objects.all(),
        'title': _(u'trash cans'),
        'extra_columns': [
            {
                'name': _(u'name'),
                'attribute': 'name'
            },
            {
                'name': _(u'label'),
                'attribute': 'label'
            },
            {
                'name': _(u'items'),
                'attribute': 'items.count'
            },
        ],
        'hide_object': True,
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))


def trash_can_items(request, trash_can_pk):
    #Permission.objects.check_permissions(request.user, [PERMISSION_VIEW_JOB_LIST])

    trash_can = get_object_or_404(TrashCan, pk=trash_can_pk)

    context = {
        'object_list': trash_can.items.all(),
        'object': trash_can,
        'title': _(u'items in trash can: %s') % trash_can,
        'extra_columns': [
            {
                'name': _(u'date time'),
                'attribute': 'trashed_at'
            },
        ],
        'hide_link': True,
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))
        
        
def trash_can_item_restore(request, trash_can_item_pk):
    #Permission.objects.check_permissions(request.user, [PERMISSION_OCR_QUEUE_ENABLE_DISABLE])

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))

    trash_can_item = get_object_or_404(TrashCanItem, pk=trash_can_item_pk)

    if request.method == 'POST':
        try:
            trash_can_item.restore()
        except Exception, exc:
            messages.warning(request, _(u'Error restoring item; %s') % exc)
            return HttpResponseRedirect(previous)            
        else:
            messages.success(request, _(u'Item restored successfully.'))
            return HttpResponseRedirect(next)

    return render_to_response('generic_confirm.html', {
        'object': trash_can_item,
        'title': _(u'Are you sure you wish to restore trash can item: %s?') % trash_can_item,
        'next': next,
        'previous': previous,
        'form_icon': 'bin_empty.png',
    }, context_instance=RequestContext(request))
