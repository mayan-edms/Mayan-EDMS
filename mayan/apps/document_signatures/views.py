import logging

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.common.generics import (
    ConfirmView, FormView, SingleObjectCreateView, SingleObjectDeleteView,
    SingleObjectDetailView, SingleObjectDownloadView, SingleObjectListView
)
from mayan.apps.common.mixins import ExternalObjectMixin
from mayan.apps.django_gpg.exceptions import NeedPassphrase, PassphraseError
from mayan.apps.django_gpg.permissions import permission_key_sign
from mayan.apps.documents.models import DocumentVersion

from .forms import (
    DocumentVersionSignatureCreateForm,
    DocumentVersionSignatureDetailForm
)
from .icons import (
    icon_document_signature_list,
    icon_document_version_signature_detached_create,
    icon_document_version_signature_embedded_create
)
from .links import (
    link_document_version_signature_detached_create,
    link_document_version_signature_embedded_create,
    link_document_version_signature_upload
)
from .models import DetachedSignature, EmbeddedSignature, SignatureBaseModel
from .permissions import (
    permission_document_version_sign_detached,
    permission_document_version_sign_embedded,
    permission_document_version_signature_delete,
    permission_document_version_signature_download,
    permission_document_version_signature_upload,
    permission_document_version_signature_verify,
    permission_document_version_signature_view,
)
from .tasks import task_verify_missing_embedded_signature

logger = logging.getLogger(name=__name__)


