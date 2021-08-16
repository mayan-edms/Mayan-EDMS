import json
import shutil

from django.db.models import Q

from mayan.apps.documents.literals import DOCUMENT_FILE_ACTION_PAGES_NEW
from mayan.apps.documents.tests.literals import TEST_SMALL_DOCUMENT_PATH
from mayan.apps.storage.utils import fs_cleanup, mkdtemp

from ..forms import NewDocumentForm
from ..models import Source
from ..source_backends.email_backends import (
    SourceBackendIMAPEmail, SourceBackendPOP3Email
)
from ..source_backends.literals import (
    DEFAULT_EMAIL_IMAP_MAILBOX, DEFAULT_EMAIL_IMAP_SEARCH_CRITERIA,
    DEFAULT_EMAIL_IMAP_STORE_COMMANDS, DEFAULT_EMAIL_METADATA_ATTACHMENT_NAME,
    DEFAULT_EMAIL_POP3_TIMEOUT, DEFAULT_PERIOD_INTERVAL,
    SOURCE_UNCOMPRESS_CHOICE_NEVER
)
from ..source_backends.staging_folder_backends import SourceBackendStagingFolder
from ..source_backends.watch_folder_backends import SourceBackendWatchFolder
from ..source_backends.web_form_backends import SourceBackendWebForm

from .literals import (
    TEST_SOURCE_BACKEND_PATH, TEST_SOURCE_BACKEND_EMAIL_PATH,
    TEST_SOURCE_BACKEND_PERIODIC_PATH, TEST_SOURCE_LABEL,
    TEST_SOURCE_LABEL_EDITED, TEST_STAGING_PREVIEW_HEIGHT,
    TEST_STAGING_PREVIEW_WIDTH
)

from .mocks import MockRequest


