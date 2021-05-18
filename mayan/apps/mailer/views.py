from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.utils.translation import ungettext, ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.models import Document
from mayan.apps.organizations.utils import get_organization_installation_url
from mayan.apps.views.generics import (
    FormView, MultipleObjectFormActionView, SingleObjectDeleteView,
    SingleObjectDynamicFormCreateView, SingleObjectDynamicFormEditView,
    SingleObjectListView
)
from mayan.apps.views.mixins import ExternalObjectViewMixin

from .classes import MailerBackend
from .forms import (
    DocumentMailForm, UserMailerBackendSelectionForm, UserMailerDynamicForm,
    UserMailerTestForm
)
from .icons import icon_mail_document_submit, icon_user_mailer_setup
from .links import link_user_mailer_create
from .models import UserMailer
from .permissions import (
    permission_mailing_link, permission_mailing_send_document,
    permission_user_mailer_create, permission_user_mailer_delete,
    permission_user_mailer_edit, permission_user_mailer_use,
    permission_user_mailer_view
)
from .tasks import task_send_document


class MailDocumentView(MultipleObjectFormActionView):
    as_attachment = True
    form_class = DocumentMailForm
    object_permission = permission_mailing_send_document
    pk_url_kwarg = 'document_id'
    source_queryset = Document.valid
    success_message = _('%(count)d document queued for email delivery')
    success_message_plural = _(
        '%(count)d documents queued for email delivery'
    )
    title = 'Email document'
    title_plural = 'Email documents'
    title_document = 'Email document: %s'

    def get_extra_context(self):
        queryset = self.object_list

        result = {
            'submit_icon': icon_mail_document_submit,
            'submit_label': _('Send'),
            'title': ungettext(
                singular=self.title,
                plural=self.title_plural,
                number=queryset.count()
            )
        }

        if queryset.count() == 1:
            result.update(
                {
                    'object': queryset.first(),
                    'title': _(self.title_document) % queryset.first()
                }
            )

        return result

    def get_form_extra_kwargs(self):
        return {
            'as_attachment': self.as_attachment,
            'user': self.request.user
        }

    def object_action(self, form, instance):
        AccessControlList.objects.check_access(
            obj=form.cleaned_data['user_mailer'],
            permissions=(permission_user_mailer_use,), user=self.request.user
        )

        task_send_document.apply_async(
            kwargs={
                'as_attachment': self.as_attachment,
                'body': form.cleaned_data['body'],
                'document_id': instance.pk,
                'organization_installation_url': get_organization_installation_url(
                    request=self.request
                ),
                'recipient': form.cleaned_data['email'],
                'sender': self.request.user.email,
                'subject': form.cleaned_data['subject'],
                'user_mailer_id': form.cleaned_data['user_mailer'].pk
            }
        )


class MailDocumentLinkView(MailDocumentView):
    as_attachment = False
    object_permission = permission_mailing_link
    success_message = _('%(count)d document link queued for email delivery')
    success_message_plural = _(
        '%(count)d document links queued for email delivery'
    )
    title = 'Email document link'
    title_plural = 'Email document links'
    title_document = 'Email link for document: %s'


class UserMailerBackendSelectionView(FormView):
    extra_context = {
        'title': _('New mailing profile backend selection'),
    }
    form_class = UserMailerBackendSelectionForm
    view_permission = permission_user_mailer_create

    def form_valid(self, form):
        backend = form.cleaned_data['backend']
        return HttpResponseRedirect(
            redirect_to=reverse(
                viewname='mailer:user_mailer_create', kwargs={
                    'class_path': backend
                }
            )
        )


class UserMailingCreateView(SingleObjectDynamicFormCreateView):
    form_class = UserMailerDynamicForm
    post_action_redirect = reverse_lazy(viewname='mailer:user_mailer_list')
    view_permission = permission_user_mailer_create

    def get_backend(self):
        try:
            return MailerBackend.get(name=self.kwargs['class_path'])
        except KeyError:
            raise Http404(
                '{} class not found'.format(self.kwargs['class_path'])
            )

    def get_extra_context(self):
        return {
            'title': _(
                'Create a "%s" mailing profile'
            ) % self.get_backend().label,
        }

    def get_form_schema(self):
        backend = self.get_backend()
        result = {
            'fields': backend.fields,
            'widgets': getattr(backend, 'widgets', {})
        }
        if hasattr(backend, 'field_order'):
            result['field_order'] = backend.field_order

        return result

    def get_instance_extra_data(self):
        return {'backend_path': self.kwargs['class_path']}


class UserMailingDeleteView(SingleObjectDeleteView):
    model = UserMailer
    object_permission = permission_user_mailer_delete
    pk_url_kwarg = 'mailer_id'
    post_action_redirect = reverse_lazy(viewname='mailer:user_mailer_list')

    def get_extra_context(self):
        return {
            'title': _('Delete mailing profile: %s') % self.object,
        }


class UserMailingEditView(SingleObjectDynamicFormEditView):
    form_class = UserMailerDynamicForm
    model = UserMailer
    object_permission = permission_user_mailer_edit
    pk_url_kwarg = 'mailer_id'

    def get_extra_context(self):
        return {
            'title': _('Edit mailing profile: %s') % self.object,
        }

    def get_form_schema(self):
        backend = self.object.get_backend()
        result = {
            'fields': backend.fields,
            'widgets': getattr(backend, 'widgets', {})
        }
        if hasattr(backend, 'field_order'):
            result['field_order'] = backend.field_order

        return result


class UserMailerListView(SingleObjectListView):
    model = UserMailer
    object_permission = permission_user_mailer_view

    def get_extra_context(self):
        return {
            'hide_object': True,
            'no_results_icon': icon_user_mailer_setup,
            'no_results_main_link': link_user_mailer_create.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'Mailing profiles are email configurations. '
                'Mailing profiles allow sending documents as attachments or as '
                'links via email.'
            ),
            'no_results_title': _('No mailing profiles available'),
            'title': _('Mailing profile'),
        }

    def get_form_schema(self):
        return {'fields': self.get_backend().fields}


class UserMailerTestView(ExternalObjectViewMixin, FormView):
    external_object_class = UserMailer
    external_object_permission = permission_user_mailer_use
    external_object_pk_url_kwarg = 'mailer_id'
    form_class = UserMailerTestForm

    def form_valid(self, form):
        self.external_object.test(to=form.cleaned_data['email'])
        messages.success(
            message=_('Test email sent.'), request=self.request
        )
        return super().form_valid(form=form)

    def get_extra_context(self):
        return {
            'hide_object': True,
            'object': self.external_object,
            'submit_label': _('Test'),
            'title': _('Test mailing profile: %s') % self.external_object,
        }
