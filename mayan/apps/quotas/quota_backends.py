import types

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models import IntegerField
from django.db.models.functions import Cast
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

from actstream.models import Action

from mayan.apps.common.signals import signal_mayan_pre_save
from mayan.apps.documents.events import event_document_created
from mayan.apps.documents.models import Document, DocumentFile
from mayan.apps.user_management.querysets import get_user_queryset

from .classes import QuotaBackend
from .exceptions import QuotaExceeded
from .mixins import DocumentTypesQuotaMixin, GroupsUsersQuotaMixin


def hook_factory_document_check_quota(klass):
    def hook_check_quota(**kwargs):
        # Fake Document to be able to reuse the .process() method
        # for pre check.
        fake_document_instance = types.SimpleNamespace(pk=None)

        final_kwargs = kwargs['kwargs'].copy()
        final_kwargs['instance'] = fake_document_instance

        for quota in klass.get_instances().filter(enabled=True):
            backend_instance = quota.get_backend_instance()

            backend_instance.process(**final_kwargs)
    return hook_check_quota


def hook_factory_document_file_check_quota(klass):
    def hook_check_quota(**kwargs):
        # Pass the real parent document or create a fake one.
        if 'document' in kwargs['kwargs']:
            document = kwargs['kwargs']['document']
        else:
            document = types.SimpleNamespace(
                document_type=kwargs['kwargs']['document_type']
            )
        # Fake DocumentFile to be able to reuse the
        # .process() method for pre check.
        shared_uploaded_file = kwargs['kwargs']['shared_uploaded_file']
        if shared_uploaded_file:
            fake_document_instance = types.SimpleNamespace(
                file=kwargs['kwargs']['shared_uploaded_file'].file,
                document=document,
                pk=None
            )

            final_kwargs = kwargs['kwargs'].copy()
            final_kwargs['instance'] = fake_document_instance

            for quota in klass.get_instances().filter(enabled=True):
                backend_instance = quota.get_backend_instance()

                backend_instance.process(**final_kwargs)
    return hook_check_quota


class DocumentCountQuota(
    GroupsUsersQuotaMixin, DocumentTypesQuotaMixin, QuotaBackend
):
    error_message = _('Document count quota exceeded.')
    field_order = ('documents_limit',)
    fields = {
        'documents_limit': {
            'label': _('Documents limit'),
            'class': 'django.forms.IntegerField',
            'help_text': _(
                'Maximum number of documents.'
            )
        },
    }
    label = _('Document count limit')
    sender = Document
    signal = signal_mayan_pre_save

    @classmethod
    def _initialize(cls):
        Document.register_pre_create_hook(
            func=hook_factory_document_check_quota(klass=cls)
        )

    def __init__(
        self, document_type_all, document_type_ids, documents_limit,
        group_ids, user_all, user_ids
    ):
        self.document_type_all = document_type_all
        self.document_type_ids = document_type_ids
        self.documents_limit = documents_limit
        self.group_ids = group_ids
        self.user_all = user_all
        self.user_ids = user_ids

    def _allowed(self):
        return self.documents_limit

    def _allowed_filter_display(self):
        return _('document count: %(document_count)s') % {
            'document_count': self._allowed()
        }

    def _get_user_document_count(self, user):
        action_queryset = Action.objects.annotate(
            target_object_id_int=Cast(
                'target_object_id', output_field=IntegerField()
            ),
        )
        action_filter_kwargs = {
            'verb': event_document_created.id
        }
        document_filter_kwargs = {}

        if not self.document_type_all:
            document_filter_kwargs.update(
                {
                    'document_type_id__in': self._get_document_types().values(
                        'pk'
                    ),
                }
            )

        if user:
            # Admins are always excluded.
            if user.is_superuser or user.is_staff:
                return 0

            if not self.user_all:
                users = self._get_users() | get_user_queryset().filter(
                    groups__in=self._get_groups()
                )

                if not users.filter(pk=user.pk).exists():
                    # User is not in the restricted list of users and groups.
                    return 0
                else:
                    content_type = ContentType.objects.get_for_model(
                        model=get_user_model()
                    )

                    action_filter_kwargs.update(
                        {
                            'actor_object_id': user.pk,
                            'actor_content_type': content_type,
                        }
                    )

        action_queryset = action_queryset.filter(**action_filter_kwargs)

        document_filter_kwargs.update(
            {
                'pk__in': action_queryset.values('target_object_id_int')
            }
        )

        return Document.objects.filter(**document_filter_kwargs).count()

    def process(self, **kwargs):
        # Only for new documents.
        if not kwargs['instance'].pk:
            if self._get_user_document_count(user=kwargs.get('user')) >= self._allowed():
                raise QuotaExceeded(
                    _('Document count quota exceeded.')
                )


class DocumentSizeQuota(
    GroupsUsersQuotaMixin, DocumentTypesQuotaMixin, QuotaBackend
):
    field_order = ('document_size_limit',)
    fields = {
        'document_size_limit': {
            'label': _('Document size limit'),
            'class': 'django.forms.FloatField',
            'help_text': _('Maximum document size in megabytes (MB).')
        }
    }
    label = _('Document size limit')
    sender = DocumentFile
    signal = signal_mayan_pre_save

    @classmethod
    def _initialize(cls):
        DocumentFile.register_pre_create_hook(
            func=hook_factory_document_file_check_quota(klass=cls)
        )

    def __init__(
        self, document_size_limit, document_type_all, document_type_ids,
        group_ids, user_all, user_ids
    ):
        self.document_size_limit = document_size_limit
        self.document_type_all = document_type_all
        self.document_type_ids = document_type_ids
        self.group_ids = group_ids
        self.user_all = user_all
        self.user_ids = user_ids

    def _allowed(self):
        return self.document_size_limit * 1024 * 1024

    def _allowed_filter_display(self):
        return _('document size: %(formatted_file_size)s') % {
            'formatted_file_size': filesizeformat(self._allowed())
        }

    def process(self, **kwargs):
        if not kwargs['instance'].pk:
            if kwargs['instance'].file.size >= self._allowed():
                if self.document_type_all or self._get_document_types().filter(pk=kwargs['instance'].document.document_type.pk).exists():
                    # Don't asume there is always a user in the signal.
                    # Non interactive uploads might not include a user.
                    if kwargs['user']:
                        if kwargs['user'].is_superuser or kwargs['user'].is_staff:
                            return

                    users = self._get_users() | get_user_queryset().filter(
                        groups__in=self._get_groups()
                    )

                    if self.user_all or kwargs['user'] and users.filter(pk=kwargs['user'].pk).exists():
                        raise QuotaExceeded(
                            _('Document size quota exceeded.')
                        )
