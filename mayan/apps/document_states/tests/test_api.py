from __future__ import absolute_import, unicode_literals

from django.test import override_settings

from rest_framework import status

from documents.models import DocumentType
from documents.permissions import permission_document_type_view
from documents.tests.literals import (
    TEST_DOCUMENT_TYPE_LABEL, TEST_SMALL_DOCUMENT_PATH
)
from rest_api.tests import BaseAPITestCase

from ..models import Workflow
from ..permissions import (
    permission_workflow_create, permission_workflow_delete,
    permission_workflow_edit, permission_workflow_transition,
    permission_workflow_view
)

from .literals import (
    TEST_WORKFLOW_INTERNAL_NAME, TEST_WORKFLOW_INITIAL_STATE_COMPLETION,
    TEST_WORKFLOW_INITIAL_STATE_LABEL,
    TEST_WORKFLOW_INSTANCE_LOG_ENTRY_COMMENT, TEST_WORKFLOW_LABEL,
    TEST_WORKFLOW_LABEL_EDITED, TEST_WORKFLOW_STATE_COMPLETION,
    TEST_WORKFLOW_STATE_LABEL, TEST_WORKFLOW_STATE_LABEL_EDITED,
    TEST_WORKFLOW_TRANSITION_LABEL, TEST_WORKFLOW_TRANSITION_LABEL_EDITED
)


