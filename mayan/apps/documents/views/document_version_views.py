import logging

from django.contrib import messages
from django.template import RequestContext
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from mayan.apps.views.generics import (
    ConfirmView, MultipleObjectDeleteView, SingleObjectDeleteView,
    SingleObjectDetailView, SingleObjectListView
)
from mayan.apps.views.mixins import ExternalObjectMixin

from ..events import event_document_viewed
from ..forms.document_version_forms import (
    DocumentVersionDownloadForm, DocumentVersionPreviewForm
)
from ..icons import icon_document_version_list
from ..models.document_models import Document
from ..models.document_version_models import DocumentVersion
from ..permissions import (
    permission_document_version_delete, permission_document_version_view
)

__all__ = (
    'DocumentVersionListView', 'DocumentVersionRevertView',
    'DocumentVersionView'
)
logger = logging.getLogger(name=__name__)


class DocumentVersionDeleteView(MultipleObjectDeleteView):
    model = DocumentVersion
    object_permission = permission_document_version_delete
    pk_url_kwarg = 'document_version_id'

    #def get_extra_context(self):
    #    return {
    #        #'message': _(
    #        #    'All document version pages from this document version will '
    #        #    'be deleted too.'
    #        #),
    #        'object': self.object,
    #        'title': _('Delete document version %s ?') % self.object,
    #    }
    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
        }

    def get_post_action_redirect(self):
        # Use [0] instead of first(). First returns None and it is not usable.
        return reverse(
            viewname='documents:document_version_list', kwargs={
                'document_id': self.object_list[0].document_id
            }
        )

'''
#class DocumentVersionDeleteView(SingleObjectDeleteView):
#    model = DocumentVersion
#    object_permission = permission_document_version_delete
#    pk_url_kwarg = 'document_version_id'

    def get_extra_context(self):
        return {
            'message': _(
                'All document version pages from this document version will '
                'be deleted too.'
            ),
            'object': self.object,
            'title': _('Delete document version %s ?') % self.object,
        }


    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
        }

    def get_post_action_redirect(self):
        return reverse(
            viewname='documents:document_version_list', kwargs={
                'document_id': self.object.document_id
            }
        )
'''

class DocumentVersionListView(ExternalObjectMixin, SingleObjectListView):
    external_object_class = Document
    external_object_permission = permission_document_version_view
    external_object_pk_url_kwarg = 'document_id'

    def get_document(self):
        document = self.external_object
        document.add_as_recent_document_for_user(user=self.request.user)
        return document

    def get_extra_context(self):
        return {
            'hide_object': True,
            'list_as_items': True,
            'no_results_icon': icon_document_version_list,
            #'no_results_main_link': link_tag_create.resolve(
            #    context=RequestContext(request=self.request)
            #),
            'no_results_text': _(
                'Versions are views that can display document file pages as '
                'they are, remap or merge them into different layouts.'
            ),
            'no_results_title': _('No versions available'),
            'object': self.get_document(),
            'table_cell_container_classes': 'td-container-thumbnail',
            'title': _('Versions of document: %s') % self.get_document(),
        }

    def get_source_queryset(self):
        return self.get_document().versions.order_by('-timestamp')


class DocumentVersionView(SingleObjectDetailView):
    form_class = DocumentVersionPreviewForm
    model = DocumentVersion
    object_permission = permission_document_version_view
    pk_url_kwarg = 'document_version_id'

    def dispatch(self, request, *args, **kwargs):
        result = super().dispatch(request, *args, **kwargs)
        self.object.document.add_as_recent_document_for_user(
            user=request.user
        )
        event_document_viewed.commit(
            actor=request.user, target=self.object.document
        )

        return result

    def get_extra_context(self):
        return {
            'hide_labels': True,
            'object': self.object,
            'title': _('Preview of document version: %s') % self.object,
        }
