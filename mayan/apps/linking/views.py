from __future__ import absolute_import, unicode_literals

import logging

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from acls.models import AccessControlList
from common.utils import encapsulate
from common.views import AssignRemoveView, SingleObjectListView
from common.widgets import two_state_template
from documents.models import Document, DocumentType
from documents.permissions import permission_document_view
from documents.views import DocumentListView
from permissions import Permission

from .forms import SmartLinkConditionForm, SmartLinkForm
from .models import ResolvedSmartLink, SmartLink, SmartLinkCondition
from .permissions import (
    permission_smart_link_create, permission_smart_link_delete,
    permission_smart_link_edit, permission_smart_link_view
)

logger = logging.getLogger(__name__)


class SetupSmartLinkDocumentTypesView(AssignRemoveView):
    decode_content_type = True
    left_list_title = _('Available document types')
    right_list_title = _('Document types enabled')
    object_permission = permission_smart_link_edit

    def add(self, item):
        self.get_object().document_types.add(item)

    def get_object(self):
        return get_object_or_404(SmartLink, pk=self.kwargs['pk'])

    def left_list(self):
        return AssignRemoveView.generate_choices(
            DocumentType.objects.exclude(
                pk__in=self.get_object().document_types.all()
            )
        )

    def right_list(self):
        return AssignRemoveView.generate_choices(
            self.get_object().document_types.all()
        )

    def remove(self, item):
        self.get_object().document_types.remove(item)

    def get_context_data(self, **kwargs):
        data = super(
            SetupSmartLinkDocumentTypesView, self
        ).get_context_data(**kwargs)
        data.update({
            'object': self.get_object(),
            'title': _(
                'Document type for which to enable smart link: %s'
            ) % self.get_object(),
        })

        return data


class ResolvedSmartLinkView(DocumentListView):
    def dispatch(self, request, *args, **kwargs):
        self.document = get_object_or_404(
            Document, pk=self.kwargs['document_pk']
        )
        self.smart_link = get_object_or_404(
            SmartLink, pk=self.kwargs['smart_link_pk']
        )

        try:
            Permission.check_permissions(
                request.user, [permission_document_view]
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_document_view, request.user, self.document
            )

        try:
            Permission.check_permissions(
                request.user, [permission_smart_link_view]
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_smart_link_view, request.user, self.smart_link
            )

        return super(
            ResolvedSmartLinkView, self
        ).dispatch(request, *args, **kwargs)

    def get_document_queryset(self):
        try:
            queryset = self.smart_link.get_linked_document_for(self.document)
        except Exception as exception:
            queryset = Document.objects.none()

            if self.request.user.is_staff or self.request.user.is_superuser:
                messages.error(
                    self.request, _('Smart link query error: %s' % exception)
                )

        return queryset

    def get_extra_context(self):
        return {
            'hide_links': True,
            'object': self.document,
            'title': _(
                'Documents in smart link "%(smart_link)s" as relation to '
                '"%(document)s"'
            ) % {
                'document': self.document,
                'smart_link': self.smart_link.get_dynamic_label(self.document),
            }
        }


class SmartLinkListView(SingleObjectListView):
    object_permission = permission_smart_link_view

    def get_queryset(self):
        self.queryset = self.get_smart_link_queryset()
        return super(SmartLinkListView, self).get_queryset()

    def get_smart_link_queryset(self):
        return SmartLink.objects.all()

    def get_extra_context(self):
        return {
            'extra_columns': [
                {'name': _('Dynamic label'), 'attribute': 'dynamic_label'},
                {
                    'name': _('Enabled'), 'attribute': encapsulate(
                        lambda instance: two_state_template(instance.enabled)
                    )
                },
            ],
            'hide_link': True,
            'title': _('Smart links'),
        }


