from __future__ import absolute_import, unicode_literals

import logging

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from acls.models import AccessEntry
from acls.utils import apply_default_acls
from acls.views import acl_list_for
from common.utils import encapsulate, generate_choices_w_labels
from common.views import assign_remove
from common.widgets import two_state_template
from documents.models import Document, DocumentType
from documents.views import document_list
from permissions.models import Permission

from .forms import SmartLinkConditionForm, SmartLinkForm
from .models import SmartLink, SmartLinkCondition
from .permissions import (
    PERMISSION_SMART_LINK_CREATE, PERMISSION_SMART_LINK_DELETE,
    PERMISSION_SMART_LINK_EDIT, PERMISSION_SMART_LINK_VIEW
)

logger = logging.getLogger(__name__)


def smart_link_instance_view(request, document_id, smart_link_pk):
    document = get_object_or_404(Document, pk=document_id)
    smart_link = get_object_or_404(SmartLink, pk=smart_link_pk)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_SMART_LINK_VIEW])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_SMART_LINK_VIEW, request.user, smart_link)

    try:
        object_list = smart_link.get_linked_document_for(document)
    except Exception as exception:
        object_list = []

        if request.user.is_staff or request.user.is_superuser:
            messages.error(request, _('Smart link query error: %s' % exception))

    return document_list(
        request,
        title=_('Documents in smart link: %s') % smart_link.get_dynamic_title(document),
        object_list=object_list,
        extra_context={
            'object': document
        }
    )


def smart_link_instances_for_document(request, document_id):
    document = get_object_or_404(Document, pk=document_id)

    try:
        queryset = SmartLink.objects.get_for(document)
    except Exception as exception:
        queryset = []
        messages.error(
            request, _('Error calculating smart link for: %(document)s; %(exception)s.') %
            {'document': document, 'exception': exception}
        )

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_SMART_LINK_VIEW])
    except PermissionDenied:
        smart_links = AccessEntry.objects.filter_objects_by_access(PERMISSION_SMART_LINK_VIEW, request.user, queryset)
    else:
        smart_links = queryset

    context = {
        'document': document,
        'extra_columns': [
            {'name': _('Indentifier'), 'attribute': encapsulate(lambda resolved_smart_link: resolved_smart_link.smart_link.get_dynamic_title(document))},
            {'name': _('Documents'), 'attribute': encapsulate(lambda resolved_smart_link: resolved_smart_link.queryset.count())}
        ],
        'extra_navigation_links': {
            SmartLink: {
                None: {
                    'link': [{'text': 'asd'}]
                }
            }

        },
        'hide_object': True,
        'hide_link': True,
        'object': document,
        'object_list': smart_links,
        'title': _('Smart links for document: %s') % document,
    }

    return render_to_response('main/generic_list.html', context,
                              context_instance=RequestContext(request))


def smart_link_list(request):
    qs = SmartLink.objects.all()

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_SMART_LINK_VIEW])
    except PermissionDenied:
        qs = AccessEntry.objects.filter_objects_by_access(PERMISSION_SMART_LINK_VIEW, request.user, qs)

    return render_to_response('main/generic_list.html', {
        'title': _('Smart links'),
        'object_list': qs,
        'extra_columns': [
            {'name': _('Dynamic title'), 'attribute': 'dynamic_title'},
            {'name': _('Enabled'), 'attribute': encapsulate(lambda x: two_state_template(x.enabled))},
        ],
        'hide_link': True,
        'list_object_variable_name': 'smart_link',

    }, context_instance=RequestContext(request))


def smart_link_create(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_SMART_LINK_CREATE])

    if request.method == 'POST':
        form = SmartLinkForm(request.POST)
        if form.is_valid():
            document_group = form.save()
            apply_default_acls(document_group, request.user)
            messages.success(request, _('Smart link: %s created successfully.') % document_group)
            return HttpResponseRedirect(reverse('linking:smart_link_list'))
    else:
        form = SmartLinkForm()

    return render_to_response('main/generic_form.html', {
        'form': form,
        'title': _('Create new smart link')
    }, context_instance=RequestContext(request))


def smart_link_edit(request, smart_link_pk):
    smart_link = get_object_or_404(SmartLink, pk=smart_link_pk)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_SMART_LINK_EDIT])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_SMART_LINK_EDIT, request.user, smart_link)

    if request.method == 'POST':
        form = SmartLinkForm(request.POST, instance=smart_link)
        if form.is_valid():
            smart_link = form.save()
            messages.success(request, _('Smart link: %s edited successfully.') % smart_link)
            return HttpResponseRedirect(reverse('linking:smart_link_list'))
    else:
        form = SmartLinkForm(instance=smart_link)

    return render_to_response('main/generic_form.html', {
        'object': smart_link,
        'form': form,
        'title': _('Edit smart link: %s') % smart_link
    }, context_instance=RequestContext(request))


def smart_link_delete(request, smart_link_pk):
    smart_link = get_object_or_404(SmartLink, pk=smart_link_pk)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_SMART_LINK_DELETE])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_SMART_LINK_DELETE, request.user, smart_link)

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', reverse('main:home'))))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse('main:home'))))

    if request.method == 'POST':
        try:
            smart_link.delete()
            messages.success(request, _('Smart link: %s deleted successfully.') % smart_link)
        except Exception as exception:
            messages.error(request, _('Error deleting smart link: %(smart_link)s; %(exception)s.') % {
                'smart_link': smart_link,
                'exception': exception
            })
        return HttpResponseRedirect(next)

    return render_to_response('main/generic_confirm.html', {
        'delete_view': True,
        'object': smart_link,
        'title': _('Are you sure you wish to delete smart link: %s?') % smart_link,
        'next': next,
        'previous': previous,
    }, context_instance=RequestContext(request))