class DocumentVersionDetachedSignatureCreateView(FormView):
    form_class = DocumentVersionSignatureCreateForm

    def form_valid(self, form):
        key = form.cleaned_data['key']
        passphrase = form.cleaned_data['passphrase'] or None

        AccessControlList.objects.check_access(
            obj=key, permissions=(permission_key_sign,), user=self.request.user
        )

        try:
            DetachedSignature.objects.sign_document_version(
                document_version=self.get_document_version(),
                key=key, passphrase=passphrase, user=self.request.user
            )
        except NeedPassphrase:
            messages.error(
                message=_('Passphrase is needed to unlock this key.'),
                request=self.request
            )
            return HttpResponseRedirect(
                redirect_to=reverse(
                    viewname='signatures:document_version_signature_detached_create',
                    kwargs={
                        'document_version_id': self.get_document_version().pk
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
                    viewname='signatures:document_version_signature_detached_create',
                    kwargs={
                        'document_version_id': self.get_document_version().pk
                    }
                )
            )
        else:
            messages.success(
                message=_('Document version signed successfully.'),
                request=self.request
            )

        return super(
            DocumentVersionDetachedSignatureCreateView, self
        ).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        AccessControlList.objects.check_access(
            obj=self.get_document_version().document,
            permissions=(permission_document_version_sign_detached,),
            user=request.user
        )

        return super(
            DocumentVersionDetachedSignatureCreateView, self
        ).dispatch(request, *args, **kwargs)

    def get_document_version(self):
        return get_object_or_404(
            klass=DocumentVersion, pk=self.kwargs['document_version_id']
        )

    def get_extra_context(self):
        return {
            'object': self.get_document_version(),
            'submit_icon_class': icon_document_version_signature_detached_create,
            'submit_label': _('Sign'),
            'title': _(
                'Sign document version "%s" with a detached signature'
            ) % self.get_document_version(),
        }

    def get_form_extra_kwargs(self):
        return {'user': self.request.user}

    def get_post_action_redirect(self):
        return reverse(
            viewname='signatures:document_version_signature_list',
            kwargs={'document_version_id': self.get_document_version().pk}
        )


class DocumentVersionEmbeddedSignatureCreateView(FormView):
    form_class = DocumentVersionSignatureCreateForm

    def form_valid(self, form):
        key = form.cleaned_data['key']
        passphrase = form.cleaned_data['passphrase'] or None

        AccessControlList.objects.check_access(
            obj=key, permissions=(permission_key_sign,), user=self.request.user
        )

        try:
            signature = EmbeddedSignature.objects.sign_document_version(
                document_version=self.get_document_version(),
                key=key, passphrase=passphrase, user=self.request.user
            )
        except NeedPassphrase:
            messages.error(
                message=_('Passphrase is needed to unlock this key.'),
                request=self.request
            )
            return HttpResponseRedirect(
                redirect_to=reverse(
                    viewname='signatures:document_version_signature_embedded_create',
                    kwargs={
                        'document_version_id': self.get_document_version().pk
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
                    viewname='signatures:document_version_signature_embedded_create',
                    kwargs={
                        'document_version_id': self.get_document_version().pk
                    }
                )
            )
        else:
            messages.success(
                message=_('Document version signed successfully.'),
                request=self.request
            )

            return HttpResponseRedirect(
                redirect_to=reverse(
                    viewname='signatures:document_version_signature_list',
                    kwargs={'document_version_id': signature.document_version.pk}
                )
            )

        return super(
            DocumentVersionEmbeddedSignatureCreateView, self
        ).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        AccessControlList.objects.check_access(
            obj=self.get_document_version().document,
            permissions=(permission_document_version_sign_embedded,),
            user=request.user
        )

        return super(
            DocumentVersionEmbeddedSignatureCreateView, self
        ).dispatch(request, *args, **kwargs)

    def get_document_version(self):
        return get_object_or_404(
            klass=DocumentVersion, pk=self.kwargs['document_version_id']
        )

    def get_extra_context(self):
        return {
            'object': self.get_document_version(),
            'submit_icon_class': icon_document_version_signature_embedded_create,
            'submit_label': _('Sign'),
            'title': _(
                'Sign document version "%s" with a embedded signature'
            ) % self.get_document_version(),
        }

    def get_form_extra_kwargs(self):
        return {'user': self.request.user}


class DocumentVersionSignatureDeleteView(SingleObjectDeleteView):
    model = DetachedSignature
    object_permission = permission_document_version_signature_delete
    pk_url_kwarg = 'signature_id'

    def get_extra_context(self):
        return {
            'object': self.object.document_version,
            'signature': self.object,
            'title': _('Delete detached signature: %s') % self.object
        }

    def get_post_action_redirect(self):
        return reverse(
            viewname='signatures:document_version_signature_list',
            kwargs={
                'document_version_id': self.object.document_version.pk
            }
        )


class DocumentVersionSignatureDetailView(SingleObjectDetailView):
    form_class = DocumentVersionSignatureDetailForm
    object_permission = permission_document_version_signature_view
    pk_url_kwarg = 'signature_id'

    def get_extra_context(self):
        return {
            'hide_object': True,
            'object': self.object.document_version,
            'signature': self.object,
            'title': _(
                'Details for signature: %s'
            ) % self.object,
        }

    def get_source_queryset(self):
        return SignatureBaseModel.objects.select_subclasses()


class DocumentVersionSignatureDownloadView(SingleObjectDownloadView):
    model = DetachedSignature
    object_permission = permission_document_version_signature_download
    pk_url_kwarg = 'signature_id'

    def get_download_file_object(self):
        return self.object.signature_file

    def get_download_filename(self):
        return force_text(self.object)


class DocumentVersionSignatureListView(
    ExternalObjectMixin, SingleObjectListView
):
    external_object_class = DocumentVersion
    external_object_permission = permission_document_version_signature_view
    external_object_pk_url_kwarg = 'document_version_id'

    def get_extra_context(self):
        return {
            'hide_object': True,
            'no_results_icon': icon_document_signature_list,
            'no_results_text': _(
                'Signatures help provide authorship evidence and tamper '
                'detection. They are very secure and hard to '
                'forge. A signature can be embedded as part of the document '
                'itself or uploaded as a separate file.'
            ),
            'no_results_secondary_links': [
                link_document_version_signature_detached_create.resolve(
                    RequestContext(
                        request=self.request, dict_={
                            'object': self.external_object
                        }
                    )
                ),
                link_document_version_signature_embedded_create.resolve(
                    RequestContext(
                        request=self.request, dict_={
                            'object': self.external_object
                        }
                    )
                ),
                link_document_version_signature_upload.resolve(
                    RequestContext(
                        request=self.request, dict_={
                            'object': self.external_object
                        }
                    )
                ),
            ],
            'no_results_title': _(
                'There are no signatures for this document.'
            ),
            'object': self.external_object,
            'title': _(
                'Signatures for document version: %s'
            ) % self.external_object,
        }

    def get_source_queryset(self):
        return self.external_object.signatures.all()


class DocumentVersionSignatureUploadView(SingleObjectCreateView):
    fields = ('signature_file',)
    model = DetachedSignature

    def dispatch(self, request, *args, **kwargs):
        AccessControlList.objects.check_access(
            obj=self.get_document_version(),
            permissions=(permission_document_version_signature_upload,),
            user=request.user
        )

        return super(
            DocumentVersionSignatureUploadView, self
        ).dispatch(request, *args, **kwargs)

    def get_document_version(self):
        return get_object_or_404(
            klass=DocumentVersion, pk=self.kwargs['document_version_id']
        )

    def get_extra_context(self):
        return {
            'object': self.get_document_version(),
            'title': _(
                'Upload detached signature for document version: %s'
            ) % self.get_document_version(),
        }

    def get_instance_extra_data(self):
        return {'document_version': self.get_document_version()}

    def get_post_action_redirect(self):
        return reverse(
            viewname='signatures:document_version_signature_list', kwargs={
                'document_version_id': self.get_document_version().pk
            }
        )


class AllDocumentSignatureVerifyView(ConfirmView):
    extra_context = {
        'message': _(
            'On large databases this operation may take some time to execute.'
        ), 'title': _('Verify all document for signatures?'),
    }
    view_permission = permission_document_version_signature_verify

    def get_post_action_redirect(self):
        return reverse(viewname='common:tools_list')

    def view_action(self):
        task_verify_missing_embedded_signature.delay()
        messages.success(
            message=_('Signature verification queued successfully.'),
            request=self.request
        )
