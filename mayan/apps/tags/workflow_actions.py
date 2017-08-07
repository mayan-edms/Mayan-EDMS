from __future__ import absolute_import, unicode_literals

import logging

from django.utils.translation import ugettext_lazy as _

from acls.models import AccessControlList
from document_states.classes import WorkflowAction
from tags.models import Tag
from tags.permissions import permission_tag_view

__all__ = ('AttachTagAction',)
logger = logging.getLogger(__name__)


class AttachTagAction(WorkflowAction):
    fields = (
        {
            'name': 'tags', 'label': _('Tags'),
            'class': 'django.forms.ModelMultipleChoiceField', 'kwargs': {
                'help_text': _('Tags to attach to the document'),
                'queryset': Tag.objects.none(), 'required': False
            }
        },
    )
    label = _('Attach tag')
    widgets = {
        'tags': {
            'class': 'tags.widgets.TagFormWidget', 'kwargs': {
                'attrs': {'class': 'select2-tags'},
                'queryset': Tag.objects.none()
            }
        }
    }

    def __init__(self, tags=None):
        if tags:
            self.tags = Tag.objects.filter(pk__in=tags)
        else:
            self.tags = Tag.objects.none()

    def get_form_schema(self, request):
        user = request.user
        logger.debug('user: %s', user)

        queryset = AccessControlList.objects.filter_by_access(
            permission_tag_view, user, queryset=Tag.objects.all()
        )

        self.fields[0]['kwargs']['queryset'] = queryset
        self.widgets['tags']['kwargs']['queryset'] = queryset

        return {
            'fields': self.fields,
            'widgets': self.widgets
        }

    def execute(self, context):
        for tag in self.tags:
            tag.attach_to(
                document=context['entry_log'].workflow_instance.document
            )