class DocumentFileUploadViewTestMixin:
    def _request_document_file_upload_view(self):
        with open(file=TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            return self.post(
                viewname='sources:document_file_upload', kwargs={
                    'document_id': self.test_document.pk,
                    'source_id': self.test_source.pk,
                }, data={
                    'document-action': DOCUMENT_FILE_ACTION_PAGES_NEW,
                    'source-file': file_object
                }
            )

    def _request_document_file_upload_no_source_view(self):
        with open(file=TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            return self.post(
                viewname='sources:document_file_upload', kwargs={
                    'document_id': self.test_document.pk,
                }, data={
                    'document-action': DOCUMENT_FILE_ACTION_PAGES_NEW,
                    'source-file': file_object
                }
            )


class DocumentUploadWizardViewTestMixin:
    def _request_upload_interactive_view(self):
        return self.get(
            viewname='sources:document_upload_interactive', data={
                'document_type_id': self.test_document_type.pk,
            }
        )

    def _request_upload_wizard_view(self, document_path=TEST_SMALL_DOCUMENT_PATH):
        with open(file=document_path, mode='rb') as file_object:
            return self.post(
                viewname='sources:document_upload_interactive', kwargs={
                    'source_id': self.test_source.pk
                }, data={
                    'source-file': file_object,
                    'document_type_id': self.test_document_type.pk,
                }
            )


class SourceTestMixin:
    _create_source_method = '_create_test_source'
    auto_create_test_source = True

    def setUp(self):
        super().setUp()
        self._test_sources = []

        if self.auto_create_test_source:
            getattr(self, self._create_source_method)()

    def _create_test_source(self, backend_path=None, backend_data=None):
        total_test_sources = len(self._test_sources)
        label = '{}_{}'.format(TEST_SOURCE_LABEL, total_test_sources)

        self.test_source = Source.objects.create(
            backend_path=backend_path or TEST_SOURCE_BACKEND_PATH,
            backend_data=json.dumps(obj=backend_data or {}),
            label=label
        )
        self._test_sources.append(self.test_source)


class EmailSourceBackendTestMixin(SourceTestMixin):
    def _create_test_email_source_backend(self, extra_data=None):
        backend_data = {
            'document_type_id': self.test_document_type.pk,
            'from_metadata_type_id': None,
            'host': '',
            'interval': DEFAULT_PERIOD_INTERVAL,
            'metadata_attachment_name': DEFAULT_EMAIL_METADATA_ATTACHMENT_NAME,
            'password': '',
            'port': '',
            'ssl': True,
            'subject_metadata_type_id': None,
            'store_body': False,
            'username': ''
        }

        if extra_data:
            backend_data.update(extra_data)

        self._create_test_source(
            backend_path=TEST_SOURCE_BACKEND_EMAIL_PATH,
            backend_data=backend_data
        )


class IMAPEmailSourceTestMixin(SourceTestMixin):
    _create_source_method = '_create_test_imap_email_source'

    def _create_test_imap_email_source(self, extra_data=None):
        backend_data = {
            'document_type_id': self.test_document_type.pk,
            'execute_expunge': True,
            'from_metadata_type_id': None,
            'host': '',
            'interval': DEFAULT_PERIOD_INTERVAL,
            'mailbox': DEFAULT_EMAIL_IMAP_MAILBOX,
            'mailbox_destination': '',
            'metadata_attachment_name': DEFAULT_EMAIL_METADATA_ATTACHMENT_NAME,
            'password': '',
            'port': '',
            'search_criteria': DEFAULT_EMAIL_IMAP_SEARCH_CRITERIA,
            'ssl': True,
            'store_body': False,
            'store_commands': DEFAULT_EMAIL_IMAP_STORE_COMMANDS,
            'subject_metadata_type_id': None,
            'uncompress': SOURCE_UNCOMPRESS_CHOICE_NEVER,
            'username': ''
        }

        if extra_data:
            backend_data.update(extra_data)

        self._create_test_source(
            backend_path=SourceBackendIMAPEmail.get_class_path(),
            backend_data=backend_data
        )


class InteractiveSourceBackendTestMixin:
    class MockSourceForm:
        def __init__(self, **kwargs):
            self.cleaned_data = kwargs

    def setUp(self):
        super().setUp()
        self.test_document_form = self.get_test_document_form()

    def get_test_document_form(self):
        document_form = NewDocumentForm(
            data={}, document_type=self.test_document_type
        )
        document_form.full_clean()

        return document_form

    def get_test_request(self):
        return MockRequest(user=self._test_case_user)


class PeriodicSourceBackendTestMixin(SourceTestMixin):
    _create_source_method = '_create_test_periodic_source_backend'

    def _create_test_periodic_source_backend(self, extra_data=None):
        backend_data = {
            'interval': DEFAULT_PERIOD_INTERVAL
        }

        if extra_data:
            backend_data.update(extra_data)

        self._create_test_source(
            backend_path=TEST_SOURCE_BACKEND_PERIODIC_PATH,
            backend_data=backend_data
        )


class POP3EmailSourceTestMixin(SourceTestMixin):
    _create_source_method = '_create_test_pop3_email_source'

    def _create_test_pop3_email_source(self, extra_data=None):
        backend_data = {
            'document_type_id': self.test_document_type.pk,
            'from_metadata_type_id': None,
            'host': '',
            'interval': DEFAULT_PERIOD_INTERVAL,
            'metadata_attachment_name': DEFAULT_EMAIL_METADATA_ATTACHMENT_NAME,
            'password': '',
            'port': '',
            'ssl': True,
            'store_body': False,
            'subject_metadata_type_id': None,
            'timeout': DEFAULT_EMAIL_POP3_TIMEOUT,
            'uncompress': SOURCE_UNCOMPRESS_CHOICE_NEVER,
            'username': ''
        }

        if extra_data:
            backend_data.update(extra_data)

        self._create_test_source(
            backend_path=SourceBackendPOP3Email.get_class_path(),
            backend_data=backend_data
        )


class SourceAPIViewTestMixin:
    def _request_test_source_create_api_view(
        self, backend_path=None, extra_data=None
    ):
        pk_list = list(Source.objects.values_list('pk', flat=True))

        data = {
            'backend_path': backend_path or TEST_SOURCE_BACKEND_PATH,
            'enabled': True,
            'label': TEST_SOURCE_LABEL
        }

        if extra_data:
            data.update(extra_data)

        response = self.post(viewname='rest_api:source-list', data=data)

        try:
            self.test_source = Source.objects.get(~Q(pk__in=pk_list))
        except Source.DoesNotExist:
            self.test_source = None

        return response

    def _request_test_source_delete_api_view(self):
        return self.delete(
            viewname='rest_api:source-detail', kwargs={
                'source_id': self.test_source.pk
            }
        )

    def _request_test_source_edit_api_view_via_patch(self):
        return self.patch(
            viewname='rest_api:source-detail', kwargs={
                'source_id': self.test_source.pk
            }, data={'label': TEST_SOURCE_LABEL_EDITED}
        )

    def _request_test_source_edit_api_view_via_put(self):
        data = {
            'backend_path': self.test_source.backend_path,
            'enabled': self.test_source.enabled,
            'label': TEST_SOURCE_LABEL_EDITED
        }

        return self.put(
            viewname='rest_api:source-detail', kwargs={
                'source_id': self.test_source.pk
            }, data=data
        )

    def _request_test_source_list_api_view(self):
        return self.get(viewname='rest_api:source-list')


class SourceViewTestMixin:
    def _request_test_source_backend_selection_view(self):
        return self.get(
            viewname='sources:source_backend_selection'
        )

    def _request_test_source_create_view(
        self, backend_path=None, extra_data=None
    ):
        pk_list = list(Source.objects.values_list('pk', flat=True))

        data = {
            'enabled': True,
            'label': TEST_SOURCE_LABEL,
            'uncompress': SOURCE_UNCOMPRESS_CHOICE_NEVER
        }

        if extra_data:
            data.update(extra_data)

        response = self.post(
            kwargs={
                'backend_path': backend_path or TEST_SOURCE_BACKEND_PATH
            }, viewname='sources:source_create', data=data
        )

        try:
            self.test_source = Source.objects.get(~Q(pk__in=pk_list))
        except Source.DoesNotExist:
            self.test_source = None

        return response

    def _request_test_source_delete_view(self):
        return self.post(
            viewname='sources:source_delete', kwargs={
                'source_id': self.test_source.pk
            }
        )

    def _request_test_source_edit_view(self):
        return self.post(
            viewname='sources:source_edit', kwargs={
                'source_id': self.test_source.pk
            }, data={
                'label': TEST_SOURCE_LABEL_EDITED
            }
        )

    def _request_test_source_list_view(self):
        return self.get(viewname='sources:source_list')

    def _request_test_source_test_get_view(self):
        return self.get(
            viewname='sources:source_test', kwargs={
                'source_id': self.test_source.pk
            }
        )

    def _request_test_source_test_post_view(self):
        return self.post(
            viewname='sources:source_test', kwargs={
                'source_id': self.test_source.pk
            }
        )


class StagingFolderActionAPIViewTestMixin:
    def _request_test_staging_folder_file_delete_action_api_view(self):
        return self.post(
            viewname='rest_api:source-action', kwargs={
                'action_name': 'file_delete', 'source_id': self.test_source.pk
            }, data={
                'arguments': json.dumps(
                    obj={
                        'encoded_filename': self.test_staging_folder_file.encoded_filename
                    }
                )
            }
        )

    def _request_test_staging_folder_file_image_action_api_view(self):
        return self.get(
            viewname='rest_api:source-action', kwargs={
                'action_name': 'file_image', 'source_id': self.test_source.pk
            }, query={'encoded_filename': self.test_staging_folder_file.encoded_filename}
        )

    def _request_test_staging_folder_file_list_action_api_view(self):
        return self.get(
            viewname='rest_api:source-action', kwargs={
                'action_name': 'file_list', 'source_id': self.test_source.pk
            }
        )

    def _request_test_staging_folder_file_upload_action_api_view(self):
        return self.post(
            viewname='rest_api:source-action', kwargs={
                'action_name': 'file_upload', 'source_id': self.test_source.pk
            }, data={
                'arguments': json.dumps(
                    obj={
                        'document_type_id': self.test_document_type.pk,
                        'encoded_filename': self.test_staging_folder_file.encoded_filename
                    }
                )
            }
        )


class StagingFolderTestMixin(SourceTestMixin):
    _create_source_method = '_create_test_staging_folder'

    def tearDown(self):
        fs_cleanup(filename=self.test_source.get_backend_data()['folder_path'])
        super().tearDown()

    def _create_test_staging_folder(self, extra_data=None):
        backend_data = {
            'folder_path': mkdtemp(),
            'preview_width': TEST_STAGING_PREVIEW_WIDTH,
            'preview_height': TEST_STAGING_PREVIEW_HEIGHT,
            'uncompress': SOURCE_UNCOMPRESS_CHOICE_NEVER
        }

        if extra_data:
            backend_data.update(extra_data)

        self._create_test_source(
            backend_path=SourceBackendStagingFolder.get_class_path(),
            backend_data=backend_data
        )

    def _copy_test_staging_folder_document(self):
        shutil.copy(
            src=TEST_SMALL_DOCUMENT_PATH,
            dst=self.test_source.get_backend_data()['folder_path']
        )
        self.test_staging_folder_file = list(
            self.test_source.get_backend_instance().get_files()
        )[0]


class EmailSourceBackendViewTestMixin(SourceViewTestMixin):
    def _request_test_email_source_create_view(self, extra_data=None):
        data = {
            'document_type_id': self.test_document_type.pk,
            'host': '127.0.0.1',
            'interval': DEFAULT_PERIOD_INTERVAL,
            'metadata_attachment_name': DEFAULT_EMAIL_METADATA_ATTACHMENT_NAME,
            'port': '0',
            'ssl': True,
            'store_body': False,
            'username': 'username'
        }

        if extra_data:
            data.update(extra_data)

        return self._request_test_source_create_view(
            backend_path=TEST_SOURCE_BACKEND_EMAIL_PATH, extra_data=data
        )


class WatchFolderTestMixin(SourceTestMixin):
    def setUp(self):
        super().setUp()
        self.temporary_directory = mkdtemp()
        self.test_watch_folders = []

    def tearDown(self):
        shutil.rmtree(path=self.temporary_directory)
        super().tearDown()

    def _create_test_watchfolder(self, extra_data=None):
        backend_data = {
            'document_type_id': self.test_document_type.pk,
            'folder_path': self.temporary_directory,
            'include_subdirectories': False,
            'interval': DEFAULT_PERIOD_INTERVAL,
            'uncompress': SOURCE_UNCOMPRESS_CHOICE_NEVER
        }

        if extra_data:
            backend_data.update(extra_data)

        self._create_test_source(
            backend_path=SourceBackendWatchFolder.get_class_path(),
            backend_data=backend_data
        )


class WebFormSourceTestMixin(SourceTestMixin):
    _create_source_method = '_create_test_web_form_source'

    def _create_test_web_form_source(self, extra_data=None):
        backend_data = {'uncompress': SOURCE_UNCOMPRESS_CHOICE_NEVER}

        if extra_data:
            backend_data.update(extra_data)

        self._create_test_source(
            backend_path=SourceBackendWebForm.get_class_path(),
            backend_data=backend_data
        )
