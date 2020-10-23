import logging

from mayan.apps.documents.models.document_models import Document
from mayan.apps.documents.permissions import (
    permission_document_create, permission_document_new_version
)
from mayan.apps.documents.tests.base import DocumentTestMixin
from mayan.apps.documents.tests.literals import TEST_SMALL_DOCUMENT_PATH
from mayan.apps.sources.tests.mixins import (
    DocumentUploadWizardViewTestMixin, DocumentVersionUploadViewTestMixin,
    SourceTestMixin
)
from mayan.apps.testing.tests.base import GenericViewTestCase

from ..classes import QuotaBackend
from ..exceptions import QuotaExceeded
from ..quota_backends import DocumentCountQuota, DocumentSizeQuota


class QuotaHooksTestCase(
    DocumentTestMixin, DocumentUploadWizardViewTestMixin,
    DocumentVersionUploadViewTestMixin, SourceTestMixin, GenericViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super(QuotaHooksTestCase, self).setUp()
        # Increase the initial usage count to 1 by uploading a document
        # as the test case user.
        self._upload_test_document(_user=self._test_case_user)
        self.test_case_silenced_logger_new_level = logging.FATAL + 10
        self._silence_logger(name='mayan.apps.sources.views')
        self._silence_logger(name='mayan.apps.logging.middleware.error_logging')

    def tearDown(self):
        QuotaBackend.connect_signals()
        super(QuotaHooksTestCase, self).tearDown()

    def test_document_quantity_quota_and_source_upload_wizard_view_with_permission(self):
        self.test_quota_backend = DocumentCountQuota

        self.test_quota = DocumentCountQuota.create(
            documents_limit=1,
            document_type_all=True,
            document_type_ids=(),
            group_ids=(),
            user_all=True,
            user_ids=(),
        )

        self.test_quota_backend.signal.disconnect(
            dispatch_uid='quotas_handler_process_signal',
            sender=self.test_quota_backend.sender
        )

        self.grant_permission(permission=permission_document_create)

        document_count = Document.objects.count()

        with self.assertRaises(expected_exception=QuotaExceeded):
            self._request_upload_wizard_view()

        self.assertEqual(Document.objects.count(), document_count)

    def test_document_size_quota_and_source_upload_wizard_view_with_permission(self):
        self.test_quota_backend = DocumentSizeQuota

        self.test_quota = DocumentSizeQuota.create(
            document_size_limit=0.01,
            document_type_all=True,
            document_type_ids=(),
            group_ids=(),
            user_all=True,
            user_ids=(),
        )

        self.test_quota_backend.signal.disconnect(
            dispatch_uid='quotas_handler_process_signal',
            sender=self.test_quota_backend.sender
        )

        self.grant_permission(permission=permission_document_create)

        document_count = Document.objects.count()

        with self.assertRaises(expected_exception=QuotaExceeded):
            self._request_upload_wizard_view()

        self.assertEqual(Document.objects.count(), document_count)

    def test_document_size_quota_and_document_version_upload_with_access(self):
        self.test_quota_backend = DocumentSizeQuota

        self.test_quota = DocumentSizeQuota.create(
            document_size_limit=0.01,
            document_type_all=True,
            document_type_ids=(),
            group_ids=(),
            user_all=True,
            user_ids=(),
        )

        self.test_quota_backend.signal.disconnect(
            dispatch_uid='quotas_handler_process_signal',
            sender=self.test_quota_backend.sender
        )

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_new_version
        )
        version_count = self.test_document.versions.count()

        with self.assertRaises(expected_exception=QuotaExceeded):
            with open(file=TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
                self._request_document_version_upload_view(
                    source_file=file_object
                )

        self.test_document.refresh_from_db()
        self.assertEqual(
            self.test_document.versions.count(), version_count
        )
