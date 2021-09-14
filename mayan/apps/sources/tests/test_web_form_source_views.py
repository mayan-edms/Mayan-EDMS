from django.test import override_settings

from mayan.apps.documents.events import (
    event_document_created, event_document_file_created,
    event_document_file_edited, event_document_version_created,
    event_document_version_page_created
)
from mayan.apps.documents.models import Document
from mayan.apps.documents.permissions import (
    permission_document_create, permission_document_file_new
)
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.documents.tests.literals import TEST_COMPRESSED_DOCUMENT_PATH

from ..source_backends.literals import SOURCE_UNCOMPRESS_CHOICE_ALWAYS

from .mixins.base_mixins import (
    DocumentFileUploadViewTestMixin, DocumentUploadWizardViewTestMixin
)
from .mixins.web_form_source_mixins import WebFormSourceTestMixin


class WebFormDocumentUploadWizardViewTestCase(
    WebFormSourceTestMixin, DocumentUploadWizardViewTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    @override_settings(DOCUMENTS_LANGUAGE='fra')
    def test_default_document_language_setting(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_create
        )
        self.grant_access(
            obj=self.test_source, permission=permission_document_create
        )

        self._clear_events()

        response = self._request_upload_interactive_view()
        self.assertContains(
            response=response,
            text='<option value="fra" selected>French</option>',
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_upload_compressed_file(self):
        backend_data = self.test_source.get_backend_data()
        backend_data['uncompress'] = SOURCE_UNCOMPRESS_CHOICE_ALWAYS
        self.test_source.set_backend_data(obj=backend_data)
        self.test_source.save()

        self.grant_access(
            obj=self.test_document_type, permission=permission_document_create
        )
        self.grant_access(
            obj=self.test_source, permission=permission_document_create
        )

        test_document_count = Document.objects.count()

        self._clear_events()

        response = self._request_upload_wizard_view(
            document_path=TEST_COMPRESSED_DOCUMENT_PATH
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Document.objects.count(), test_document_count + 2)
        self.assertTrue(
            'first document.pdf' in Document.objects.values_list(
                'label', flat=True
            )
        )
        self.assertTrue(
            'second document.pdf' in Document.objects.values_list(
                'label', flat=True
            )
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 11)

        test_documents = (Document.objects.first(), Document.objects.last())
        test_document_files = (
            test_documents[0].file_latest, test_documents[1].file_latest
        )
        test_document_versions = (
            test_documents[0].version_active, test_documents[1].version_active
        )
        test_document_version_pages = (
            test_document_versions[0].pages.first(),
            test_document_versions[1].pages.first(),
            test_document_versions[1].pages.last()
        )

        self.assertEqual(events[0].action_object, self.test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, test_documents[0])
        self.assertEqual(events[0].verb, event_document_created.id)

        self.assertEqual(events[1].action_object, test_documents[0])
        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].target, test_document_files[0])
        self.assertEqual(events[1].verb, event_document_file_created.id)

        self.assertEqual(events[2].action_object, test_documents[0])
        self.assertEqual(events[2].actor, self._test_case_user)
        self.assertEqual(events[2].target, test_document_files[0])
        self.assertEqual(events[2].verb, event_document_file_edited.id)

        self.assertEqual(events[3].action_object, test_documents[0])
        self.assertEqual(events[3].actor, self._test_case_user)
        self.assertEqual(events[3].target, test_document_versions[0])
        self.assertEqual(events[3].verb, event_document_version_created.id)

        self.assertEqual(events[4].action_object, test_document_versions[0])
        self.assertEqual(events[4].actor, self._test_case_user)
        self.assertEqual(events[4].target, test_document_version_pages[0])
        self.assertEqual(
            events[4].verb, event_document_version_page_created.id
        )

        self.assertEqual(events[5].action_object, self.test_document_type)
        self.assertEqual(events[5].actor, self._test_case_user)
        self.assertEqual(events[5].target, test_documents[1])
        self.assertEqual(events[5].verb, event_document_created.id)

        self.assertEqual(events[6].action_object, test_documents[1])
        self.assertEqual(events[6].actor, self._test_case_user)
        self.assertEqual(events[6].target, test_document_files[1])
        self.assertEqual(events[6].verb, event_document_file_created.id)

        self.assertEqual(events[7].action_object, test_documents[1])
        self.assertEqual(events[7].actor, self._test_case_user)
        self.assertEqual(events[7].target, test_document_files[1])
        self.assertEqual(events[7].verb, event_document_file_edited.id)

        self.assertEqual(events[8].action_object, test_documents[1])
        self.assertEqual(events[8].actor, self._test_case_user)
        self.assertEqual(events[8].target, test_document_versions[1])
        self.assertEqual(events[8].verb, event_document_version_created.id)

        self.assertEqual(events[9].action_object, test_document_versions[1])
        self.assertEqual(events[9].actor, self._test_case_user)
        self.assertEqual(events[9].target, test_document_version_pages[1])
        self.assertEqual(
            events[9].verb, event_document_version_page_created.id
        )

        self.assertEqual(events[10].action_object, test_document_versions[1])
        self.assertEqual(events[10].actor, self._test_case_user)
        self.assertEqual(events[10].target, test_document_version_pages[2])
        self.assertEqual(
            events[10].verb, event_document_version_page_created.id
        )

    def test_upload_interactive_view_no_permission(self):
        test_document_count = Document.objects.count()

        self._clear_events()

        response = self._request_upload_interactive_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Document.objects.count(), test_document_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_upload_interactive_view_with_document_type_access(self):
        self.grant_access(
            obj=self.test_document_type, permission=permission_document_create
        )

        test_document_count = Document.objects.count()

        self._clear_events()

        response = self._request_upload_interactive_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Document.objects.count(), test_document_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_upload_interactive_view_with_source_access(self):
        self.grant_access(
            obj=self.test_source, permission=permission_document_create
        )

        test_document_count = Document.objects.count()

        self._clear_events()

        response = self._request_upload_interactive_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Document.objects.count(), test_document_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_upload_interactive_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document_type, permission=permission_document_create
        )
        self.grant_access(
            obj=self.test_source, permission=permission_document_create
        )

        test_document_count = Document.objects.count()

        self._clear_events()

        response = self._request_upload_interactive_view()
        self.assertContains(
            response=response, text=self.test_source.label, status_code=200
        )

        self.assertEqual(Document.objects.count(), test_document_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_upload_wizard_no_permission(self):
        test_document_count = Document.objects.count()

        self._clear_events()

        response = self._request_upload_wizard_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Document.objects.count(), test_document_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_upload_wizard_with_document_type_access(self):
        self.grant_access(
            obj=self.test_document_type, permission=permission_document_create
        )

        test_document_count = Document.objects.count()

        self._clear_events()

        response = self._request_upload_wizard_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Document.objects.count(), test_document_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_upload_wizard_with_source_access(self):
        self.grant_access(
            obj=self.test_source, permission=permission_document_create
        )

        test_document_count = Document.objects.count()

        self._clear_events()

        response = self._request_upload_wizard_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Document.objects.count(), test_document_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_upload_wizard_with_full_access(self):
        self.grant_access(
            obj=self.test_document_type, permission=permission_document_create
        )
        self.grant_access(
            obj=self.test_source, permission=permission_document_create
        )

        test_document_count = Document.objects.count()

        self._clear_events()

        response = self._request_upload_wizard_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Document.objects.count(), test_document_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 5)

        test_document = Document.objects.first()
        test_document_file = test_document.file_latest
        test_document_version = test_document.version_active
        test_document_version_page = test_document_version.pages.first()

        self.assertEqual(events[0].action_object, self.test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, test_document)
        self.assertEqual(events[0].verb, event_document_created.id)

        self.assertEqual(events[1].action_object, test_document)
        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].target, test_document_file)
        self.assertEqual(events[1].verb, event_document_file_created.id)

        self.assertEqual(events[2].action_object, test_document)
        self.assertEqual(events[2].actor, self._test_case_user)
        self.assertEqual(events[2].target, test_document_file)
        self.assertEqual(events[2].verb, event_document_file_edited.id)

        self.assertEqual(events[3].action_object, test_document)
        self.assertEqual(events[3].actor, self._test_case_user)
        self.assertEqual(events[3].target, test_document_version)
        self.assertEqual(events[3].verb, event_document_version_created.id)

        self.assertEqual(events[4].action_object, test_document_version)
        self.assertEqual(events[4].actor, self._test_case_user)
        self.assertEqual(events[4].target, test_document_version_page)
        self.assertEqual(
            events[4].verb, event_document_version_page_created.id
        )


