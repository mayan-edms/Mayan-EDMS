from __future__ import absolute_import, unicode_literals

import logging

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from acls.models import AccessControlList
from document_states.classes import WorkflowAction
from permissions.classes import Permission
from permissions.models import Role

from .classes import ModelPermission
from .permissions import permission_acl_edit

__all__ = ('GrantAccessAction',)
logger = logging.getLogger(__name__)


class GrantAccessAction(WorkflowAction):
    fields = (
        {
            'name': 'content_type', 'label': _('Object type'),
            'class': 'django.forms.ModelChoiceField', 'kwargs': {
                'help_text': _(
                    'Type of the object for which the access will be granted.'
                ),
                'queryset': ModelPermission.get_classes(as_content_type=True),
                'required': True
            }
        }, {
            'name': 'object_id', 'label': _('Object ID'),
            'class': 'django.forms.IntegerField', 'kwargs': {
                'help_text': _(
                    'Numeric identifier of the object for which the access '
                    'will be granted.'
                ), 'required': True
            }
        }, {
            'name': 'roles', 'label': _('Roles'),
            'class': 'django.forms.ModelMultipleChoiceField', 'kwargs': {
                'help_text': _('Roles that will be granted access.'),
                'queryset': Role.objects.all(), 'required': True
            }
        }, {
            'name': 'permissions', 'label': _('Permissions'),
            'class': 'django.forms.MultipleChoiceField', 'kwargs': {
                'help_text': _(
                    'Permissions to grant to the role for the object.'
                ), 'choices': Permission.all(as_choices=True),
                'required': True
            }
        },
    )
    label = _('Grant access')
    widgets = {
        'roles': {
            'class': 'django.forms.widgets.SelectMultiple', 'kwargs': {
                'attrs': {'class': 'select2'},
            }
        },
        'permissions': {
            'class': 'django.forms.widgets.SelectMultiple', 'kwargs': {
                'attrs': {'class': 'select2'},
            }
        }
    }

    @classmethod
    def clean(cls, request, form_data=None):
        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )

        content_type = ContentType.objects.get(
            pk=int(form_data['action_data']['content_type'])
        )
        obj = content_type.get_object_for_this_type(
            pk=int(form_data['action_data']['object_id'])
        )

        try:
            AccessControlList.objects.check_access(
                permissions=permission_acl_edit, user=request.user, obj=obj
            )
        except Exception as exception:
            raise ValidationError(exception)
        else:
            return form_data

    def execute(self, context):
        content_type = ContentType.objects.get(
            pk=self.form_data['content_type']
        )
        obj = content_type.get_object_for_this_type(
            pk=self.form_data['object_id']
        )
        roles = Role.objects.filter(pk__in=self.form_data['roles'])
        permissions = [Permission.get(pk=permission.uuid) for permission in self.form_data['permissions']]

        for role in roles:
            for permission in permissions:
                AccessControlList.objects.grant(
                    permission=permission, role=role, obj=obj
                )
