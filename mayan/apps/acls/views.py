import logging

from django.template import RequestContext
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.generics import (
    AddRemoveView, SingleObjectCreateView, SingleObjectDeleteView,
    SingleObjectListView
)
from mayan.apps.common.mixins import (
    ContentTypeViewMixin, ExternalObjectMixin
)
from mayan.apps.permissions.models import Role

from .classes import ModelPermission
from .forms import ACLCreateForm
from .icons import icon_acl_list
from .links import link_acl_create
from .models import AccessControlList
from .permissions import permission_acl_edit, permission_acl_view

logger = logging.getLogger(name=__name__)


class ACLCreateView(
    ContentTypeViewMixin, ExternalObjectMixin, SingleObjectCreateView
):
    content_type_url_kw_args = {
        'app_label': 'app_label',
        'model_name': 'model_name'
    }
    external_object_permission = permission_acl_edit
    external_object_pk_url_kwarg = 'object_id'
    form_class = ACLCreateForm

    def get_error_message_duplicate(self):
        return _(
            'An ACL for "%(object)s" using role "%(role)s" already exists. '
            'Edit that ACL entry instead.'
        ) % {'object': self.get_external_object(), 'role': self.object.role}

    def get_external_object_queryset(self):
        # Here we get a queryset the object model for which an ACL will be
        # created.
        return self.get_content_type().get_all_objects_for_this_type()

    def get_extra_context(self):
        return {
            'object': self.external_object,
            'title': _(
                'New access control lists for: %s'
            ) % self.external_object
        }

    def get_form_extra_kwargs(self):
        try:
            roles = self.external_object.acls.values('role')
        except AttributeError:
            # Fallback when attempting to access the ACLs generic relation
            # field of models that have not been registered.
            roles = Role.objects.none()

        return {
            'field_name': 'role',
            'label': _('Role'),
            'queryset': Role.objects.exclude(pk__in=roles),
            'widget_attributes': {'class': 'select2'},
            'user': self.request.user
        }

    def get_instance_extra_data(self):
        return {
            'content_object': self.external_object
        }

    def get_queryset(self):
        self.external_object.acls.all()

    def get_success_url(self):
        return self.object.get_absolute_url()


class ACLDeleteView(SingleObjectDeleteView):
    model = AccessControlList
    object_permission = permission_acl_edit
    pk_url_kwarg = 'acl_id'

    def get_extra_context(self):
        return {
            'acl': self.object,
            'navigation_object_list': ('object', 'acl'),
            'object': self.object.content_object,
            'title': _('Delete ACL: %s') % self.object,
        }

    def get_post_action_redirect(self):
        return reverse(
            viewname='acls:acl_list', kwargs={
                'app_label': self.object.content_type.app_label,
                'model_name': self.object.content_type.model,
                'object_id': self.object.object_id
            }
        )


class ACLListView(ContentTypeViewMixin, ExternalObjectMixin, SingleObjectListView):
    content_type_url_kw_args = {
        'app_label': 'app_label',
        'model_name': 'model_name'
    }
    external_object_permission = permission_acl_view
    external_object_pk_url_kwarg = 'object_id'

    def get_external_object_queryset(self):
        # Here we get a queryset the object model for which an ACL will be
        # created.
        return self.get_content_type().get_all_objects_for_this_type()

    def get_extra_context(self):
        return {
            'hide_object': True,
            'no_results_icon': icon_acl_list,
            'no_results_main_link': link_acl_create.resolve(
                context=RequestContext(
                    self.request, {
                        'resolved_object': self.external_object
                    }
                )
            ),
            'no_results_title': _(
                'There are no ACLs for this object'
            ),
            'no_results_text': _(
                'ACL stands for Access Control List and is a precise method '
                'to control user access to objects in the system. ACLs '
                'allow granting a permission to a role but only for a '
                'specific object or set of objects.'
            ),
            'object': self.external_object,
            'title': _(
                'Access control lists for: %s' % self.external_object
            ),
        }

    def get_source_queryset(self):
        return self.external_object.acls.all()


class ACLPermissionsView(AddRemoveView):
    main_object_method_add = 'permissions_add'
    main_object_method_remove = 'permissions_remove'
    main_object_model = AccessControlList
    main_object_permission = permission_acl_edit
    main_object_pk_url_kwarg = 'acl_id'
    list_added_title = _('Granted permissions')
    list_available_title = _('Available permissions')
    related_field = 'permissions'

    def generate_choices(self, queryset):
        namespaces_dictionary = {}

        # Sort permissions by their translatable label
        object_list = sorted(
            queryset,
            key=lambda permission: permission.volatile_permission.label
        )

        # Group permissions by namespace
        for permission in object_list:
            namespaces_dictionary.setdefault(
                permission.volatile_permission.namespace.label,
                []
            )
            namespaces_dictionary[
                permission.volatile_permission.namespace.label
            ].append(
                (permission.pk, force_text(s=permission))
            )

        # Sort permissions by their translatable namespace label
        return sorted(namespaces_dictionary.items())

    def get_actions_extra_kwargs(self):
        return {'_user': self.request.user}

    def get_disabled_choices(self):
        """
        Get permissions from a parent's ACLs or directly granted to the role.
        We return a list since that is what the form widget's can process.
        """
        return self.main_object.get_inherited_permissions().values_list(
            'pk', flat=True
        )

    def get_extra_context(self):
        return {
            'acl': self.main_object,
            'object': self.main_object.content_object,
            'navigation_object_list': ('object', 'acl'),
            'title': _('Role "%(role)s" permission\'s for "%(object)s".') % {
                'role': self.main_object.role,
                'object': self.main_object.content_object,
            }
        }

    def get_list_added_help_text(self):
        if self.main_object.get_inherited_permissions():
            return _(
                'Disabled permissions are inherited from a parent object or '
                'directly granted to the role and can\'t be removed from this '
                'view. Inherited permissions need to be removed from the '
                'parent object\'s ACL or from them role via the Setup menu.'
            )
        else:
            return super(ACLPermissionsView, self).get_list_added_help_text()

    def get_list_added_queryset(self):
        """
        Merge of permissions we hold for this object and the permissions we
        hold for this object's parents via another ACL. .distinct() is added
        in case the permission was added to the ACL and then added to a
        parent ACL's and thus inherited and would appear twice. If
        order to remove the double permission from the ACL it would need to be
        remove from the parent first to enable the choice in the form,
        remove it from the ACL and then re-add it to the parent ACL.
        """
        queryset_acl = super(ACLPermissionsView, self).get_list_added_queryset()

        return (
            queryset_acl | self.main_object.get_inherited_permissions()
        ).distinct()

    def get_secondary_object_source_queryset(self):
        return ModelPermission.get_for_instance(
            instance=self.main_object.content_object
        )
