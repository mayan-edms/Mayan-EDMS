from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from mayan.apps.document_indexing.tasks import task_index_instance_document_add
from mayan.apps.events.classes import EventType
from mayan.apps.events.literals import TEXT_UNKNOWN_EVENT_ID

from .literals import STORAGE_NAME_WORKFLOW_CACHE
from .settings import setting_workflow_image_cache_maximum_size
from .tasks import task_launch_all_workflow_for


def handler_create_workflow_image_cache(sender, **kwargs):
    Cache = apps.get_model(app_label='file_caching', model_name='Cache')
    Cache.objects.update_or_create(
        defaults={
            'maximum_size': setting_workflow_image_cache_maximum_size.value,
        }, defined_storage_name=STORAGE_NAME_WORKFLOW_CACHE,
    )


def handler_launch_workflow_on_create(sender, instance, created, **kwargs):
    if created:
        task_launch_all_workflow_for.apply_async(
            kwargs={'document_id': instance.pk}
        )


def handler_launch_workflow_on_type_change(sender, instance, **kwargs):
    task_launch_all_workflow_for.apply_async(
        kwargs={'document_id': instance.pk}
    )


def handler_trigger_transition(sender, **kwargs):
    action = kwargs['instance']

    Document = apps.get_model(
        app_label='documents', model_name='Document'
    )
    WorkflowInstance = apps.get_model(
        app_label='document_states', model_name='WorkflowInstance'
    )
    WorkflowTransition = apps.get_model(
        app_label='document_states', model_name='WorkflowTransition'
    )

    trigger_transitions = WorkflowTransition.objects.filter(
        trigger_events__event_type__name=kwargs['instance'].verb
    )

    if isinstance(action.target, Document):
        workflow_instances = WorkflowInstance.objects.filter(
            workflow__transitions__in=trigger_transitions,
            document=action.target
        ).distinct()
    elif isinstance(action.action_object, Document):
        workflow_instances = WorkflowInstance.objects.filter(
            workflow__transitions__in=trigger_transitions,
            document=action.action_object
        ).distinct()
    else:
        workflow_instances = WorkflowInstance.objects.none()

    for workflow_instance in workflow_instances:
        # Select the first transition that is valid for this workflow state.
        valid_transitions = list(
            set(
                trigger_transitions
            ) & set(
                workflow_instance.get_transition_choices()
            )
        )
        if valid_transitions:
            try:
                event_type_label = EventType.get(id=action.verb).label
            except KeyError:
                event_type_label = TEXT_UNKNOWN_EVENT_ID % action.verb

            workflow_instance.do_transition(
                comment=_('Event trigger: %s') % event_type_label,
                transition=valid_transitions[0]
            )


# Indexing, workflow template


def handler_workflow_template_post_edit(sender, **kwargs):
    if not kwargs.get('created', False):
        for workflow_instance in kwargs['instance'].instances.all():
            task_index_instance_document_add.apply_async(
                kwargs={'document_id': workflow_instance.document.pk}
            )


# Indexing, workflow state


def handler_workflow_template_state_post_edit(sender, **kwargs):
    if not kwargs.get('created', False):
        for workflow_instance in kwargs['instance'].workflow.instances.all():
            task_index_instance_document_add.apply_async(
                kwargs={'document_id': workflow_instance.document.pk}
            )


def handler_workflow_template_state_pre_delete(sender, **kwargs):
    for workflow_instance in kwargs['instance'].workflow.instances.all():
        # Remove each of the documents.
        # Trigger the remove event for each document so they can be
        # reindexed.
        workflow_instance.delete()
        task_index_instance_document_add.apply_async(
            kwargs={'document_id': workflow_instance.document.pk}
        )


# Indexing, workflow template


def handler_workflow_template_transition_post_edit(sender, **kwargs):
    if not kwargs.get('created', False):
        for workflow_instance in kwargs['instance'].workflow.instances.all():
            task_index_instance_document_add.apply_async(
                kwargs={'document_id': workflow_instance.document.pk}
            )


def handler_workflow_template_transition_pre_delete(sender, **kwargs):
    for workflow_instance in kwargs['instance'].workflow.instances.all():
        # Remove each of the documents.
        # Trigger the remove event for each document so they can be
        # reindexed.
        workflow_instance.delete()
        task_index_instance_document_add.apply_async(
            kwargs={'document_id': workflow_instance.document.pk}
        )
