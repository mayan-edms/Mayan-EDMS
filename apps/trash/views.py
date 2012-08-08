from __future__ import absolute_import

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
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
        'list_object_variable_name': 'trash_can',
        'title': _(u'trash cans'),
        'extra_columns': [
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
        'trash_can': trash_can,
        'list_object_variable_name': 'trash_can_item',
        'navigation_object_name': 'trash_can',
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

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))

    trash_can_item = get_object_or_404(TrashCanItem, pk=trash_can_item_pk)

    if request.method == 'POST':
        try:
            trash_can_item.restore()
        except Exception, exc:
            messages.warning(request, _(u'Error restoring trash can item; %s') % exc)
            return HttpResponseRedirect(previous)            
        else:
            messages.success(request, _(u'Trash can item "%s" restored successfully.') % trash_can_item)
            return HttpResponseRedirect(reverse('trash_can_items', args=[trash_can_item.trash_can.pk]))

    return render_to_response('generic_confirm.html', {
        'trash_can': trash_can_item.trash_can,
        'trash_can_item': trash_can_item,
        'navigation_object_list': [
            {'object': 'trash_can', 'name': _(u'trash can')},
            {'object': 'trash_can_item', 'name': _(u'trash can item')},
        ],        
        'title': _(u'Are you sure you wish to restore trash can item: %s?') % trash_can_item,
        'previous': previous,
        'form_icon': 'bin_empty.png',
    }, context_instance=RequestContext(request))


def trash_can_item_delete(request, trash_can_item_pk):
    #Permission.objects.check_permissions(request.user, [PERMISSION_OCR_QUEUE_ENABLE_DISABLE])

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))

    trash_can_item = get_object_or_404(TrashCanItem, pk=trash_can_item_pk)

    if request.method == 'POST':
        try:
            trash_can_item.purge()
        except Exception, exc:
            messages.warning(request, _(u'Error deleting trash can item; %s') % exc)
            return HttpResponseRedirect(previous)            
        else:
            messages.success(request, _(u'Trash can item deleted successfully.') % trash_can_item)
            return HttpResponseRedirect(reverse('trash_can_items', args=[trash_can_item.trash_can.pk]))

    return render_to_response('generic_confirm.html', {
        'trash_can': trash_can_item.trash_can,
        'trash_can_item': trash_can_item,
        'navigation_object_list': [
            {'object': 'trash_can', 'name': _(u'trash can')},
            {'object': 'trash_can_item', 'name': _(u'trash can item')},
        ],        
        'title': _(u'Are you sure you wish to delete trash can item: %s?') % trash_can_item,
        'previous': previous,
        'form_icon': 'delete.png',
    }, context_instance=RequestContext(request))
