from django.contrib.contenttypes.models import ContentType

from mayan.apps.document_states.tests.base import ActionTestCase
from mayan.apps.documents.permissions import permission_document_view

from ..workflow_actions import (
    GrantAccessAction, GrantDocumentAccessAction, RevokeAccessAction,
    RevokeDocumentAccessAction
)


class ACLActionTestCase(ActionTestCase):
    def test_grant_access_action(self):
        action = GrantAccessAction(
            form_data={
                'content_type': ContentType.objects.get_for_model(
                    model=self.test_document
                ).pk,
                'object_id': self.test_document.pk,
                'roles': [self._test_case_role.pk],
                'permissions': [permission_document_view.pk],
            }
        )
        action.execute(context={'entry_log': self.entry_log})

        self.assertEqual(self.test_document.acls.count(), 1)
        self.assertEqual(
            list(self.test_document.acls.first().permissions.all()),
            [permission_document_view.stored_permission]
        )
        self.assertEqual(
            self.test_document.acls.first().role, self._test_case_role
        )

    def test_grant_document_access_action(self):
        action = GrantDocumentAccessAction(
            form_data={
                'roles': [self._test_case_role.pk],
                'permissions': [permission_document_view.pk],
            }
        )
        action.execute(context={'document': self.test_document})

        self.assertEqual(self.test_document.acls.count(), 1)
        self.assertEqual(
            list(self.test_document.acls.first().permissions.all()),
            [permission_document_view.stored_permission]
        )
        self.assertEqual(
            self.test_document.acls.first().role, self._test_case_role
        )

    def test_revoke_access_action(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        action = RevokeAccessAction(
            form_data={
                'content_type': ContentType.objects.get_for_model(
                    model=self.test_document
                ).pk,
                'object_id': self.test_document.pk,
                'roles': [self._test_case_role.pk],
                'permissions': [permission_document_view.pk],
            }
        )
        action.execute(context={'entry_log': self.entry_log})

        self.assertEqual(self.test_document.acls.count(), 0)

    def test_revoke_document_access_action(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        action = RevokeDocumentAccessAction(
            form_data={
                'roles': [self._test_case_role.pk],
                'permissions': [permission_document_view.pk],
            }
        )
        action.execute(context={'document': self.test_document})

        self.assertEqual(self.test_document.acls.count(), 0)