@override_settings(OCR_AUTO_OCR=False)
class WorkflowAPITestCase(BaseAPITestCase):
    def setUp(self):
        super(WorkflowAPITestCase, self).setUp()
        self.login_user()

        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )

        with open(TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            self.document = self.document_type.new_document(
                file_object=file_object
            )

    def tearDown(self):
        if hasattr(self, 'document_type'):
            self.document_type.delete()
        super(WorkflowAPITestCase, self).tearDown()

    def _create_workflow(self):
        return Workflow.objects.create(
            label=TEST_WORKFLOW_LABEL,
            internal_name=TEST_WORKFLOW_INTERNAL_NAME
        )

    def _request_workflow_create_view(self):
        return self.post(
            viewname='rest_api:workflow-list', data={
                'label': TEST_WORKFLOW_LABEL
            }
        )

    def test_workflow_create_view_no_permission(self):
        response = self._request_workflow_create_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Workflow.objects.count(), 0)

    def test_workflow_create_view_with_permission(self):
        self.grant_permission(permission=permission_workflow_create)
        response = self._request_workflow_create_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Workflow.objects.count(), 1)
        self.assertEqual(
            response.data['label'], TEST_WORKFLOW_LABEL
        )

    def _request_workflow_create_view_with_document_type(self):
        return self.post(
            viewname='rest_api:workflow-list', data={
                'label': TEST_WORKFLOW_LABEL,
                'document_types_pk_list': '{}'.format(self.document_type.pk)
            }
        )

    def test_workflow_create_with_document_type_view_no_permission(self):
        response = self._request_workflow_create_view_with_document_type()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Workflow.objects.count(), 0)

    def test_workflow_create_with_document_type_view_with_permission(self):
        self.grant_permission(permission=permission_workflow_create)
        response = self._request_workflow_create_view_with_document_type()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Workflow.objects.count(), 1)
        workflow = Workflow.objects.first()
        self.assertQuerysetEqual(
            workflow.document_types.all(), (repr(self.document_type),)
        )
        self.assertEqual(response.data['id'], workflow.pk)

    def _request_workflow_delete_view(self):
        return self.delete(
            viewname='rest_api:workflow-detail', args=(self.workflow.pk,)
        )

    def test_workflow_delete_view_no_permission(self):
        self.workflow = self._create_workflow()
        response = self._request_workflow_delete_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Workflow.objects.count(), 1)

    def test_workflow_delete_view_with_permission(self):
        self.workflow = self._create_workflow()
        self.grant_access(
            permission=permission_workflow_delete, obj=self.workflow
        )
        response = self._request_workflow_delete_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Workflow.objects.count(), 0)

    def _request_workflow_detail_view(self):
        return self.get(
            viewname='rest_api:workflow-detail', args=(self.workflow.pk,)
        )

    def test_workflow_detail_view_no_access(self):
        self.workflow = self._create_workflow()
        response = self._request_workflow_detail_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse('label' in response.data)

    def test_workflow_detail_view_with_access(self):
        self.workflow = self._create_workflow()
        self.grant_access(permission=permission_workflow_view, obj=self.workflow)
        response = self._request_workflow_detail_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['label'], self.workflow.label)

    def _request_workflow_document_type_list_create_view(self):
        return self.post(
            viewname='rest_api:workflow-document-type-list',
            args=(self.workflow.pk,), data={
                'document_type_pk': self.document_type.pk
            }
        )

    def test_workflow_document_type_create_view_no_access(self):
        self.workflow = self._create_workflow()
        response = self._request_workflow_document_type_list_create_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.workflow.document_types.count(), 0)

    def test_workflow_document_type_create_view_with_access(self):
        self.workflow = self._create_workflow()
        self.grant_access(permission=permission_workflow_edit, obj=self.workflow)
        response = self._request_workflow_document_type_list_create_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertQuerysetEqual(
            self.workflow.document_types.all(), (repr(self.document_type),)
        )

    def _request_workflow_document_type_delete_view(self):
        return self.delete(
            viewname='rest_api:workflow-document-type-detail',
            args=(self.workflow.pk, self.document_type.pk)
        )

    def test_workflow_document_type_delete_view_no_access(self):
        self.workflow = self._create_workflow()
        self.workflow.document_types.add(self.document_type)
        response = self._request_workflow_document_type_delete_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.workflow.refresh_from_db()
        self.assertEqual(self.workflow.document_types.count(), 1)

    def test_workflow_document_type_delete_view_with_access(self):
        self.workflow = self._create_workflow()
        self.workflow.document_types.add(self.document_type)
        self.grant_access(permission=permission_workflow_edit, obj=self.workflow)
        response = self._request_workflow_document_type_delete_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.workflow.refresh_from_db()
        self.assertEqual(self.workflow.document_types.count(), 0)

    def _request_workflow_document_type_detail_view(self):
        return self.get(
            viewname='rest_api:workflow-document-type-detail',
            args=(self.workflow.pk, self.document_type.pk)
        )

    def test_workflow_document_type_detail_view_no_access(self):
        self.workflow = self._create_workflow()
        self.workflow.document_types.add(self.document_type)
        response = self._request_workflow_document_type_detail_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('label' in response.data)

    def test_workflow_document_type_detail_view_with_workflow_access(self):
        self.workflow = self._create_workflow()
        self.workflow.document_types.add(self.document_type)
        self.grant_access(permission=permission_workflow_view, obj=self.workflow)
        response = self._request_workflow_document_type_detail_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse('label' in response.data)

    def test_workflow_document_type_detail_view_with_document_access(self):
        self.workflow = self._create_workflow()
        self.workflow.document_types.add(self.document_type)
        self.grant_access(permission=permission_document_type_view, obj=self.document_type)
        response = self._request_workflow_document_type_detail_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('label' in response.data)

    def test_workflow_document_type_detail_view_with_access(self):
        self.workflow = self._create_workflow()
        self.workflow.document_types.add(self.document_type)
        self.grant_access(permission=permission_document_type_view, obj=self.document_type)
        self.grant_access(permission=permission_workflow_view, obj=self.workflow)
        response = self._request_workflow_document_type_detail_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['label'], self.document_type.label)

    def _request_workflow_document_type_list_view(self):
        return self.get(
            viewname='rest_api:workflow-document-type-list', args=(
                self.workflow.pk,
            )
        )

    def test_workflow_document_type_list_view_no_access(self):
        self.workflow = self._create_workflow()
        self.workflow.document_types.add(self.document_type)
        response = self._request_workflow_document_type_list_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_workflow_document_type_list_view_with_workflow_access(self):
        self.workflow = self._create_workflow()
        self.workflow.document_types.add(self.document_type)
        self.grant_access(permission=permission_workflow_view, obj=self.workflow)
        response = self._request_workflow_document_type_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_workflow_document_type_list_view_with_document_access(self):
        self.workflow = self._create_workflow()
        self.workflow.document_types.add(self.document_type)
        self.grant_access(permission=permission_document_type_view, obj=self.document_type)
        response = self._request_workflow_document_type_list_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_workflow_document_type_list_view_with_access(self):
        self.workflow = self._create_workflow()
        self.workflow.document_types.add(self.document_type)
        self.grant_access(permission=permission_document_type_view, obj=self.document_type)
        self.grant_access(permission=permission_workflow_view, obj=self.workflow)
        response = self._request_workflow_document_type_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['label'], self.document_type.label)

    def _request_workflow_list_view(self):
        return self.get(viewname='rest_api:workflow-list')

    def test_workflow_list_view_no_access(self):
        self.workflow = self._create_workflow()
        response = self._request_workflow_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_workflow_list_view_with_access(self):
        self.workflow = self._create_workflow()
        self.grant_access(permission=permission_workflow_view, obj=self.workflow)
        response = self._request_workflow_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['label'], self.workflow.label)

    def _request_workflow_edit_view_via_patch(self):
        return self.patch(
            viewname='rest_api:workflow-detail', args=(self.workflow.pk,),
            data={'label': TEST_WORKFLOW_LABEL_EDITED}
        )

    def test_workflow_patch_view_no_access(self):
        self.workflow = self._create_workflow()
        response = self._request_workflow_edit_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.workflow.refresh_from_db()
        self.assertEqual(self.workflow.label, TEST_WORKFLOW_LABEL)

    def test_workflow_patch_view_with_access(self):
        self.workflow = self._create_workflow()
        self.grant_access(permission=permission_workflow_edit, obj=self.workflow)
        response = self._request_workflow_edit_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.workflow.refresh_from_db()
        self.assertEqual(self.workflow.label, TEST_WORKFLOW_LABEL_EDITED)

    def _request_workflow_edit_view_via_put(self):
        return self.put(
            viewname='rest_api:workflow-detail', args=(self.workflow.pk,),
            data={'label': TEST_WORKFLOW_LABEL_EDITED}
        )

    def test_workflow_put_view_no_access(self):
        self.workflow = self._create_workflow()
        response = self._request_workflow_edit_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.workflow.refresh_from_db()
        self.assertEqual(self.workflow.label, TEST_WORKFLOW_LABEL)

    def test_workflow_put_view_with_access(self):
        self.workflow = self._create_workflow()
        self.grant_access(permission=permission_workflow_edit, obj=self.workflow)
        response = self._request_workflow_edit_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.workflow.refresh_from_db()
        self.assertEqual(self.workflow.label, TEST_WORKFLOW_LABEL_EDITED)

    def _request_document_type_workflow_list_view(self):
        return self.get(
            viewname='rest_api:documenttype-workflow-list',
            args=(self.document_type.pk,)
        )

    def test_document_type_workflow_list_no_access(self):
        self.workflow = self._create_workflow()
        self.workflow.document_types.add(self.document_type)
        response = self._request_document_type_workflow_list_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('results' in response.data)

    def test_document_type_workflow_list_with_workflow_access(self):
        self.workflow = self._create_workflow()
        self.workflow.document_types.add(self.document_type)
        self.grant_access(permission=permission_workflow_view, obj=self.workflow)
        response = self._request_document_type_workflow_list_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('results' in response.data)

    def test_document_type_workflow_list_with_document_access(self):
        self.workflow = self._create_workflow()
        self.workflow.document_types.add(self.document_type)
        self.grant_access(
            permission=permission_document_type_view, obj=self.document_type
        )
        response = self._request_document_type_workflow_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_document_type_workflow_list_with_access(self):
        self.workflow = self._create_workflow()
        self.workflow.document_types.add(self.document_type)
        self.grant_access(permission=permission_workflow_view, obj=self.workflow)
        self.grant_access(
            permission=permission_document_type_view, obj=self.document_type
        )
        response = self._request_document_type_workflow_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['label'], self.workflow.label)


