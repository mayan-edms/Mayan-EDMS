from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_save
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

from actstream.models import actor_stream

from documents.events import event_document_create, event_document_new_version
from documents.models import Document, DocumentVersion

from .classes import QuotaBackend
from .exceptions import QuotaExceeded

__all__ = ('DocumentStorageQuota', 'DocumentCountQuota',)


class DocumentCountQuota(QuotaBackend):
    fields = (
        {
            'name': 'documents_limit', 'label': _('Documents limit'),
            'class': 'django.forms.IntegerField',
            'help_text': _('Maximum number of documents')
        },
    )
    label = _('Document count')
    sender = Document
    signal = pre_save

    def __init__(self, documents_limit):
        self.documents_limit = documents_limit

    def _allowed(self):
        return self.documents_limit

    def _usage(self, **kwargs):
        return Document.passthrough.all().count()

    def display(self):
        return _(
            'Maximum document count: %(total_documents)s'
        ) % {
            'total_documents': self._allowed(),
        }

    def process(self, **kwargs):
        if self._usage() > self._allowed():
            raise QuotaExceeded('Document count exceeded')

    def usage(self):
        return _('%(usage)s out of %(allowed)s') % {
            'usage': self._usage(),
            'allowed': self._allowed()
        }


class DocumentStorageQuota(QuotaBackend):
    fields = (
        {
            'name': 'storage_size', 'label': _('Storage size'),
            'class': 'django.forms.FloatField',
            'help_text': _('Total storage usage in megabytes (MB)')
        },
    )
    label = _('Document storage')
    sender = Document
    signal = pre_save

    def __init__(self, storage_size):
        self.storage_size = storage_size

    def _allowed(self):
        return self.storage_size * 1024 * 1024

    def _usage(self, **kwargs):
        total_usage = 0
        for document_version in DocumentVersion.objects.all():
            if document_version.exists():
                total_usage += document_version.file.size

        return total_usage

    def display(self):
        return _(
            'Maximum storage usage: %(formatted_file_size)s (%(raw_file_size)s MB)'
        ) % {
            'formatted_file_size': filesizeformat(self._allowed()),
            'raw_file_size': self.storage_size
        }

    def process(self, **kwargs):
        if self._usage() > self.storage_size * 1024 * 1024:
            raise QuotaExceeded('Storage usage exceeded')

    def usage(self):
        return _('%(usage)s out of %(allowed)s') % {
            'usage': filesizeformat(self._usage()),
            'allowed': filesizeformat(self._allowed())
        }


class UserDocumentCountQuota(QuotaBackend):
    fields = (
        {
            'name': 'username', 'label': _('Username'),
            'class': 'django.forms.CharField', 'kwargs': {
                'max_length': 255
            }, 'help_text': _(
                'Username of the user to which the quota will be applied'
            )
        },
        {
            'name': 'documents_limit', 'label': _('Documents limit'),
            'class': 'django.forms.IntegerField',
            'help_text': _('Maximum number of documents')
        },
    )
    label = _('User document count')
    sender = Document
    signal = pre_save

    def __init__(self, documents_limit, username):
        self.documents_limit = documents_limit
        self.username = username

    def _allowed(self):
        return self.documents_limit

    def _usage(self, **kwargs):
        user = get_user_model().objects.get(username=self.username)
        return actor_stream(user).filter(verb=event_document_create.id).count()

    def display(self):
        user = get_user_model().objects.get(username=self.username)
        return _(
            'Maximum document count: %(total_documents)s, for user: %(user)s'
        ) % {
            'total_documents': self._allowed(),
            'user': user.get_full_name() or user
        }

    def process(self, **kwargs):
        if self._usage() > self._allowed():
            raise QuotaExceeded('Document count exceeded')

    def usage(self):
        return _('%(usage)s out of %(allowed)s') % {
            'usage': self._usage(),
            'allowed': self._allowed()
        }


###
class UserDocumentStorageQuota(QuotaBackend):
    fields = (
        {
            'name': 'username', 'label': _('Username'),
            'class': 'django.forms.CharField', 'kwargs': {
                'max_length': 255
            }, 'help_text': _(
                'Username of the user to which the quota will be applied'
            )
        },
        {
            'name': 'storage_size', 'label': _('Storage size'),
            'class': 'django.forms.FloatField',
            'help_text': _('Total storage usage in megabytes (MB)')
        },
    )
    label = _('User document storage')
    sender = Document
    signal = pre_save

    def __init__(self, storage_size, username):
        self.storage_size = storage_size
        self.username = username

    def _allowed(self):
        return self.storage_size * 1024 * 1024

    def _usage(self, **kwargs):
        total_usage = 0
        user = get_user_model().objects.get(username=self.username)
        content_type = ContentType.objects.get_for_model(model=user)
        for document_version in DocumentVersion.objects.filter(target_actions__actor_object_id=1, target_actions__actor_content_type=content_type, target_actions__verb=event_document_new_version.id):
            if document_version.exists():
                total_usage += document_version.file.size

        return total_usage

    def display(self):
        user = get_user_model().objects.get(username=self.username)
        return _(
            'Maximum storage usage: %(formatted_file_size)s (%(raw_file_size)s MB), for user %(user)s'
        ) % {
            'formatted_file_size': filesizeformat(self._allowed()),
            'raw_file_size': self.storage_size,
            'user': user.get_full_name() or user
        }

    def process(self, **kwargs):
        if self._usage() > self._allowed():
            raise QuotaExceeded('Document count exceeded')

    def usage(self):
        return _('%(usage)s out of %(allowed)s') % {
            'usage': filesizeformat(self._usage()),
            'allowed': filesizeformat(self._allowed())
        }
