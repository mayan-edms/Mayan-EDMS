from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

link_setup_workflow_list = {'text': _('Workflows'), 'view': 'document_states:setup_workflow_list', 'famfam': 'table', 'icon': 'main/icons/table.png'}
link_setup_workflow_create = {'text': _('Create'), 'view': 'document_states:setup_workflow_create', 'famfam': 'table_add'}
link_setup_workflow_delete = {'text': _('Delete'), 'view': 'document_states:setup_workflow_delete', 'args': 'object.pk', 'famfam': 'table_delete'}
link_setup_workflow_edit = {'text': _('Edit'), 'view': 'document_states:setup_workflow_edit', 'args': 'object.pk', 'famfam': 'table_edit'}

link_setup_workflow_states = {'text': _('States'), 'view': 'document_states:setup_workflow_states', 'args': 'object.pk', 'famfam': 'style'}
link_setup_workflow_state_create = {'text': _('Create state'), 'view': 'document_states:setup_workflow_state_create', 'args': 'object.pk', 'famfam': 'style_add'}
link_setup_workflow_state_delete = {'text': _('Delete'), 'view': 'document_states:setup_workflow_state_delete', 'args': 'object.pk', 'famfam': 'delete'}
link_setup_workflow_state_edit = {'text': _('Edit'), 'view': 'document_states:setup_workflow_state_edit', 'args': 'object.pk', 'famfam': 'pencil'}

link_setup_workflow_transitions = {'text': _('Transitions'), 'view': 'document_states:setup_workflow_transitions', 'args': 'object.pk', 'famfam': 'lightning'}
link_setup_workflow_transition_create = {'text': _('Create transition'), 'view': 'document_states:setup_workflow_transition_create', 'args': 'object.pk', 'famfam': 'lightning_add'}
link_setup_workflow_transition_delete = {'text': _('Delete'), 'view': 'document_states:setup_workflow_transition_delete', 'args': 'object.pk', 'famfam': 'delete'}
link_setup_workflow_transition_edit = {'text': _('Edit'), 'view': 'document_states:setup_workflow_transition_edit', 'args': 'object.pk', 'famfam': 'pencil'}

link_setup_workflow_document_types = {'text': _('Document types'), 'view': 'document_states:setup_workflow_document_types', 'args': 'object.pk', 'famfam': 'layout'}

link_document_workflow_instance_list = {'text': _('Workflows'), 'view': 'document_states:document_workflow_instance_list', 'args': 'object.pk', 'famfam': 'table'}
link_workflow_instance_detail = {'text': _('Detail'), 'view': 'document_states:workflow_instance_detail', 'args': 'workflow_instance.pk', 'famfam': 'table'}
link_workflow_instance_transition = {'text': _('Transition'), 'view': 'document_states:workflow_instance_transition', 'args': 'workflow_instance.pk', 'famfam': 'table_lightning'}
