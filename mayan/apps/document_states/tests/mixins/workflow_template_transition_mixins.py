from django.db.models import Q

from mayan.apps.events.classes import EventType

from ...models import (
    WorkflowTransition, WorkflowTransitionField,
    WorkflowTransitionTriggerEvent
)

from ..literals import (
    TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_HELP_TEXT,
    TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_LABEL,
    TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_LABEL_EDITED,
    TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_NAME,
    TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_TYPE,
    TEST_WORKFLOW_TEMPLATE_TRANSITION_LABEL,
    TEST_WORKFLOW_TEMPLATE_TRANSITION_LABEL_EDITED
)


class WorkflowTransitionFieldViewTestMixin:
    def _request_workflow_template_transition_field_create_view(self):
        pk_list = list(
            WorkflowTransitionField.objects.values_list('pk', flat=True)
        )

        response = self.post(
            viewname='document_states:workflow_template_transition_field_create',
            kwargs={
                'workflow_template_transition_id': self._test_workflow_template_transition.pk
            }, data={
                'field_type': TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_TYPE,
                'name': TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_NAME,
                'label': TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_LABEL,
                'help_text': TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_HELP_TEXT
            }
        )

        try:
            self._test_workflow_template_transition_field = WorkflowTransitionField.objects.get(
                ~Q(pk__in=pk_list)
            )
        except WorkflowTransitionField.DoesNotExist:
            self._test_workflow_template_transition_field = None

        return response

    def _request_workflow_template_transition_field_delete_view(self):
        return self.post(
            viewname='document_states:workflow_template_transition_field_delete',
            kwargs={
                'workflow_template_transition_field_id': self._test_workflow_template_transition_field.pk
            }
        )

    def _request_workflow_template_transition_field_edit_view(self):
        return self.post(
            viewname='document_states:workflow_template_transition_field_edit',
            kwargs={
                'workflow_template_transition_field_id': self._test_workflow_template_transition_field.pk
            }, data={
                'field_type': TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_TYPE,
                'name': TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_NAME,
                'label': TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_LABEL_EDITED,
                'help_text': TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_HELP_TEXT
            }
        )

    def _request_test_workflow_template_transition_field_list_view(self):
        return self.get(
            viewname='document_states:workflow_template_transition_field_list',
            kwargs={
                'workflow_template_transition_id': self._test_workflow_template_transition.pk
            }
        )


class WorkflowTemplateTransitionAPIViewTestMixin:
    def _request_test_workflow_template_transition_create_api_view(
        self, extra_data=None
    ):
        data = {
            'label': TEST_WORKFLOW_TEMPLATE_TRANSITION_LABEL,
            'origin_state_id': self._test_workflow_template_states[0].pk,
            'destination_state_id': self._test_workflow_template_states[1].pk
        }

        if extra_data:
            data.update(extra_data)

        pk_list = list(
            WorkflowTransition.objects.values_list('pk', flat=True)
        )

        response = self.post(
            viewname='rest_api:workflow-template-transition-list', kwargs={
                'workflow_template_id': self._test_workflow_template.pk
            }, data=data
        )

        try:
            self._test_workflow_template_transition = WorkflowTransition.objects.get(
                ~Q(pk__in=pk_list)
            )
        except WorkflowTransition.DoesNotExist:
            self._test_workflow_template_transition = None

        return response

    def _request_test_workflow_template_transition_delete_api_view(self):
        return self.delete(
            viewname='rest_api:workflow-template-transition-detail',
            kwargs={
                'workflow_template_id': self._test_workflow_template.pk,
                'workflow_template_transition_id': self._test_workflow_template_transition.pk
            }
        )

    def _request_test_workflow_template_transition_detail_api_view(self):
        return self.get(
            viewname='rest_api:workflow-template-transition-detail',
            kwargs={
                'workflow_template_id': self._test_workflow_template.pk,
                'workflow_template_transition_id': self._test_workflow_template_transition.pk
            }
        )

    def _request_test_workflow_template_transition_list_api_view(self):
        return self.get(
            viewname='rest_api:workflow-template-transition-list',
            kwargs={
                'workflow_template_id': self._test_workflow_template.pk
            }
        )

    def _request_test_workflow_template_transition_edit_patch_api_view(self):
        return self.patch(
            viewname='rest_api:workflow-template-transition-detail',
            kwargs={
                'workflow_template_id': self._test_workflow_template.pk,
                'workflow_template_transition_id': self._test_workflow_template_transition.pk
            }, data={
                'label': TEST_WORKFLOW_TEMPLATE_TRANSITION_LABEL_EDITED,
                'origin_state_id': self._test_workflow_template_states[1].pk,
                'destination_state_id': self._test_workflow_template_states[0].pk
            }
        )

    def _request_test_workflow_template_transition_edit_put_api_view_via(self):
        return self.put(
            viewname='rest_api:workflow-template-transition-detail',
            kwargs={
                'workflow_template_id': self._test_workflow_template.pk,
                'workflow_template_transition_id': self._test_workflow_template_transition.pk
            }, data={
                'label': TEST_WORKFLOW_TEMPLATE_TRANSITION_LABEL_EDITED,
                'origin_state_id': self._test_workflow_template_states[1].pk,
                'destination_state_id': self._test_workflow_template_states[0].pk
            }
        )


