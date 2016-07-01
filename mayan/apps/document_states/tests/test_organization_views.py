from __future__ import unicode_literals

from django.test import override_settings

from organizations.tests.test_organization_views import OrganizationViewTestCase

from ..models import Workflow

from .literals import TEST_WORKFLOW_LABEL, TEST_WORKFLOW_LABEL_EDITED


@override_settings(OCR_AUTO_OCR=False)
class OrganizationWorkflowiewTestCase(OrganizationViewTestCase):
    def create_workflow(self):
        with self.settings(ORGANIZATION_ID=self.organization_a.pk):
            self.workflow = Workflow.on_organization.create(label=TEST_WORKFLOW_LABEL)

    def test_workflow_create_view(self):
        with self.settings(ORGANIZATION_ID=self.organization_a.pk):
            response = self.post(
                'document_states:setup_workflow_create',
                data={'label': TEST_WORKFLOW_LABEL_EDITED}, follow=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(Workflow.on_organization.count(), 1)

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            self.assertEqual(Workflow.on_organization.count(), 0)

    def test_workflow_delete_view(self):
        self.create_workflow()

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            response = self.post(
                'document_states:setup_workflow_delete',
                args=(self.workflow.pk,), follow=True
            )
            self.assertEqual(response.status_code, 404)

    def test_workflow_edit_view(self):
        self.create_workflow()

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            response = self.post(
                'document_states:setup_workflow_edit',
                args=(self.workflow.pk,),
                data={'label': TEST_WORKFLOW_LABEL_EDITED}, follow=True
            )
            self.assertEqual(response.status_code, 404)

        with self.settings(ORGANIZATION_ID=self.organization_a.pk):
            self.assertEqual(
                Workflow.on_organization.first().label, TEST_WORKFLOW_LABEL
            )