def smart_link_document_types(request, smart_link_pk):
    smart_link = get_object_or_404(SmartLink, pk=smart_link_pk)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_SMART_LINK_EDIT])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_SMART_LINK_EDIT, request.user, smart_link)

    return assign_remove(
        request,
        left_list=lambda: generate_choices_w_labels(DocumentType.objects.exclude(pk__in=smart_link.document_types.all()), display_object_type=False),
        right_list=lambda: generate_choices_w_labels(smart_link.document_types.all(), display_object_type=False),
        add_method=lambda x: smart_link.document_types.add(x),
        remove_method=lambda x: smart_link.document_types.remove(x),
        decode_content_type=True,
        extra_context={
            'main_title': _('Document type for which to enable smart link: %s') % smart_link,
            'object': smart_link,
        }
    )


def smart_link_condition_list(request, smart_link_pk):
    smart_link = get_object_or_404(SmartLink, pk=smart_link_pk)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_SMART_LINK_EDIT])
    except PermissionDenied:
        AccessEntry.objects.check_accesses([PERMISSION_SMART_LINK_EDIT], request.user, smart_link)

    return render_to_response('main/generic_list.html', {
        'title': _('Conditions for smart link: %s') % smart_link,
        'object_list': smart_link.conditions.all(),
        'extra_columns': [
            {'name': _('Enabled'), 'attribute': encapsulate(lambda x: two_state_template(x.enabled))},
        ],
        'hide_link': True,
        'object': smart_link,
        'list_object_variable_name': 'condition',
    }, context_instance=RequestContext(request))


def smart_link_condition_create(request, smart_link_pk):
    smart_link = get_object_or_404(SmartLink, pk=smart_link_pk)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_SMART_LINK_EDIT])
    except PermissionDenied:
        AccessEntry.objects.check_accesses([PERMISSION_SMART_LINK_EDIT], request.user, smart_link)

    if request.method == 'POST':
        form = SmartLinkConditionForm(data=request.POST)
        if form.is_valid():
            new_smart_link_condition = form.save(commit=False)
            new_smart_link_condition.smart_link = smart_link
            new_smart_link_condition.save()
            messages.success(request, _('Smart link condition: "%s" created successfully.') % new_smart_link_condition)
            return HttpResponseRedirect(reverse('linking:smart_link_condition_list', args=[smart_link.pk]))
    else:
        form = SmartLinkConditionForm()

    return render_to_response('main/generic_form.html', {
        'form': form,
        'title': _('Add new conditions to smart link: "%s"') % smart_link,
        'object': smart_link,
    }, context_instance=RequestContext(request))


def smart_link_condition_edit(request, smart_link_condition_pk):
    smart_link_condition = get_object_or_404(SmartLinkCondition, pk=smart_link_condition_pk)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_SMART_LINK_EDIT])
    except PermissionDenied:
        AccessEntry.objects.check_accesses([PERMISSION_SMART_LINK_EDIT], request.user, smart_link_condition.smart_link)

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', reverse('main:home'))))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse('main:home'))))

    if request.method == 'POST':
        form = SmartLinkConditionForm(request.POST, instance=smart_link_condition)
        if form.is_valid():
            smart_link_condition = form.save()
            messages.success(request, _('Smart link condition: "%s" edited successfully.') % smart_link_condition)
            return HttpResponseRedirect(next)
    else:
        form = SmartLinkConditionForm(instance=smart_link_condition)

    return render_to_response('main/generic_form.html', {
        'form': form,
        'title': _('Edit smart link condition'),
        'next': next,
        'previous': previous,
        'condition': smart_link_condition,
        'object': smart_link_condition.smart_link,
        'navigation_object_list': [
            {'object': 'object', 'name': _('Smart link')},
            {'object': 'condition', 'name': _('Condition')}
        ],

    }, context_instance=RequestContext(request))


def smart_link_condition_delete(request, smart_link_condition_pk):
    smart_link_condition = get_object_or_404(SmartLinkCondition, pk=smart_link_condition_pk)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_SMART_LINK_EDIT])
    except PermissionDenied:
        AccessEntry.objects.check_accesses([PERMISSION_SMART_LINK_EDIT], request.user, smart_link_condition.smart_link)

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', reverse('main:home'))))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse('main:home'))))

    if request.method == 'POST':
        try:
            smart_link_condition.delete()
            messages.success(request, _('Smart link condition: "%s" deleted successfully.') % smart_link_condition)
        except Exception as exception:
            messages.error(request, _('Error deleting smart link condition: %(smart_link_condition)s; %(exception)s.') % {
                'smart_link_condition': smart_link_condition,
                'exception': exception
            })
        return HttpResponseRedirect(next)

    return render_to_response('main/generic_confirm.html', {
        'delete_view': True,
        'condition': smart_link_condition,
        'object': smart_link_condition.smart_link,
        'navigation_object_list': [
            {'object': 'object', 'name': _('Smart link')},
            {'object': 'condition', 'name': _('Condition')}
        ],
        'title': _('Are you sure you wish to delete smart link condition: "%s"?') % smart_link_condition,
        'next': next,
        'previous': previous,
    }, context_instance=RequestContext(request))


def smart_link_acl_list(request, smart_link_pk):
    smart_link = get_object_or_404(SmartLink, pk=smart_link_pk)
    logger.debug('smart_link: %s', smart_link)

    return acl_list_for(
        request,
        smart_link,
        extra_context={
            'object': smart_link,
            'smart_link': smart_link,
        }
    )
