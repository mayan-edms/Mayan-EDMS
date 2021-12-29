from django.apps import apps
from django.db.models.signals import post_migrate, post_save

from mayan.apps.documents.signals import signal_post_document_file_upload
from mayan.apps.testing.tests.base import MayanMigratorTestCase

from .mixins.document_mixins import DocumentTestMixin


class DocumentsAppMigrationTestCase(
    DocumentTestMixin, MayanMigratorTestCase
):
    auto_create_test_document_type = False
    auto_create_test_document = False
    auto_delete_test_document_type = False
    migrate_from = ('documents', '0055_auto_20200814_0626')
    migrate_to = ('documents', '0075_delete_duplicateddocumentold')

    def setUp(self):
        self.clear_signals_and_hooks()
        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.restore_signals_and_hooks()

    def clear_signals_and_hooks(self):
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        DocumentFile = apps.get_model(
            app_label='documents', model_name='DocumentFile'
        )

        self.document_file_hooks_pre_create = DocumentFile._hooks_pre_create
        DocumentFile._hooks_pre_create = []

        self.document_file_pre_open_hooks = DocumentFile._pre_open_hooks
        DocumentFile._pre_open_hooks = []

        self.document_file_pre_save_hooks = DocumentFile._pre_save_hooks
        DocumentFile._pre_save_hooks = []

        self.document_file_post_save_hooks = DocumentFile._post_save_hooks
        DocumentFile._post_save_hooks = []

        self.document_hooks_pre_create = Document._hooks_pre_create
        Document._hooks_pre_create = []

        self.signal_post_document_file_upload_receivers = signal_post_document_file_upload.receivers
        signal_post_document_file_upload.receivers = []
        signal_post_document_file_upload.sender_receivers_cache.clear()

        self.post_save_receivers = post_save.receivers
        post_save.receivers = []
        post_save.sender_receivers_cache.clear()

        self.post_migrate_receivers = post_migrate.receivers
        post_migrate.receivers = []
        post_migrate.sender_receivers_cache.clear()

    def restore_signals_and_hooks(self):
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        DocumentFile = apps.get_model(
            app_label='documents', model_name='DocumentFile'
        )

        DocumentFile._hooks_pre_create = self.document_file_hooks_pre_create
        DocumentFile._pre_open_hooks = self.document_file_pre_open_hooks
        DocumentFile._pre_save_hooks = self.document_file_pre_save_hooks
        DocumentFile._post_save_hooks = self.document_file_post_save_hooks
        Document._hooks_pre_create = self.document_hooks_pre_create

        signal_post_document_file_upload.receivers = self.signal_post_document_file_upload_receivers
        signal_post_document_file_upload.sender_receivers_cache.clear()

        post_save.receivers = self.post_save_receivers
        post_save.sender_receivers_cache.clear()

        post_migrate.receivers = self.post_migrate_receivers
        post_migrate.sender_receivers_cache.clear()

    def prepare(self):
        DocumentType = self.old_state.apps.get_model(
            app_label='documents', model_name='DocumentType'
        )
        Document = self.old_state.apps.get_model(
            app_label='documents', model_name='Document'
        )
        DocumentVersion = self.old_state.apps.get_model(
            app_label='documents', model_name='DocumentVersion'
        )
        DocumentPage = self.old_state.apps.get_model(
            app_label='documents', model_name='DocumentPage'
        )

        self._test_document_type = DocumentType.objects.create(
            label='test document type'
        )
        self._test_document = Document.objects.create(
            document_type=self._test_document_type, label='test document'
        )

        self._test_document_versions = []
        self._test_document_versions.append(
            DocumentVersion.objects.create(document_id=self._test_document.pk)
        )
        self._test_document_versions.append(
            DocumentVersion.objects.create(document_id=self._test_document.pk)
        )

        DocumentPage.objects.create(
            document_version_id=self._test_document_versions[0].pk
        )
        DocumentPage.objects.create(
            document_version_id=self._test_document_versions[1].pk
        )

    def test_single_active_version(self):
        DocumentFile = self.new_state.apps.get_model(
            app_label='documents', model_name='DocumentFile'
        )
        DocumentVersion = self.new_state.apps.get_model(
            app_label='documents', model_name='DocumentVersion'
        )

        self.assertEqual(DocumentFile.objects.count(), 2)

        self.assertEqual(DocumentVersion.objects.count(), 2)

        self.assertEqual(
            DocumentVersion.objects.filter(active=True).count(), 1
        )
