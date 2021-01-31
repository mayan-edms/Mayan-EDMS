import logging

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from mayan.apps.django_gpg.exceptions import NeedPassphrase, PassphraseError
from mayan.apps.documents.models.document_file_models import DocumentFile
from mayan.apps.views.generics import (
    ConfirmView, FormView, SingleObjectCreateView, SingleObjectDeleteView,
    SingleObjectDetailView, SingleObjectDownloadView, SingleObjectListView
)
from mayan.apps.views.mixins import ExternalObjectViewMixin

from .forms import (
    DocumentFileSignatureCreateForm,
    DocumentFileSignatureDetailForm
)
from .icons import (
    icon_document_file_signature_detached_create,
    icon_document_file_signature_embedded_create,
    icon_document_file_signature_list
)
from .links import (
    link_document_file_signature_detached_create,
    link_document_file_signature_embedded_create,
    link_document_file_signature_upload
)
from .models import DetachedSignature, EmbeddedSignature, SignatureBaseModel
from .permissions import (
    permission_document_file_sign_detached,
    permission_document_file_sign_embedded,
    permission_document_file_signature_delete,
    permission_document_file_signature_download,
    permission_document_file_signature_upload,
    permission_document_file_signature_verify,
    permission_document_file_signature_view,
)
from .tasks import (
    task_refresh_signature_information, task_verify_missing_embedded_signature
)

logger = logging.getLogger(name=__name__)


class DocumentFileDetachedSignatureCreateView(ExternalObjectViewMixin, FormView):
    external_object_permission = permission_document_file_sign_detached
    external_object_pk_url_kwarg = 'document_file_id'
    external_object_queryset = DocumentFile.valid
    form_class = DocumentFileSignatureCreateForm

    def form_valid(self, form):
        key = form.cleaned_data['key']
        passphrase = form.cleaned_data['passphrase'] or None

        try:
            DetachedSignature.objects.sign_document_file(
                document_file=self.external_object,
                key=key, passphrase=passphrase, user=self.request.user
            )
        except NeedPassphrase:
            messages.error(
                message=_('Passphrase is needed to unlock this key.'),
                request=self.request
            )
            return HttpResponseRedirect(
                redirect_to=reverse(
                    viewname='signatures:document_file_signature_detached_create',
                    kwargs={
                        'document_file_id': self.external_object.pk
                    }
                )
            )
        except PassphraseError:
            messages.error(
                message=_('Passphrase is incorrect.'),
                request=self.request
            )
            return HttpResponseRedirect(
                redirect_to=reverse(
                    viewname='signatures:document_file_signature_detached_create',
                    kwargs={
                        'document_file_id': self.external_object.pk
                    }
                )
            )
        else:
            messages.success(
                message=_('Document file signed successfully.'),
                request=self.request
            )

        return super().form_valid(form)

    def get_extra_context(self):
        return {
            'object': self.external_object,
            'submit_icon': icon_document_file_signature_detached_create,
            'submit_label': _('Sign'),
            'title': _(
                'Sign document file "%s" with a detached signature'
            ) % self.external_object,
        }

    def get_form_extra_kwargs(self):
        return {'user': self.request.user}

    def get_post_action_redirect(self):
        return reverse(
            viewname='signatures:document_file_signature_list',
            kwargs={'document_file_id': self.external_object.pk}
        )


class DocumentFileEmbeddedSignatureCreateView(ExternalObjectViewMixin, FormView):
    external_object_permission = permission_document_file_sign_embedded
    external_object_pk_url_kwarg = 'document_file_id'
    external_object_queryset = DocumentFile.valid
    form_class = DocumentFileSignatureCreateForm

    def form_valid(self, form):
        key = form.cleaned_data['key']
        passphrase = form.cleaned_data['passphrase'] or None

        try:
            signature = EmbeddedSignature.objects.sign_document_file(
                document_file=self.external_object,
                key=key, passphrase=passphrase, user=self.request.user
            )
        except NeedPassphrase:
            messages.error(
                message=_('Passphrase is needed to unlock this key.'),
                request=self.request
            )
            return HttpResponseRedirect(
                redirect_to=reverse(
                    viewname='signatures:document_file_signature_embedded_create',
                    kwargs={
                        'document_file_id': self.external_object.pk
                    }
                )
            )
        except PassphraseError:
            messages.error(
                message=_('Passphrase is incorrect.'),
                request=self.request
            )
            return HttpResponseRedirect(
                redirect_to=reverse(
                    viewname='signatures:document_file_signature_embedded_create',
                    kwargs={
                        'document_file_id': self.external_object.pk
                    }
                )
            )
        else:
            messages.success(
                message=_('Document file signed successfully.'),
                request=self.request
            )

            return HttpResponseRedirect(
                redirect_to=reverse(
                    viewname='signatures:document_file_signature_list',
                    kwargs={'document_file_id': signature.document_file.pk}
                )
            )

        return super().form_valid(form)

    def get_extra_context(self):
        return {
            'object': self.external_object,
            'submit_icon': icon_document_file_signature_embedded_create,
            'submit_label': _('Sign'),
            'title': _(
                'Sign document file "%s" with a embedded signature'
            ) % self.external_object,
        }

    def get_form_extra_kwargs(self):
        return {'user': self.request.user}


