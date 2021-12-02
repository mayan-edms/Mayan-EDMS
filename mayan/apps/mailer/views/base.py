from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.utils.translation import ungettext, ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.organizations.utils import get_organization_installation_url
from mayan.apps.views.generics import MultipleObjectFormActionView

from ..forms import ObjectMailForm
from ..literals import MODEL_SEND_FUNCTION_DOTTED_PATH
from ..models import UserMailer
from ..permissions import permission_user_mailer_use
from ..tasks import task_send_object


class ObjectLinkMailView(MultipleObjectFormActionView):
    as_attachment = False
    form_class = ObjectMailForm

    def get_extra_context(self):
        queryset = self.object_list

        result = {
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
        queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_user_mailer_use,
            queryset=UserMailer.objects.filter(enabled=True),
            user=self.request.user
        )

        mailer = get_object_or_404(
            klass=queryset, pk=form.cleaned_data['user_mailer'].pk
        )

        content_type = ContentType.objects.get_for_model(model=instance)

        kwargs = {
            'as_attachment': self.as_attachment,
            'body': form.cleaned_data['body'],
            'content_type_id': content_type.pk,
            'object_id': instance.pk,
            'object_name': _('Document file'),
            'organization_installation_url': get_organization_installation_url(
                request=self.request
            ),
            'recipient': form.cleaned_data['email'],
            'sender': self.request.user.email,
            'subject': form.cleaned_data['subject'],
            'user_mailer_id': mailer.pk,
            'user_id': self.request.user.pk
        }

        kwargs.update(
            MODEL_SEND_FUNCTION_DOTTED_PATH.get(instance._meta.model, {})
        )

        task_send_object.apply_async(kwargs=kwargs)


class ObjectAttachmentMailView(ObjectLinkMailView):
    as_attachment = True