class DocumentSmartLinkListView(SmartLinkListView):
    def dispatch(self, request, *args, **kwargs):
        self.document = get_object_or_404(Document, pk=self.kwargs['pk'])

        try:
            Permission.check_permissions(
                request.user, (permission_document_view,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_permissions(
                permission_document_view, request.user, self.document
            )

        return super(
            DocumentSmartLinkListView, self
        ).dispatch(request, *args, **kwargs)

    def get_smart_link_queryset(self):
        return ResolvedSmartLink.objects.filter(
            document_types=self.document.document_type, enabled=True
        )

    def get_extra_context(self):
        return {
            'document': self.document,
            'extra_columns': (
                {
                    'name': _('Label'), 'attribute': encapsulate(
                        lambda smart_link: smart_link.get_dynamic_label(
                            self.document
                        )
                    )
                },
            ),
            'hide_object': True,
            'hide_link': True,
            'object': self.document,
            'title': _('Smart links for document: %s') % self.document,
        }


def smart_link_create(request):
    Permission.check_permissions(
        request.user, [permission_smart_link_create]
    )

    if request.method == 'POST':
        form = SmartLinkForm(request.POST)
        if form.is_valid():
            document_group = form.save()
            messages.success(
                request, _(
                    'Smart link: %s created successfully.'
                ) % document_group
            )
            return HttpResponseRedirect(reverse('linking:smart_link_list'))
    else:
        form = SmartLinkForm()

    return render_to_response('appearance/generic_form.html', {
        'form': form,
        'title': _('Create new smart link')
    }, context_instance=RequestContext(request))


def smart_link_edit(request, smart_link_pk):
    smart_link = get_object_or_404(SmartLink, pk=smart_link_pk)

    try:
        Permission.check_permissions(
            request.user, [permission_smart_link_edit]
        )
    except PermissionDenied:
        AccessControlList.objects.check_access(
            permission_smart_link_edit, request.user, smart_link
        )

    if request.method == 'POST':
        form = SmartLinkForm(request.POST, instance=smart_link)
        if form.is_valid():
            smart_link = form.save()
            messages.success(
                request, _(
                    'Smart link: %s edited successfully.'
                ) % smart_link
            )
            return HttpResponseRedirect(reverse('linking:smart_link_list'))
    else:
        form = SmartLinkForm(instance=smart_link)

    return render_to_response('appearance/generic_form.html', {
        'object': smart_link,
        'form': form,
        'title': _('Edit smart link: %s') % smart_link
    }, context_instance=RequestContext(request))


def smart_link_delete(request, smart_link_pk):
    smart_link = get_object_or_404(SmartLink, pk=smart_link_pk)

    try:
        Permission.check_permissions(
            request.user, [permission_smart_link_delete]
        )
    except PermissionDenied:
        AccessControlList.objects.check_access(
            permission_smart_link_delete, request.user, smart_link
        )

    next = request.POST.get(
        'next', request.GET.get('next', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)))
    )
    previous = request.POST.get(
        'previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)))
    )

    if request.method == 'POST':
        try:
            smart_link.delete()
            messages.success(
                request, _(
                    'Smart link: %s deleted successfully.'
                ) % smart_link
            )
        except Exception as exception:
            messages.error(
                request, _(
                    'Error deleting smart link: %(smart_link)s; '
                    '%(exception)s.'
                ) % {
                    'smart_link': smart_link,
                    'exception': exception
                }
            )
        return HttpResponseRedirect(next)

    return render_to_response('appearance/generic_confirm.html', {
        'delete_view': True,
        'object': smart_link,
        'title': _('Delete smart link: %s?') % smart_link,
        'next': next,
        'previous': previous,
    }, context_instance=RequestContext(request))


def smart_link_condition_list(request, smart_link_pk):
    smart_link = get_object_or_404(SmartLink, pk=smart_link_pk)

    try:
        Permission.check_permissions(
            request.user, [permission_smart_link_edit]
        )
    except PermissionDenied:
        AccessControlList.objects.check_access(
            [permission_smart_link_edit], request.user, smart_link
        )

    return render_to_response('appearance/generic_list.html', {
        'title': _('Conditions for smart link: %s') % smart_link,
        'object_list': smart_link.conditions.all(),
        'extra_columns': [
            {
                'name': _('Enabled'),
                'attribute': encapsulate(
                    lambda x: two_state_template(x.enabled)
                )
            },
        ],
        'hide_link': True,
        'object': smart_link,
    }, context_instance=RequestContext(request))


