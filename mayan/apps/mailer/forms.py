from django import forms
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.common.settings import (
    setting_project_title, setting_project_url
)
from mayan.apps.views.forms import BackendDynamicForm

from .classes import MailerBackend
from .models import UserMailer
from .permissions import permission_user_mailer_use
from .settings import (
    setting_attachment_body_template, setting_attachment_subject_template,
    setting_document_link_body_template, setting_document_link_subject_template
)
from .validators import validate_email_multiple


class ObjectMailForm(forms.Form):
    def __init__(self, *args, **kwargs):
        as_attachment = kwargs.pop('as_attachment', False)
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if as_attachment:
            self.fields[
                'subject'
            ].initial = setting_attachment_subject_template.value

            self.fields[
                'body'
            ].initial = setting_attachment_body_template.value % {
                'project_title': setting_project_title.value,
                'project_website': setting_project_url.value
            }
        else:
            self.fields[
                'subject'
            ].initial = setting_document_link_subject_template.value
            self.fields['body'].initial = setting_document_link_body_template.value % {
                'project_title': setting_project_title.value,
                'project_website': setting_project_url.value
            }

        queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_user_mailer_use,
            queryset=UserMailer.objects.filter(enabled=True), user=user
        )

        self.fields['user_mailer'].queryset = queryset
        try:
            self.fields['user_mailer'].initial = queryset.get(default=True)
        except UserMailer.DoesNotExist:
            pass

    email = forms.CharField(
        help_text=_(
            'Email address of the recipient. Can be multiple addresses '
            'separated by comma or semicolon.'
        ), label=_('Email address'), validators=[validate_email_multiple]
    )
    subject = forms.CharField(label=_('Subject'), required=False)
    body = forms.CharField(
        label=_('Body'), widget=forms.widgets.Textarea(), required=False
    )
    user_mailer = forms.ModelChoiceField(
        help_text=_(
            'The email profile that will be used to send this email.'
        ), label=_('Mailing profile'), queryset=UserMailer.objects.none()
    )


class UserMailerBackendSelectionForm(forms.Form):
    backend = forms.ChoiceField(
        choices=(), help_text=_('The driver to use when sending emails.'),
        label=_('Backend')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['backend'].choices = MailerBackend.get_choices()


class UserMailerDynamicForm(BackendDynamicForm):
    class Meta:
        fields = ('label', 'enabled')
        model = UserMailer


class UserMailerTestForm(forms.Form):
    email = forms.CharField(
        help_text=_(
            'Email address of the recipient. Can be multiple addresses '
            'separated by comma or semicolon.'
        ), label=_('Email address'), validators=[validate_email_multiple]
    )