@override_settings(OCR_AUTO_OCR=False)
class WorkflowStatesAPITestCase(BaseAPITestCase):
    def setUp(self):
        super(WorkflowStatesAPITestCase, self).setUp()
        self.login_user()

        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )

        with open(TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            self.document = self.document_type.new_document(
                file_object=file_object
            )

    def tearDown(self):
        if hasattr(self, 'document_type'):
            self.document_type.delete()
        super(WorkflowStatesAPITestCase, self).tearDown()

    def _create_workflow(self):
        self.workflow = Workflow.objects.create(
            label=TEST_WORKFLOW_LABEL,
            internal_name=TEST_WORKFLOW_INTERNAL_NAME
        )

    def _create_workflow_state(self):
        self._create_workflow()
        self.workflow_state = self.workflow.states.create(
            completion=TEST_WORKFLOW_STATE_COMPLETION,
            label=TEST_WORKFLOW_STATE_LABEL
        )

    def _request_workflow_state_create_view(self):
        return self.post(
            viewname='rest_api:workflowstate-list',
            args=(self.workflow.pk,), data={
                'completion': TEST_WORKFLOW_STATE_COMPLETION,
                'label': TEST_WORKFLOW_STATE_LABEL
            }
        )

    def test_workflow_state_create_view_no_access(self):
        self._create_workflow()
        response = self._request_workflow_state_create_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.workflow.refresh_from_db()
        self.assertEqual(self.workflow.states.count(), 0)

    def test_workflow_state_create_view_with_access(self):
        self._create_workflow()
        self.grant_access(permission=permission_workflow_edit, obj=self.workflow)
        response = self._request_workflow_state_create_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.workflow.refresh_from_db()
        self.assertEqual(
            self.workflow.states.first().label, TEST_WORKFLOW_STATE_LABEL
        )

    def _request_workflow_state_delete_view(self):
        return self.delete(
            viewname='rest_api:workflowstate-detail',
            args=(self.workflow.pk, self.workflow_state.pk)
        )

    def test_workflow_state_delete_view_no_access(self):
        self._create_workflow_state()
        response = self._request_workflow_state_delete_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.workflow.refresh_from_db()
        self.assertEqual(self.workflow.states.count(), 1)

    def test_workflow_state_delete_view_with_access(self):
        self._create_workflow_state()
        self.grant_access(permission=permission_workflow_edit, obj=self.workflow)
        response = self._request_workflow_state_delete_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.workflow.refresh_from_db()
        self.assertEqual(self.workflow.states.count(), 0)

    def _request_workflow_state_detail_view(self):
        return self.get(
            viewname='rest_api:workflowstate-detail',
            args=(self.workflow.pk, self.workflow_state.pk)
        )

    def test_workflow_state_detail_view_no_access(self):
        self._create_workflow_state()
        response = self._request_workflow_state_detail_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('label' in response.data)

    def test_workflow_state_detail_view_with_access(self):
        self._create_workflow_state()
        self.grant_access(permission=permission_workflow_view, obj=self.workflow)
        response = self._request_workflow_state_detail_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['label'], TEST_WORKFLOW_STATE_LABEL
        )

    def _request_workflow_state_list_view(self):
        return self.get(
            viewname='rest_api:workflowstate-list', args=(self.workflow.pk,),
        )

    def test_workflow_state_list_view_no_access(self):
        self._create_workflow_state()
        response = self._request_workflow_state_list_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('label' in response.data)

    def test_workflow_state_list_view_with_access(self):
        self._create_workflow_state()
        self.grant_access(permission=permission_workflow_view, obj=self.workflow)
        response = self._request_workflow_state_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['label'], TEST_WORKFLOW_STATE_LABEL
        )

    def _request_workflow_state_edit_view_via_patch(self):
        return self.patch(
            viewname='rest_api:workflowstate-detail',
            args=(self.workflow.pk, self.workflow_state.pk), data={
                'label': TEST_WORKFLOW_STATE_LABEL_EDITED
            }
        )

    def test_workflow_state_edit_view_via_patch_no_access(self):
        self._create_workflow_state()
        response = self._request_workflow_state_edit_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.workflow_state.refresh_from_db()
        self.assertEqual(
            self.workflow_state.label, TEST_WORKFLOW_STATE_LABEL
        )

    def test_workflow_state_edit_view_via_patch_with_access(self):
        self._create_workflow_state()
        self.grant_access(permission=permission_workflow_edit, obj=self.workflow)
        response = self._request_workflow_state_edit_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.workflow_state.refresh_from_db()
        self.assertEqual(
            self.workflow_state.label, TEST_WORKFLOW_STATE_LABEL_EDITED
        )

    def _request_workflow_state_edit_view_via_put(self):
        return self.put(
            viewname='rest_api:workflowstate-detail',
            args=(self.workflow.pk, self.workflow_state.pk), data={
                'label': TEST_WORKFLOW_STATE_LABEL_EDITED
            }
        )

    def test_workflow_state_edit_view_via_put_no_access(self):
        self._create_workflow_state()
        response = self._request_workflow_state_edit_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.workflow_state.refresh_from_db()
        self.assertEqual(
            self.workflow_state.label, TEST_WORKFLOW_STATE_LABEL
        )

    def test_workflow_state_edit_view_via_put_with_access(self):
        self._create_workflow_state()
        self.grant_access(permission=permission_workflow_edit, obj=self.workflow)
        response = self._request_workflow_state_edit_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.workflow_state.refresh_from_db()
        self.assertEqual(
            self.workflow_state.label, TEST_WORKFLOW_STATE_LABEL_EDITED
        )


