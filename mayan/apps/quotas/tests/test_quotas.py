import logging

from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.user_management.tests.mixins import GroupTestMixin

from ..exceptions import QuotaExceeded
from ..quota_backends import DocumentCountQuota, DocumentSizeQuota


class DocumentCountQuotaTestCase(GroupTestMixin, GenericDocumentTestCase):
    auto_upload_test_document = False

    def setUp(self):
        super(DocumentCountQuotaTestCase, self).setUp()
        # Increase the initial usage count to 1 by uploading a document
        # as the test case user.
        self._upload_test_document(_user=self._test_case_user)
        self.test_case_silenced_logger_new_level = logging.FATAL + 10
        self._silence_logger(name='mayan.apps.documents.models')

    def test_user_all_document_type_all(self):
        self.test_quota = DocumentCountQuota.create(
            documents_limit=1,
            document_type_all=True,
            document_type_ids=(),
            group_ids=(),
            user_all=True,
            user_ids=(),
        )

        with self.assertRaises(expected_exception=QuotaExceeded):
            self._upload_test_document()

    def test_user_all_document_type_all_two_users(self):
        self.test_quota = DocumentCountQuota.create(
            documents_limit=1,
            document_type_all=True,
            document_type_ids=(),
            group_ids=(),
            user_all=True,
            user_ids=(),
        )
        self._create_test_user()

        with self.assertRaises(expected_exception=QuotaExceeded):
            self._upload_test_document(_user=self.test_user)

    def test_user_all_document_type_test(self):
        self.test_quota = DocumentCountQuota.create(
            documents_limit=1,
            document_type_all=False,
            document_type_ids=(self.test_document_type.pk,),
            group_ids=(),
            user_all=True,
            user_ids=(),
        )

        with self.assertRaises(expected_exception=QuotaExceeded):
            self._upload_test_document()

    def test_user_test_document_type_all(self):
        self.test_quota = DocumentCountQuota.create(
            documents_limit=1,
            document_type_all=True,
            document_type_ids=(),
            group_ids=(),
            user_all=False,
            user_ids=(self._test_case_user.pk,),
        )

        with self.assertRaises(expected_exception=QuotaExceeded):
            self._upload_test_document(_user=self._test_case_user)

    def test_group_test_document_type_all(self):
        self._create_test_group()
        self._test_case_user.groups.add(self.test_group)

        self.test_quota = DocumentCountQuota.create(
            documents_limit=1,
            document_type_all=True,
            document_type_ids=(),
            group_ids=(self.test_group.pk,),
            user_all=False,
            user_ids=(),
        )

        with self.assertRaises(expected_exception=QuotaExceeded):
            self._upload_test_document(_user=self._test_case_user)

    def test_allow(self):
        self.test_quota = DocumentCountQuota.create(
            documents_limit=1,
            document_type_all=True,
            document_type_ids=(),
            group_ids=(),
            user_all=False,
            user_ids=(),
        )

        self._upload_test_document(_user=self._test_case_user)

    def test_super_user_restriction(self):
        self._create_test_superuser()

        self.test_quota = DocumentCountQuota.create(
            documents_limit=1,
            document_type_all=True,
            document_type_ids=(),
            group_ids=(),
            user_all=True,
            user_ids=(),
        )

        self._upload_test_document(_user=self.test_superuser)


class DocumentSizeQuotaTestCase(GroupTestMixin, GenericDocumentTestCase):
    auto_upload_test_document = False

    def setUp(self):
        super(DocumentSizeQuotaTestCase, self).setUp()
        self.test_case_silenced_logger_new_level = logging.FATAL + 10
        self._silence_logger(name='mayan.apps.documents.models')

    def test_user_all_document_type_all(self):
        self.test_quota = DocumentSizeQuota.create(
            document_size_limit=0.01,
            document_type_all=True,
            document_type_ids=(),
            group_ids=(),
            user_all=True,
            user_ids=(),
        )

        with self.assertRaises(expected_exception=QuotaExceeded):
            self._upload_test_document()

    def test_user_all_document_type_test(self):
        self.test_quota = DocumentSizeQuota.create(
            document_size_limit=0.01,
            document_type_all=False,
            document_type_ids=(self.test_document_type.pk,),
            group_ids=(),
            user_all=True,
            user_ids=(),
        )

        with self.assertRaises(expected_exception=QuotaExceeded):
            self._upload_test_document()

    def test_user_test_document_type_test(self):
        self.test_quota = DocumentSizeQuota.create(
            document_size_limit=0.01,
            document_type_all=False,
            document_type_ids=(self.test_document_type.pk,),
            group_ids=(),
            user_all=False,
            user_ids=(self._test_case_user.pk,),
        )

        with self.assertRaises(expected_exception=QuotaExceeded):
            self._upload_test_document(_user=self._test_case_user)

    def test_group_test_document_type_test(self):
        self._create_test_group()
        self._test_case_user.groups.add(self.test_group)

        self.test_quota = DocumentSizeQuota.create(
            document_size_limit=0.01,
            document_type_all=False,
            document_type_ids=(self.test_document_type.pk,),
            group_ids=(self.test_group.pk,),
            user_all=False,
            user_ids=(),
        )

        with self.assertRaises(expected_exception=QuotaExceeded):
            self._upload_test_document(_user=self._test_case_user)

    def test_allow(self):
        self.test_quota = DocumentSizeQuota.create(
            document_size_limit=0.01,
            document_type_all=False,
            document_type_ids=(),
            group_ids=(),
            user_all=False,
            user_ids=(),
        )

        self._upload_test_document(_user=self._test_case_user)

    def test_super_user_restriction(self):
        self._create_test_superuser()

        self.test_quota = DocumentSizeQuota.create(
            document_size_limit=0.01,
            document_type_all=True,
            document_type_ids=(),
            group_ids=(),
            user_all=True,
            user_ids=(),
        )

        self._upload_test_document(_user=self.test_superuser)