class WorkflowTransitionFieldAPIViewTestMixin:
    def _request_test_workflow_template_transition_field_create_api_view(self):
        pk_list = list(WorkflowTransitionField.objects.values_list('pk'))

        response = self.post(
            viewname='rest_api:workflow-template-transition-field-list',
            kwargs={
                'workflow_template_id': self._test_workflow_template.pk,
                'workflow_template_transition_id': self._test_workflow_template_transition.pk,
            }, data={
                'field_type': TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_TYPE,
                'name': TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_NAME,
                'label': TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_LABEL,
                'help_text': TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_HELP_TEXT
            }
        )

        try:
            self._test_workflow_template_transition_field = WorkflowTransitionField.objects.get(
                ~Q(pk__in=pk_list)
            )
        except WorkflowTransitionField.DoesNotExist:
            self._test_workflow_template_transition_field = None

        return response

    def _request_test_workflow_template_transition_field_delete_api_view(self):
        return self.delete(
            viewname='rest_api:workflow-template-transition-field-detail',
            kwargs={
                'workflow_template_id': self._test_workflow_template.pk,
                'workflow_template_transition_id': self._test_workflow_template_transition.pk,
                'workflow_template_transition_field_id': self._test_workflow_template_transition_field.pk
            }
        )

    def _request_test_workflow_template_transition_field_detail_api_view(self):
        return self.get(
            viewname='rest_api:workflow-template-transition-field-detail',
            kwargs={
                'workflow_template_id': self._test_workflow_template.pk,
                'workflow_template_transition_id': self._test_workflow_template_transition.pk,
                'workflow_template_transition_field_id': self._test_workflow_template_transition_field.pk
            }
        )

    def _request_test_workflow_template_transition_field_edit_via_patch_api_view(self):
        return self.patch(
            viewname='rest_api:workflow-template-transition-field-detail',
            kwargs={
                'workflow_template_id': self._test_workflow_template.pk,
                'workflow_template_transition_id': self._test_workflow_template_transition.pk,
                'workflow_template_transition_field_id': self._test_workflow_template_transition_field.pk
            }, data={
                'label': '{} edited'.format(
                    self._test_workflow_template_transition_field
                )
            }
        )

    def _request_test_workflow_template_transition_field_list_api_view(self):
        return self.get(
            viewname='rest_api:workflow-template-transition-field-list',
            kwargs={
                'workflow_template_id': self._test_workflow_template.pk,
                'workflow_template_transition_id': self._test_workflow_template_transition.pk
            }
        )


class WorkflowTransitionFieldTestMixin:
    def _create_test_workflow_template_transition_field(self, extra_data=None):
        kwargs = {
            'field_type': TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_TYPE,
            'name': TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_NAME,
            'label': TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_LABEL,
            'help_text': TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_HELP_TEXT
        }
        kwargs.update(extra_data or {})

        self._test_workflow_template_transition_field = self._test_workflow_template_transition.fields.create(
            **kwargs
        )


