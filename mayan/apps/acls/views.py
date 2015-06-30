from __future__ import absolute_import, unicode_literals

import itertools
import logging

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from common.utils import encapsulate
from common.views import (
    AssignRemoveView, SingleObjectCreateView, SingleObjectDeleteView,
    SingleObjectListView
)
from permissions import Permission, PermissionNamespace
from permissions.models import StoredPermission

from .models import AccessControlList
from .permissions import permission_acl_edit, permission_acl_view

logger = logging.getLogger(__name__)


def _permission_titles(permission_list):
    return ', '.join([unicode(permission) for permission in permission_list])


class ACLListView(SingleObjectListView):
    def dispatch(self, request, *args, **kwargs):
        self.content_type = get_object_or_404(ContentType, app_label=self.kwargs['app_label'], model=self.kwargs['model'])

        try:
            self.content_object = self.content_type.get_object_for_this_type(pk=self.kwargs['object_id'])
        except self.content_type.model_class().DoesNotExist:
            raise Http404

        try:
            Permission.check_permissions(request.user, permissions=(permission_acl_view,))
        except PermissionDenied:
            AccessControlList.objects.check_access(permission_acl_view, request.user, self.content_object)

        return super(ACLListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return AccessControlList.objects.filter(content_type=self.content_type, object_id=self.content_object.pk)

    def get_context_data(self, **kwargs):
        context = super(ACLListView, self).get_context_data(**kwargs)
        context.update(
            {
                'hide_object': True,
                'object': self.content_object,
                'title': _('Access control lists for: %s' % self.content_object),
                'extra_columns': [
                    {
                        'name': _('Role'),
                        'attribute': 'role'
                    },
                    {
                        'name': _('Permissions'),
                        'attribute': encapsulate(lambda x: _permission_titles(x.permissions.all()))
                    },
                ],
            }
        )

        return context


class ACLCreateView(SingleObjectCreateView):
    model = AccessControlList
    fields = ('role',)

    def dispatch(self, request, *args, **kwargs):
        content_type = get_object_or_404(ContentType, app_label=self.kwargs['app_label'], model=self.kwargs['model'])

        try:
            self.content_object = content_type.get_object_for_this_type(pk=self.kwargs['object_id'])
        except content_type.model_class().DoesNotExist:
            raise Http404

        try:
            Permission.check_permissions(request.user, permissions=(permission_acl_edit,))
        except PermissionDenied:
            AccessControlList.objects.check_access(permission_acl_edit, request.user, self.content_object)

        return super(ACLCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.content_object = self.content_object
        instance.save()

        return super(ACLCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ACLCreateView, self).get_context_data(**kwargs)
        context.update(
            {
                'object': self.content_object,
                'title': _('New access control lists for: %s' % self.content_object),
            }
        )

        return context


class ACLDeleteView(SingleObjectDeleteView):
    model = AccessControlList
    object_permission = permission_acl_edit

    def get_context_data(self, **kwargs):
        context = super(ACLDeleteView, self).get_context_data(**kwargs)
        context.update(
            {
                'object': self.get_object().content_object,
            }
        )

        return context


class ACLPermissionsView(AssignRemoveView):
    grouped = True
    object_permission = permission_acl_edit
    left_list_title = _('Available permissions')
    right_list_title = _('Granted permissions')

    def add(self, item):
        permission = get_object_or_404(StoredPermission, pk=item)
        self.get_object().permissions.add(permission)

    def get_object(self):
        return get_object_or_404(AccessControlList, pk=self.kwargs['pk'])

    def left_list(self):
        results = []
        for namespace, permissions in itertools.groupby(StoredPermission.objects.exclude(id__in=self.get_object().permissions.values_list('pk', flat=True)), lambda entry: entry.namespace):
            permission_options = [(unicode(permission.pk), permission) for permission in permissions]
            results.append((PermissionNamespace.get(namespace), permission_options))

        return results

    def right_list(self):
        results = []
        for namespace, permissions in itertools.groupby(self.get_object().permissions.all(), lambda entry: entry.namespace):
            permission_options = [(unicode(permission.pk), permission) for permission in permissions]
            results.append((PermissionNamespace.get(namespace), permission_options))

        return results

    def get_context_data(self, **kwargs):
        context = super(ACLPermissionsView, self).get_context_data(**kwargs)
        context.update(
            {
                'object': self.get_object().content_object,
                'title': _('Role "%(role)s" permission\'s for "%(object)s"') % {
                    'role': self.get_object().role,
                    'object': self.get_object().content_object,
                }
            }
        )
        return context

    def remove(self, item):
        permission = get_object_or_404(StoredPermission, pk=item)
        self.get_object().permissions.remove(permission)
