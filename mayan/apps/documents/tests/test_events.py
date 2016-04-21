# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.test import override_settings
from django.utils.six import BytesIO

from actstream.models import Action

from common.tests.test_views import GenericViewTestCase
from converter.models import Transformation
from converter.permissions import permission_transformation_delete
from user_management.tests.literals import (
    TEST_USER_PASSWORD, TEST_USER_USERNAME
)

from ..events import event_document_download, event_document_view
from ..literals import DEFAULT_DELETE_PERIOD, DEFAULT_DELETE_TIME_UNIT
from ..models import (
    DeletedDocument, Document, DocumentType, HASH_FUNCTION
)
from ..permissions import (
    permission_document_create, permission_document_delete,
    permission_document_download, permission_document_properties_edit,
    permission_document_restore, permission_document_tools,
    permission_document_trash, permission_document_type_create,
    permission_document_type_delete, permission_document_type_edit,
    permission_document_type_view, permission_document_version_revert,
    permission_document_view, permission_empty_trash
)

from .literals import (
    TEST_DOCUMENT_TYPE, TEST_DOCUMENT_TYPE_QUICK_LABEL,
    TEST_SMALL_DOCUMENT_CHECKSUM, TEST_SMALL_DOCUMENT_PATH
)
from .test_views import GenericDocumentViewTestCase


TEST_DOCUMENT_TYPE_EDITED_LABEL = 'test document type edited label'
TEST_DOCUMENT_TYPE_2_LABEL = 'test document type 2 label'
TEST_TRANSFORMATION_NAME = 'rotate'
TEST_TRANSFORMATION_ARGUMENT = 'degrees: 180'



class DocumentEventsTestCase(GenericDocumentViewTestCase):
    def test_document_download_event_no_permissions(self):
        self.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD
        )

        Action.objects.all().delete()

        response = self.post(
            'documents:document_download', args=(self.document.pk,)
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(list(Action.objects.any(obj=self.document)), [])

    def test_document_download_event_with_permissions(self):
        self.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD
        )

        Action.objects.all().delete()

        self.role.permissions.add(
            permission_document_download.stored_permission
        )
        response = self.post(
            'documents:document_download', args=(self.document.pk,),
        )

        event = Action.objects.any(obj=self.document).first()

        self.assertEqual(event.verb, event_document_download.name)
        self.assertEqual(event.target, self.document)
        self.assertEqual(event.actor, self.user)

    def test_document_view_event_no_permissions(self):
        self.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD
        )

        Action.objects.all().delete()

        response = self.get(
            'documents:document_preview', args=(self.document.pk,)
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(list(Action.objects.any(obj=self.document)), [])

    def test_document_view_event_with_permissions(self):
        self.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD
        )

        Action.objects.all().delete()

        self.role.permissions.add(
            permission_document_view.stored_permission
        )
        response = self.get(
            'documents:document_preview', args=(self.document.pk,),
        )

        event = Action.objects.any(obj=self.document).first()

        self.assertEqual(event.verb, event_document_view.name)
        self.assertEqual(event.target, self.document)
        self.assertEqual(event.actor, self.user)