class WebFormDocumentFileUploadViewTestCase(
    DocumentFileUploadViewTestMixin, WebFormSourceTestMixin,
    GenericDocumentViewTestCase
):
    def test_document_file_upload_view_no_permission(self):
        file_count = self.test_document.files.count()

        self._clear_events()

        response = self._request_document_file_upload_view()

        self.assertEqual(response.status_code, 404)

        self.test_document.refresh_from_db()
        self.assertEqual(self.test_document.files.count(), file_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_upload_view_with_document_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_new
        )
        file_count = self.test_document.files.count()

        self._clear_events()

        response = self._request_document_file_upload_view()
        self.assertEqual(response.status_code, 404)

        self.test_document.refresh_from_db()
        self.assertEqual(self.test_document.files.count(), file_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_upload_view_with_source_access(self):
        self.grant_access(
            obj=self.test_source, permission=permission_document_file_new
        )
        file_count = self.test_document.files.count()

        self._clear_events()

        response = self._request_document_file_upload_view()
        self.assertEqual(response.status_code, 404)

        self.test_document.refresh_from_db()
        self.assertEqual(self.test_document.files.count(), file_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_upload_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_new
        )
        self.grant_access(
            obj=self.test_source, permission=permission_document_file_new
        )
        file_count = self.test_document.files.count()

        self._clear_events()

        response = self._request_document_file_upload_view()
        self.assertEqual(response.status_code, 302)

        self.test_document.refresh_from_db()
        self.assertEqual(
            self.test_document.files.count(), file_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 4)

        test_document = Document.objects.first()
        test_document_file = test_document.file_latest
        test_document_version = test_document.version_active
        test_document_version_page = test_document_version.pages.first()

        self.assertEqual(events[0].action_object, test_document)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, test_document_file)
        self.assertEqual(events[0].verb, event_document_file_created.id)

        self.assertEqual(events[1].action_object, test_document)
        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].target, test_document_file)
        self.assertEqual(events[1].verb, event_document_file_edited.id)

        self.assertEqual(events[2].action_object, test_document)
        self.assertEqual(events[2].actor, self._test_case_user)
        self.assertEqual(events[2].target, test_document_version)
        self.assertEqual(events[2].verb, event_document_version_created.id)

        self.assertEqual(events[3].action_object, test_document_version)
        self.assertEqual(events[3].actor, self._test_case_user)
        self.assertEqual(events[3].target, test_document_version_page)
        self.assertEqual(
            events[3].verb, event_document_version_page_created.id
        )

    def test_trashed_document_file_upload_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_new
        )
        self.grant_access(
            obj=self.test_source, permission=permission_document_file_new
        )
        file_count = self.test_document.files.count()

        self.test_document.delete()

        self._clear_events()

        response = self._request_document_file_upload_view()
        self.assertEqual(response.status_code, 404)

        self.test_document.refresh_from_db()
        self.assertEqual(
            self.test_document.files.count(), file_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_upload_no_source_view_no_permission(self):
        file_count = self.test_document.files.count()

        self._clear_events()

        response = self._request_document_file_upload_no_source_view()
        self.assertEqual(response.status_code, 404)

        self.test_document.refresh_from_db()
        self.assertEqual(self.test_document.files.count(), file_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_upload_no_source_view_with_document_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_new
        )
        file_count = self.test_document.files.count()

        self._clear_events()

        response = self._request_document_file_upload_no_source_view()
        self.assertEqual(response.status_code, 404)

        self.test_document.refresh_from_db()
        self.assertEqual(self.test_document.files.count(), file_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_upload_no_source_view_with_source_access(self):
        self.grant_access(
            obj=self.test_source, permission=permission_document_file_new
        )
        file_count = self.test_document.files.count()

        self._clear_events()

        response = self._request_document_file_upload_no_source_view()
        self.assertEqual(response.status_code, 404)

        self.test_document.refresh_from_db()
        self.assertEqual(self.test_document.files.count(), file_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_upload_no_source_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_new
        )
        self.grant_access(
            obj=self.test_source, permission=permission_document_file_new
        )
        file_count = self.test_document.files.count()

        self._clear_events()

        response = self._request_document_file_upload_no_source_view()
        self.assertEqual(response.status_code, 302)

        self.test_document.refresh_from_db()
        self.assertEqual(self.test_document.files.count(), file_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 4)

        test_document = Document.objects.first()
        test_document_file = test_document.file_latest
        test_document_version = test_document.version_active
        test_document_version_page = test_document_version.pages.first()

        self.assertEqual(events[0].action_object, test_document)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, test_document_file)
        self.assertEqual(events[0].verb, event_document_file_created.id)

        self.assertEqual(events[1].action_object, test_document)
        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].target, test_document_file)
        self.assertEqual(events[1].verb, event_document_file_edited.id)

        self.assertEqual(events[2].action_object, test_document)
        self.assertEqual(events[2].actor, self._test_case_user)
        self.assertEqual(events[2].target, test_document_version)
        self.assertEqual(events[2].verb, event_document_version_created.id)

        self.assertEqual(events[3].action_object, test_document_version)
        self.assertEqual(events[3].actor, self._test_case_user)
        self.assertEqual(events[3].target, test_document_version_page)
        self.assertEqual(
            events[3].verb, event_document_version_page_created.id
        )

    def test_trashed_document_file_upload_no_source_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_new
        )
        self.grant_access(
            obj=self.test_source, permission=permission_document_file_new
        )
        file_count = self.test_document.files.count()

        self.test_document.delete()

        self._clear_events()

        response = self._request_document_file_upload_no_source_view()
        self.assertEqual(response.status_code, 404)

        self.test_document.refresh_from_db()
        self.assertEqual(self.test_document.files.count(), file_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_upload_view_preserve_filename(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_new
        )
        self.grant_access(
            obj=self.test_source, permission=permission_document_file_new
        )

        file_count = self.test_document.files.count()

        self._clear_events()

        response = self._request_document_file_upload_view()
        self.assertEqual(response.status_code, 302)

        self.test_document.refresh_from_db()
        self.assertEqual(
            self.test_document.files.count(), file_count + 1
        )
        self.assertEqual(
            self.test_document.file_latest.filename,
            self.test_document_filename
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 4)

        test_document = Document.objects.first()
        test_document_file = test_document.file_latest
        test_document_version = test_document.version_active
        test_document_version_page = test_document_version.pages.first()

        self.assertEqual(events[0].action_object, test_document)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, test_document_file)
        self.assertEqual(events[0].verb, event_document_file_created.id)

        self.assertEqual(events[1].action_object, test_document)
        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].target, test_document_file)
        self.assertEqual(events[1].verb, event_document_file_edited.id)

        self.assertEqual(events[2].action_object, test_document)
        self.assertEqual(events[2].actor, self._test_case_user)
        self.assertEqual(events[2].target, test_document_version)
        self.assertEqual(events[2].verb, event_document_version_created.id)

        self.assertEqual(events[3].action_object, test_document_version)
        self.assertEqual(events[3].actor, self._test_case_user)
        self.assertEqual(events[3].target, test_document_version_page)
        self.assertEqual(
            events[3].verb, event_document_version_page_created.id
        )
