from __future__ import absolute_import, unicode_literals

import itertools
import logging

from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.views import (
    AssignRemoveView, SingleObjectCreateView, SingleObjectDeleteView,
    SingleObjectListView
)
from mayan.apps.permissions import Permission, PermissionNamespace
from mayan.apps.permissions.models import Role, StoredPermission

from .classes import ModelPermission
from .forms import ACLCreateForm
from .icons import icon_acl_list
from .links import link_acl_create
from .models import AccessControlList
from .permissions import permission_acl_edit, permission_acl_view

logger = logging.getLogger(__name__)


class ACLCreateView(SingleObjectCreateView):
    form_class = ACLCreateForm
    model = AccessControlList

    def dispatch(self, request, *args, **kwargs):
        self.object_content_type = get_object_or_404(
            klass=ContentType, app_label=self.kwargs['app_label'],
            model=self.kwargs['model']
        )

        try:
            self.content_object = self.object_content_type.get_object_for_this_type(
                pk=self.kwargs['object_id']
            )
        except self.object_content_type.model_class().DoesNotExist:
            raise Http404

        AccessControlList.objects.check_access(
            permissions=permission_acl_edit, user=request.user,
            obj=self.content_object
        )

        return super(ACLCreateView, self).dispatch(request, *args, **kwargs)

    def get_instance_extra_data(self):
        return {
            'content_object': self.content_object
        }

    def get_extra_context(self):
        return {
            'object': self.content_object,
            'title': _(
                'New access control lists for: %s'
            ) % self.content_object
        }

    def get_form_extra_kwargs(self):
        acls = AccessControlList.objects.filter(
            content_type=self.content_type, object_id=self.content_object.pk
        )

        return {
            'queryset': Role.objects.exclude(
                pk__in=acls.values('role')
            ),
            'user': self.request.user
        }

    def get_success_url(self):
        return self.object.get_absolute_url()


class ACLDeleteView(SingleObjectDeleteView):
    model = AccessControlList

    def dispatch(self, request, *args, **kwargs):
        acl = get_object_or_404(klass=AccessControlList, pk=self.kwargs['pk'])

        AccessControlList.objects.check_access(
            permissions=permission_acl_edit, user=request.user,
            obj=acl.content_object
        )

        return super(ACLDeleteView, self).dispatch(request, *args, **kwargs)

    def get_extra_context(self):
        return {
            'object': self.get_object().content_object,
            'title': _('Delete ACL: %s') % self.get_object(),
        }

    def get_post_action_redirect(self):
        instance = self.get_object()
        return reverse(
            viewname='acls:acl_list', kwargs={
                'app_label': instance.content_type.app_label,
                'model': instance.content_type.model,
                'object_id': instance.object_id
            }
        )


class ACLListView(SingleObjectListView):
    def dispatch(self, request, *args, **kwargs):
        self.object_content_type = get_object_or_404(
            klass=ContentType, app_label=self.kwargs['app_label'],
            model=self.kwargs['model']
        )

        try:
            self.content_object = self.object_content_type.get_object_for_this_type(
                pk=self.kwargs['object_id']
            )
        except self.object_content_type.model_class().DoesNotExist:
            raise Http404

        AccessControlList.objects.check_access(
            permissions=permission_acl_view, user=request.user,
            obj=self.content_object
        )

        return super(ACLListView, self).dispatch(request, *args, **kwargs)

    def get_extra_context(self):
        return {
            'hide_object': True,
            'no_results_icon': icon_acl_list,
            'no_results_main_link': link_acl_create.resolve(
                context=RequestContext(
                    self.request, {'resolved_object': self.content_object}
                )
            ),
            'no_results_title': _(
                'There are no ACLs for this object'
            ),
            'no_results_text': _(
                'ACL stands for Access Control List and is a precise method '
                ' to control user access to objects in the system.'
            ),
            'object': self.content_object,
            'title': _('Access control lists for: %s' % self.content_object),
        }

    def get_object_list(self):
        return AccessControlList.objects.filter(
            content_type=self.object_content_type,
            object_id=self.content_object.pk
        )


class ACLPermissionsView(AssignRemoveView):
    grouped = True
    left_list_title = _('Available permissions')
    right_list_title = _('Granted permissions')

    @staticmethod
    def generate_choices(entries):
        results = []

        # Sort permissions by their translatable label
        entries = sorted(
            entries, key=lambda permission: permission.volatile_permission.label
        )

        # Group permissions by namespace
        for namespace, permissions in itertools.groupby(entries, lambda entry: entry.namespace):
            permission_options = [
                (force_text(permission.pk), permission) for permission in permissions
            ]
            results.append(
                (PermissionNamespace.get(name=namespace), permission_options)
            )

        return results

    def add(self, item):
        permission = get_object_or_404(klass=StoredPermission, pk=item)
        self.get_object().permissions.add(permission)

    def dispatch(self, request, *args, **kwargs):
        acl = get_object_or_404(klass=AccessControlList, pk=self.kwargs['pk'])

        AccessControlList.objects.check_access(
            permissions=permission_acl_edit, user=request.user,
            obj=acl.content_object
        )

        return super(
            ACLPermissionsView, self
        ).dispatch(request, *args, **kwargs)

    def get_available_list(self):
        return ModelPermission.get_for_instance(
            instance=self.get_object().content_object
        ).exclude(id__in=self.get_granted_list().values_list('pk', flat=True))

    def get_disabled_choices(self):
        """
        Get permissions from a parent's acls but remove the permissions we
        already hold for this object
        """
        return map(
            str, set(
                self.get_object().get_inherited_permissions().values_list(
                    'pk', flat=True
                )
            ).difference(
                self.get_object().permissions.values_list('pk', flat=True)
            )
        )

    def get_extra_context(self):
        return {
            'object': self.get_object().content_object,
            'title': _('Role "%(role)s" permission\'s for "%(object)s"') % {
                'role': self.get_object().role,
                'object': self.get_object().content_object,
            },
        }

    def get_granted_list(self):
        """
        Merge or permissions we hold for this object and the permissions we
        hold for this object's parent via another ACL
        """
        merged_pks = self.get_object().permissions.values_list('pk', flat=True) | self.get_object().get_inherited_permissions().values_list('pk', flat=True)
        return StoredPermission.objects.filter(pk__in=merged_pks)

    def get_object(self):
        return get_object_or_404(klass=AccessControlList, pk=self.kwargs['pk'])

    def get_right_list_help_text(self):
        if self.get_object().get_inherited_permissions():
            return _(
                'Disabled permissions are inherited from a parent object.'
            )

        return None

    def left_list(self):
        Permission.refresh()
        return ACLPermissionsView.generate_choices(self.get_available_list())

    def remove(self, item):
        permission = get_object_or_404(klass=StoredPermission, pk=item)
        self.get_object().permissions.remove(permission)

    def right_list(self):
        return ACLPermissionsView.generate_choices(self.get_granted_list())