def smart_link_condition_create(request, smart_link_pk):
    smart_link = get_object_or_404(SmartLink, pk=smart_link_pk)

    try:
        Permission.check_permissions(
            request.user, [permission_smart_link_edit]
        )
    except PermissionDenied:
        AccessControlList.objects.check_access(
            [permission_smart_link_edit], request.user, smart_link
        )

    if request.method == 'POST':
        form = SmartLinkConditionForm(data=request.POST)
        if form.is_valid():
            new_smart_link_condition = form.save(commit=False)
            new_smart_link_condition.smart_link = smart_link
            new_smart_link_condition.save()
            messages.success(
                request, _(
                    'Smart link condition: "%s" created successfully.'
                ) % new_smart_link_condition
            )
            return HttpResponseRedirect(
                reverse(
                    'linking:smart_link_condition_list', args=[smart_link.pk]
                )
            )
    else:
        form = SmartLinkConditionForm()

    return render_to_response('appearance/generic_form.html', {
        'form': form,
        'title': _('Add new conditions to smart link: "%s"') % smart_link,
        'object': smart_link,
    }, context_instance=RequestContext(request))


def smart_link_condition_edit(request, smart_link_condition_pk):
    smart_link_condition = get_object_or_404(
        SmartLinkCondition, pk=smart_link_condition_pk
    )

    try:
        Permission.check_permissions(
            request.user, [permission_smart_link_edit]
        )
    except PermissionDenied:
        AccessControlList.objects.check_access(
            [permission_smart_link_edit], request.user,
            smart_link_condition.smart_link
        )

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    if request.method == 'POST':
        form = SmartLinkConditionForm(
            request.POST, instance=smart_link_condition
        )
        if form.is_valid():
            smart_link_condition = form.save()
            messages.success(
                request, _(
                    'Smart link condition: "%s" edited successfully.'
                ) % smart_link_condition
            )
            return HttpResponseRedirect(next)
    else:
        form = SmartLinkConditionForm(instance=smart_link_condition)

    return render_to_response('appearance/generic_form.html', {
        'condition': smart_link_condition,
        'form': form,
        'navigation_object_list': ['object', 'condition'],
        'next': next,
        'object': smart_link_condition.smart_link,
        'previous': previous,
        'title': _('Edit smart link condition'),
    }, context_instance=RequestContext(request))


def smart_link_condition_delete(request, smart_link_condition_pk):
    smart_link_condition = get_object_or_404(
        SmartLinkCondition, pk=smart_link_condition_pk
    )

    try:
        Permission.check_permissions(request.user, [permission_smart_link_edit])
    except PermissionDenied:
        AccessControlList.objects.check_access(
            [permission_smart_link_edit], request.user,
            smart_link_condition.smart_link
        )

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    if request.method == 'POST':
        try:
            smart_link_condition.delete()
            messages.success(
                request, _(
                    'Smart link condition: "%s" deleted successfully.'
                ) % smart_link_condition
            )
        except Exception as exception:
            messages.error(
                request, _(
                    'Error deleting smart link condition: '
                    '%(smart_link_condition)s; %(exception)s.'
                ) % {
                    'smart_link_condition': smart_link_condition,
                    'exception': exception
                }
            )
        return HttpResponseRedirect(next)

    return render_to_response('appearance/generic_confirm.html', {
        'condition': smart_link_condition,
        'delete_view': True,
        'navigation_object_list': ['object', 'condition'],
        'next': next,
        'object': smart_link_condition.smart_link,
        'previous': previous,
        'title': _('Delete smart link condition: "%s"?') % smart_link_condition,
    }, context_instance=RequestContext(request))