@override_settings(OCR_AUTO_OCR=False)
class WorkflowTransitionsAPITestCase(BaseAPITestCase):
    def setUp(self):
        super(WorkflowTransitionsAPITestCase, self).setUp()
        self.login_user()

        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )

        with open(TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            self.document = self.document_type.new_document(
                file_object=file_object
            )

    def tearDown(self):
        if hasattr(self, 'document_type'):
            self.document_type.delete()
        super(WorkflowTransitionsAPITestCase, self).tearDown()

    def _create_workflow(self):
        self.workflow = Workflow.objects.create(
            label=TEST_WORKFLOW_LABEL,
            internal_name=TEST_WORKFLOW_INTERNAL_NAME
        )

    def _create_workflow_states(self):
        self._create_workflow()
        self.workflow_state_1 = self.workflow.states.create(
            completion=TEST_WORKFLOW_INITIAL_STATE_COMPLETION,
            label=TEST_WORKFLOW_INITIAL_STATE_LABEL
        )
        self.workflow_state_2 = self.workflow.states.create(
            completion=TEST_WORKFLOW_STATE_COMPLETION,
            label=TEST_WORKFLOW_STATE_LABEL
        )

    def _create_workflow_transition(self):
        self._create_workflow_states()
        self.workflow_transition = self.workflow.transitions.create(
            label=TEST_WORKFLOW_TRANSITION_LABEL,
            origin_state=self.workflow_state_1,
            destination_state=self.workflow_state_2,
        )

    def _request_workflow_transition_create_view(self):
        return self.post(
            viewname='rest_api:workflowtransition-list',
            args=(self.workflow.pk,), data={
                'label': TEST_WORKFLOW_TRANSITION_LABEL,
                'origin_state_pk': self.workflow_state_1.pk,
                'destination_state_pk': self.workflow_state_2.pk,
            }
        )

    def test_workflow_transition_create_view_no_access(self):
        self._create_workflow_states()
        response = self._request_workflow_transition_create_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.workflow.refresh_from_db()
        self.assertEqual(self.workflow.transitions.count(), 0)

    def test_workflow_transition_create_view_with_access(self):
        self._create_workflow_states()
        self.grant_access(permission=permission_workflow_edit, obj=self.workflow)
        response = self._request_workflow_transition_create_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.workflow.refresh_from_db()
        self.assertEqual(
            self.workflow.transitions.first().label,
            TEST_WORKFLOW_TRANSITION_LABEL
        )

    def _request_workflow_transition_delete_view(self):
        return self.delete(
            viewname='rest_api:workflowtransition-detail',
            args=(self.workflow.pk, self.workflow_transition.pk)
        )

    def test_workflow_transition_delete_view_no_access(self):
        self._create_workflow_transition()
        response = self._request_workflow_transition_delete_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.workflow.refresh_from_db()
        self.assertEqual(self.workflow.transitions.count(), 1)

    def test_workflow_transition_delete_view_with_access(self):
        self._create_workflow_transition()
        self.grant_access(permission=permission_workflow_edit, obj=self.workflow)
        response = self._request_workflow_transition_delete_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.workflow.refresh_from_db()
        self.assertEqual(self.workflow.transitions.count(), 0)

    def _request_workflow_transition_detail_view(self):
        return self.get(
            viewname='rest_api:workflowtransition-detail',
            args=(self.workflow.pk, self.workflow_transition.pk)
        )

    def test_workflow_transition_detail_view_no_access(self):
        self._create_workflow_transition()
        response = self._request_workflow_transition_detail_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('label' in response.data)

    def test_workflow_transition_detail_view_with_access(self):
        self._create_workflow_transition()
        self.grant_access(
            permission=permission_workflow_view, obj=self.workflow
        )
        response = self._request_workflow_transition_detail_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['label'], TEST_WORKFLOW_TRANSITION_LABEL
        )

    def _request_workflow_transition_list_view(self):
        return self.get(
            viewname='rest_api:workflowtransition-list',
            args=(self.workflow.pk,)
        )

    def test_workflow_transition_list_view_no_access(self):
        self._create_workflow_transition()
        response = self._request_workflow_transition_list_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('results' in response.data)

    def test_workflow_transition_list_view_with_access(self):
        self._create_workflow_transition()
        self.grant_access(
            permission=permission_workflow_view, obj=self.workflow
        )
        response = self._request_workflow_transition_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['label'],
            TEST_WORKFLOW_TRANSITION_LABEL
        )

    def _request_workflow_transition_edit_view_via_patch(self):
        return self.patch(
            viewname='rest_api:workflowtransition-detail',
            args=(self.workflow.pk, self.workflow_transition.pk), data={
                'label': TEST_WORKFLOW_TRANSITION_LABEL_EDITED,
                'origin_state_pk': self.workflow_state_2.pk,
                'destination_state_pk': self.workflow_state_1.pk,
            }
        )

    def test_workflow_transition_edit_view_via_patch_no_access(self):
        self._create_workflow_transition()
        response = self._request_workflow_transition_edit_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.workflow_transition.refresh_from_db()
        self.assertEqual(
            self.workflow_transition.label,
            TEST_WORKFLOW_TRANSITION_LABEL
        )
        self.assertEqual(
            self.workflow_transition.origin_state,
            self.workflow_state_1
        )
        self.assertEqual(
            self.workflow_transition.destination_state,
            self.workflow_state_2
        )

    def test_workflow_transition_edit_view_via_patch_with_access(self):
        self._create_workflow_transition()
        self.grant_access(permission=permission_workflow_edit, obj=self.workflow)
        response = self._request_workflow_transition_edit_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.workflow_transition.refresh_from_db()
        self.assertEqual(
            self.workflow_transition.label,
            TEST_WORKFLOW_TRANSITION_LABEL_EDITED
        )
        self.assertEqual(
            self.workflow_transition.origin_state,
            self.workflow_state_2
        )
        self.assertEqual(
            self.workflow_transition.destination_state,
            self.workflow_state_1
        )

    def _request_workflow_transition_edit_view_via_put(self):
        return self.put(
            viewname='rest_api:workflowtransition-detail',
            args=(self.workflow.pk, self.workflow_transition.pk), data={
                'label': TEST_WORKFLOW_TRANSITION_LABEL_EDITED,
                'origin_state_pk': self.workflow_state_2.pk,
                'destination_state_pk': self.workflow_state_1.pk,
            }
        )

    def test_workflow_transition_edit_view_via_put_no_access(self):
        self._create_workflow_transition()
        response = self._request_workflow_transition_edit_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.workflow_transition.refresh_from_db()
        self.assertEqual(
            self.workflow_transition.label,
            TEST_WORKFLOW_TRANSITION_LABEL
        )
        self.assertEqual(
            self.workflow_transition.origin_state,
            self.workflow_state_1
        )
        self.assertEqual(
            self.workflow_transition.destination_state,
            self.workflow_state_2
        )

    def test_workflow_transition_edit_view_via_put_with_access(self):
        self._create_workflow_transition()
        self.grant_access(permission=permission_workflow_edit, obj=self.workflow)
        response = self._request_workflow_transition_edit_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.workflow_transition.refresh_from_db()
        self.assertEqual(
            self.workflow_transition.label,
            TEST_WORKFLOW_TRANSITION_LABEL_EDITED
        )
        self.assertEqual(
            self.workflow_transition.origin_state,
            self.workflow_state_2
        )
        self.assertEqual(
            self.workflow_transition.destination_state,
            self.workflow_state_1
        )