class DocumentFileSignatureDeleteView(SingleObjectDeleteView):
    object_permission = permission_document_file_signature_delete
    pk_url_kwarg = 'signature_id'

    def get_extra_context(self):
        return {
            'object': self.object.document_file,
            'signature': self.object,
            'title': _('Delete detached signature: %s') % self.object
        }

    def get_post_action_redirect(self):
        return reverse(
            viewname='signatures:document_file_signature_list',
            kwargs={
                'document_file_id': self.object.document_file.pk
            }
        )

    def get_source_queryset(self):
        document_file_queryset = DocumentFile.valid.all()

        return DetachedSignature.objects.filter(
            document_file_id__in=document_file_queryset.values('pk')
        )


class DocumentFileSignatureDetailView(SingleObjectDetailView):
    form_class = DocumentFileSignatureDetailForm
    object_permission = permission_document_file_signature_view
    pk_url_kwarg = 'signature_id'

    def get_extra_context(self):
        return {
            'hide_object': True,
            'object': self.object.document_file,
            'signature': self.object,
            'title': _(
                'Details for signature: %s'
            ) % self.object,
        }

    def get_source_queryset(self):
        document_file_queryset = DocumentFile.valid.all()

        return SignatureBaseModel.objects.select_subclasses().filter(
            document_file_id__in=document_file_queryset.values('pk')
        )


class DocumentFileSignatureDownloadView(SingleObjectDownloadView):
    object_permission = permission_document_file_signature_download
    pk_url_kwarg = 'signature_id'

    def get_download_file_object(self):
        return self.object.signature_file

    def get_download_filename(self):
        return force_text(s=self.object)

    def get_source_queryset(self):
        document_file_queryset = DocumentFile.valid.all()

        return DetachedSignature.objects.filter(
            document_file_id__in=document_file_queryset.values('pk')
        )


class DocumentFileSignatureListView(
    ExternalObjectViewMixin, SingleObjectListView
):
    external_object_permission = permission_document_file_signature_view
    external_object_pk_url_kwarg = 'document_file_id'
    external_object_queryset = DocumentFile.valid

    def get_extra_context(self):
        return {
            'hide_object': True,
            'no_results_icon': icon_document_file_signature_list,
            'no_results_text': _(
                'Signatures help provide authorship evidence and tamper '
                'detection. They are very secure and hard to '
                'forge. A signature can be embedded as part of the document '
                'itself or uploaded as a separate file.'
            ),
            'no_results_secondary_links': [
                link_document_file_signature_detached_create.resolve(
                    RequestContext(
                        request=self.request, dict_={
                            'object': self.external_object
                        }
                    )
                ),
                link_document_file_signature_embedded_create.resolve(
                    RequestContext(
                        request=self.request, dict_={
                            'object': self.external_object
                        }
                    )
                ),
                link_document_file_signature_upload.resolve(
                    RequestContext(
                        request=self.request, dict_={
                            'object': self.external_object
                        }
                    )
                ),
            ],
            'no_results_title': _(
                'There are no signatures for this document file.'
            ),
            'object': self.external_object,
            'title': _(
                'Signatures for document file: %s'
            ) % self.external_object,
        }

    def get_source_queryset(self):
        return self.external_object.signatures.all()


class DocumentFileSignatureUploadView(
    ExternalObjectViewMixin, SingleObjectCreateView
):
    external_object_permission = permission_document_file_signature_upload
    external_object_pk_url_kwarg = 'document_file_id'
    external_object_queryset = DocumentFile.valid
    fields = ('signature_file',)
    model = DetachedSignature

    def get_extra_context(self):
        return {
            'object': self.external_object,
            'title': _(
                'Upload detached signature for document file: %s'
            ) % self.external_object,
        }

    def get_instance_extra_data(self):
        return {'document_file': self.external_object}

    def get_post_action_redirect(self):
        return reverse(
            viewname='signatures:document_file_signature_list', kwargs={
                'document_file_id': self.external_object.pk
            }
        )


class AllDocumentSignatureRefreshView(ConfirmView):
    extra_context = {
        'message': _(
            'On large databases this operation may take some time to execute.'
        ), 'title': _('Refresh all signatures information?'),
    }
    view_permission = permission_document_file_signature_verify

    def get_post_action_redirect(self):
        return reverse(viewname='common:tools_list')

    def view_action(self):
        task_refresh_signature_information.delay()
        messages.success(
            message=_('Signature information refresh queued successfully.'),
            request=self.request
        )


class AllDocumentSignatureVerifyView(ConfirmView):
    extra_context = {
        'message': _(
            'On large databases this operation may take some time to execute.'
        ), 'title': _('Verify all document for signatures?'),
    }
    view_permission = permission_document_file_signature_verify

    def get_post_action_redirect(self):
        return reverse(viewname='common:tools_list')

    def view_action(self):
        task_verify_missing_embedded_signature.delay()
        messages.success(
            message=_('Signature verification queued successfully.'),
            request=self.request
        )