class WorkflowTemplateTransitionTriggerAPIViewTestMixin:
    def _request_test_workflow_template_transition_trigger_create_api_view(self):
        data = {
            'event_type_id': self._test_event_type.id
        }

        pk_list = list(
            WorkflowTransitionTriggerEvent.objects.values_list(
                'pk', flat=True
            )
        )

        response = self.post(
            viewname='rest_api:workflow-template-transition-trigger-list',
            kwargs={
                'workflow_template_id': self._test_workflow_template.pk,
                'workflow_template_transition_id': self._test_workflow_template_transition.pk
            }, data=data
        )

        try:
            self._test_workflow_template_transition_trigger = WorkflowTransitionTriggerEvent.objects.get(
                ~Q(pk__in=pk_list)
            )
        except WorkflowTransitionTriggerEvent.DoesNotExist:
            self._test_workflow_template_transition_trigger = None

        return response

    def _request_test_workflow_template_transition_trigger_delete_api_view(self):
        return self.delete(
            viewname='rest_api:workflow-template-transition-trigger-detail',
            kwargs={
                'workflow_template_id': self._test_workflow_template.pk,
                'workflow_template_transition_id': self._test_workflow_template_transition.pk,
                'workflow_template_transition_trigger_id': self._test_workflow_template_transition_trigger.pk
            }
        )

    def _request_test_workflow_template_transition_trigger_detail_api_view(self):
        return self.get(
            viewname='rest_api:workflow-template-transition-trigger-detail',
            kwargs={
                'workflow_template_id': self._test_workflow_template.pk,
                'workflow_template_transition_id': self._test_workflow_template_transition.pk,
                'workflow_template_transition_trigger_id': self._test_workflow_template_transition_trigger.pk
            }
        )

    def _request_test_workflow_template_transition_trigger_list_api_view(self):
        return self.get(
            viewname='rest_api:workflow-template-transition-trigger-list',
            kwargs={
                'workflow_template_id': self._test_workflow_template.pk,
                'workflow_template_transition_id': self._test_workflow_template_transition.pk
            }
        )

    def _request_test_workflow_template_transition_trigger_edit_patch_api_view(self):
        return self.patch(
            viewname='rest_api:workflow-template-transition-trigger-detail',
            kwargs={
                'workflow_template_id': self._test_workflow_template.pk,
                'workflow_template_transition_id': self._test_workflow_template_transition.pk,
                'workflow_template_transition_trigger_id': self._test_workflow_template_transition_trigger.pk
            }, data={
                'event_type_id': self._test_event_type.id
            }
        )

    def _request_test_workflow_template_transition_trigger_edit_put_api_view(self):
        return self.put(
            viewname='rest_api:workflow-template-transition-trigger-detail',
            kwargs={
                'workflow_template_id': self._test_workflow_template.pk,
                'workflow_template_transition_id': self._test_workflow_template_transition.pk,
                'workflow_template_transition_trigger_id': self._test_workflow_template_transition_trigger.pk
            }, data={
                'event_type_id': self._test_event_type.id
            }
        )


class WorkflowTemplateTransitionTriggerTestMixin:
    def setUp(self):
        super().setUp()
        self._test_workflow_template_transition_triggers = []

    def _create_test_workflow_template_transition_trigger(self):
        event_type = EventType.get(id=self._test_event_type.id)

        self._test_workflow_template_transition_trigger = self._test_workflow_template_transition.trigger_events.create(
            event_type=event_type.get_stored_event_type()
        )
        self._test_workflow_template_transition_triggers.append(
            self._test_workflow_template_transition_trigger
        )


class WorkflowTemplateTransitionTriggerViewTestMixin:
    def _request_test_workflow_template_transition_event_list_view(self):
        return self.get(
            viewname='document_states:workflow_template_transition_triggers',
            kwargs={
                'workflow_template_transition_id': self._test_workflow_template_transition.pk
            }
        )


class WorkflowTemplateTransitionViewTestMixin:
    def _request_test_workflow_template_transition_create_view(self):
        pk_list = list(
            WorkflowTransition.objects.values_list('pk', flat=True)
        )

        response = self.post(
            viewname='document_states:workflow_template_transition_create',
            kwargs={
                'workflow_template_id': self._test_workflow_template.pk
            }, data={
                'label': TEST_WORKFLOW_TEMPLATE_TRANSITION_LABEL,
                'origin_state': self._test_workflow_template_states[0].pk,
                'destination_state': self._test_workflow_template_states[1].pk
            }
        )

        try:
            self._test_workflow_template_transition = WorkflowTransition.objects.get(
                ~Q(pk__in=pk_list)
            )
        except WorkflowTransition.DoesNotExist:
            self._test_workflow_template_transition = None

        return response

    def _request_test_workflow_template_transition_delete_view(self):
        return self.post(
            viewname='document_states:workflow_template_transition_delete',
            kwargs={
                'workflow_template_transition_id': self._test_workflow_template_transition.pk
            }
        )

    def _request_test_workflow_template_transition_edit_view(self):
        return self.post(
            viewname='document_states:workflow_template_transition_edit',
            kwargs={
                'workflow_template_transition_id': self._test_workflow_template_transition.pk
            }, data={
                'label': TEST_WORKFLOW_TEMPLATE_TRANSITION_LABEL_EDITED,
                'origin_state': self._test_workflow_template_states[0].pk,
                'destination_state': self._test_workflow_template_states[1].pk
            }
        )

    def _request_test_workflow_template_transition_list_view(self):
        return self.get(
            viewname='document_states:workflow_template_transition_list',
            kwargs={
                'workflow_template_id': self._test_workflow_template.pk
            }
        )