@override_settings(OCR_AUTO_OCR=False)
class DocumentWorkflowsAPITestCase(BaseAPITestCase):
    def setUp(self):
        super(DocumentWorkflowsAPITestCase, self).setUp()
        self.login_user()

        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )

    def tearDown(self):
        if hasattr(self, 'document_type'):
            self.document_type.delete()
        super(DocumentWorkflowsAPITestCase, self).tearDown()

    def _create_document(self):
        with open(TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            self.document = self.document_type.new_document(
                file_object=file_object
            )

    def _create_workflow(self):
        self.workflow = Workflow.objects.create(
            label=TEST_WORKFLOW_LABEL,
            internal_name=TEST_WORKFLOW_INTERNAL_NAME
        )
        self.workflow.document_types.add(self.document_type)

    def _create_workflow_states(self):
        self._create_workflow()
        self.workflow_state_1 = self.workflow.states.create(
            completion=TEST_WORKFLOW_INITIAL_STATE_COMPLETION,
            initial=True, label=TEST_WORKFLOW_INITIAL_STATE_LABEL
        )
        self.workflow_state_2 = self.workflow.states.create(
            completion=TEST_WORKFLOW_STATE_COMPLETION,
            label=TEST_WORKFLOW_STATE_LABEL
        )

    def _create_workflow_transition(self):
        self._create_workflow_states()
        self.workflow_transition = self.workflow.transitions.create(
            label=TEST_WORKFLOW_TRANSITION_LABEL,
            origin_state=self.workflow_state_1,
            destination_state=self.workflow_state_2,
        )

    def _create_workflow_instance_log_entry(self):
        self.document.workflows.first().log_entries.create(
            comment=TEST_WORKFLOW_INSTANCE_LOG_ENTRY_COMMENT, transition=self.workflow_transition,
            user=self.user
        )

    def _request_workflow_instance_detail_view(self):
        return self.get(
            viewname='rest_api:workflowinstance-detail', args=(
                self.document.pk, self.document.workflows.first().pk
            ),
        )

    def test_workflow_instance_detail_view_no_access(self):
        self._create_workflow_transition()
        self._create_document()
        response = self._request_workflow_instance_detail_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('workflow' in response.data)

    def test_workflow_instance_detail_view_with_workflow_access(self):
        self._create_workflow_transition()
        self._create_document()
        self.grant_access(permission=permission_workflow_view, obj=self.workflow)
        response = self._request_workflow_instance_detail_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('workflow' in response.data)

    def test_workflow_instance_detail_view_with_document_access(self):
        self._create_workflow_transition()
        self._create_document()
        self.grant_access(permission=permission_workflow_view, obj=self.document)
        response = self._request_workflow_instance_detail_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse('workflow' in response.data)

    def test_workflow_instance_detail_view_with_access(self):
        self._create_workflow_transition()
        self._create_document()
        self.grant_access(permission=permission_workflow_view, obj=self.workflow)
        self.grant_access(permission=permission_workflow_view, obj=self.document)
        response = self._request_workflow_instance_detail_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['workflow']['label'],
            TEST_WORKFLOW_LABEL
        )

    def _request_workflow_instance_list_view(self):
        return self.get(
            viewname='rest_api:workflowinstance-list',
            args=(self.document.pk,)
        )

    def test_workflow_instance_list_view_no_access(self):
        self._create_workflow_transition()
        self._create_document()
        response = self._request_workflow_instance_list_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('result' in response.data)

    def test_workflow_instance_list_view_with_document_access(self):
        self._create_workflow_transition()
        self._create_document()
        self.grant_access(permission=permission_workflow_view, obj=self.document)
        response = self._request_workflow_instance_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_workflow_instance_list_view_with_workflow_access(self):
        self._create_workflow_transition()
        self._create_document()
        self.grant_access(permission=permission_workflow_view, obj=self.workflow)
        response = self._request_workflow_instance_list_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('result' in response.data)

    def test_workflow_instance_list_view_with_access(self):
        self._create_workflow_transition()
        self._create_document()
        self.grant_access(permission=permission_workflow_view, obj=self.workflow)
        self.grant_access(permission=permission_workflow_view, obj=self.document)
        response = self._request_workflow_instance_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['workflow']['label'],
            TEST_WORKFLOW_LABEL
        )

    def _request_workflow_instance_log_entry_create_view(self, workflow_instance):
        return self.post(
            viewname='rest_api:workflowinstancelogentry-list', args=(
                self.document.pk, workflow_instance.pk
            ), data={'transition_pk': self.workflow_transition.pk}
        )

    def test_workflow_instance_log_entries_create_view_no_access(self):
        self._create_workflow_transition()
        self._create_document()
        workflow_instance = self.document.workflows.first()
        response = self._request_workflow_instance_log_entry_create_view(
            workflow_instance=workflow_instance
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # We get bad request because we try to create a transition for which
        # we don't have permission and therefore is not valid for this
        # workflow instance current state
        self.assertEqual(workflow_instance.log_entries.count(), 0)

    def test_workflow_instance_log_entries_create_view_with_workflow_access(self):
        self._create_workflow_transition()
        self._create_document()
        self.grant_access(permission=permission_workflow_transition, obj=self.workflow)
        workflow_instance = self.document.workflows.first()
        response = self._request_workflow_instance_log_entry_create_view(
            workflow_instance=workflow_instance
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        workflow_instance.refresh_from_db()
        self.assertEqual(
            workflow_instance.log_entries.first().transition.label,
            TEST_WORKFLOW_TRANSITION_LABEL
        )

    def _request_workflow_instance_log_entry_list_view(self):
        return self.get(
            viewname='rest_api:workflowinstancelogentry-list', args=(
                self.document.pk, self.document.workflows.first().pk
            ),
        )

    def test_workflow_instance_log_entries_list_view_no_access(self):
        self._create_workflow_transition()
        self._create_document()
        self._create_workflow_instance_log_entry()
        response = self._request_workflow_instance_log_entry_list_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('results' in response.data)

    def test_workflow_instance_log_entries_list_view_with_document_access(self):
        self._create_workflow_transition()
        self._create_document()
        self._create_workflow_instance_log_entry()
        self.grant_access(permission=permission_workflow_view, obj=self.document)
        response = self._request_workflow_instance_log_entry_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['transition']['label'],
            TEST_WORKFLOW_TRANSITION_LABEL
        )
