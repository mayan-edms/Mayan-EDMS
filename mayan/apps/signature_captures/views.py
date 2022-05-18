import logging

from django.shortcuts import reverse
from django.template import RequestContext
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.models import Document
from mayan.apps.views.generics import (
    SingleObjectCreateView, SingleObjectDeleteView, SingleObjectDetailView,
    SingleObjectEditView, SingleObjectListView
)
from mayan.apps.views.mixins import ExternalObjectViewMixin

from .forms import SignatureCaptureForm, SignatureCaptureDetailForm
from .icons import (
    icon_signature_captures, icon_signature_capture_create,
    icon_signature_capture_single_delete, icon_signature_capture_edit,
    icon_signature_capture_list
)
from .links import link_signature_capture_create
from .models import SignatureCapture
from .permissions import (
    permission_signature_capture_create, permission_signature_capture_delete,
    permission_signature_capture_edit, permission_signature_capture_view
)

logger = logging.getLogger(name=__name__)


class SignatureCaptureCreateView(
    ExternalObjectViewMixin, SingleObjectCreateView
):
    external_object_permission = permission_signature_capture_create
    external_object_pk_url_kwarg = 'document_id'
    external_object_queryset = Document.valid.all()
    form_class = SignatureCaptureForm
    view_icon = icon_signature_capture_create

    def get_extra_context(self):
        return {
            'object': self.external_object,
            'title': _(
                'Create signature capture for document: %s'
            ) % self.external_object
        }

    def get_instance_extra_data(self):
        return {
            'document': self.external_object,
            'user': self.request.user
        }

    def get_post_action_redirect(self):
        return reverse(
            viewname='signature_captures:signature_capture_list', kwargs={
                'document_id': self.external_object.pk
            }
        )


class SignatureCaptureDeleteView(SingleObjectDeleteView):
    object_permission = permission_signature_capture_delete
    pk_url_kwarg = 'signature_capture_id'
    source_queryset = SignatureCapture.valid.all()
    view_icon = icon_signature_capture_single_delete

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }

    def get_extra_context(self):
        return {
            'document': self.object.document,
            'navigation_object_list': ('object', 'document'),
            'object': self.object,
            'title': _('Delete signature capture: %s') % self.object
        }

    def get_post_action_redirect(self):
        return reverse_lazy(
            viewname='signature_captures:signature_capture_list', kwargs={
                'document_id': self.object.document.pk
            }
        )


class SignatureCaptureDetailView(SingleObjectDetailView):
    form_class = SignatureCaptureDetailForm
    object_permission = permission_signature_capture_view
    pk_url_kwarg = 'signature_capture_id'
    source_queryset = SignatureCapture.valid.all()
    view_icon = icon_signature_captures

    def get_extra_context(self):
        return {
            'navigation_object_list': ('object', 'object.document'),
            'object': self.object,
            'title': _('Details of: %s') % self.object
        }


class SignatureCaptureEditView(SingleObjectEditView):
    form_class = SignatureCaptureForm
    object_permission = permission_signature_capture_edit
    pk_url_kwarg = 'signature_capture_id'
    source_queryset = SignatureCapture.valid.all()
    view_icon = icon_signature_capture_edit

    def get_extra_context(self):
        return {
            'document': self.object.document,
            'navigation_object_list': ('object', 'document'),
            'object': self.object,
            'title': _('Edit document signature capture: %s') % self.object
        }

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class SignatureCaptureListView(
    ExternalObjectViewMixin, SingleObjectListView
):
    external_object_pk_url_kwarg = 'document_id'
    external_object_queryset = Document.valid.all()
    object_permission = permission_signature_capture_view
    view_icon = icon_signature_capture_list

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'no_results_icon': icon_signature_captures,
            'no_results_main_link': link_signature_capture_create.resolve(
                context=RequestContext(
                    self.request, {'object': self.external_object}
                )
            ),
            'no_results_text': _(
                'Signature captures are electronic versions of a '
                'persons\'s handwritten signature.'
            ),
            'no_results_title': _('Document has no signature captures'),
            'object': self.external_object,
            'title': _(
                'Signature captures for document: %s'
            ) % self.external_object
        }

    def get_source_queryset(self):
        return self.external_object.signature_captures.all()
