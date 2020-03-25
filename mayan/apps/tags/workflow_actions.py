import logging

from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.document_states.classes import WorkflowAction

from .models import Tag
from .permissions import permission_tag_attach, permission_tag_remove

__all__ = ('AttachTagAction', 'RemoveTagAction')
logger = logging.getLogger(name=__name__)


class AttachTagAction(WorkflowAction):
    fields = {
        'tags': {
            'label': _('Tags'),
            'class': 'django.forms.ModelMultipleChoiceField', 'kwargs': {
                'help_text': _('Tags to attach to the document'),
                'queryset': Tag.objects.none(), 'required': False
            }
        },
    }
    label = _('Attach tag')
    media = {
        'js': ('tags/js/tags_form.js',)
    }
    widgets = {
        'tags': {
            'class': 'mayan.apps.tags.widgets.TagFormWidget', 'kwargs': {
                'attrs': {'class': 'select2-tags'},
            }
        }
    }
    permission = permission_tag_attach

    def execute(self, context):
        for tag in self.get_tags():
            tag.attach_to(document=context['document'])

    def get_form_schema(self, request):
        user = request.user
        logger.debug('user: %s', user)

        queryset = AccessControlList.objects.restrict_queryset(
            permission=self.permission, queryset=Tag.objects.all(),
            user=user
        )

        self.fields['tags']['kwargs']['queryset'] = queryset

        return {
            'fields': self.fields,
            'media': self.media,
            'widgets': self.widgets
        }

    def get_tags(self):
        return Tag.objects.filter(pk__in=self.form_data.get('tags', ()))


class RemoveTagAction(AttachTagAction):
    fields = {
        'tags': {
            'label': _('Tags'),
            'class': 'django.forms.ModelMultipleChoiceField', 'kwargs': {
                'help_text': _('Tags to remove from the document'),
                'queryset': Tag.objects.none(), 'required': False
            }
        },
    }
    label = _('Remove tag')
    permission = permission_tag_remove

    def execute(self, context):
        for tag in self.get_tags():
            tag.remove_from(document=context['document'])
