# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Removing unique constraint on 'WorkflowInstance', fields ['object_id', 'content_type', 'workflow']
        db.delete_unique('workflows_workflowinstance', ['object_id', 'content_type_id', 'workflow_id'])

        # Deleting model 'WorkflowStateAbilityGrant'
        db.delete_table('workflows_workflowstateabilitygrant')

        # Deleting model 'WorkflowStateTransition'
        db.delete_table('workflows_workflowstatetransition')

        # Deleting model 'WorkflowStateTransitionAbility'
        db.delete_table('workflows_workflowstatetransitionability')

        # Deleting model 'Transition'
        db.delete_table('workflows_transition')

        # Adding model 'WorkflowInstanceActiveState'
        db.create_table('workflows_workflowinstanceactivestate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('workflow_instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workflows.WorkflowInstance'])),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workflows.State'], null=True)),
        ))
        db.send_create_signal('workflows', ['WorkflowInstanceActiveState'])

        # Adding unique constraint on 'WorkflowInstanceActiveState', fields ['workflow_instance', 'state']
        db.create_unique('workflows_workflowinstanceactivestate', ['workflow_instance_id', 'state_id'])

        # Adding model 'End'
        db.create_table('workflows_end', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('workflows', ['End'])

        # Adding model 'WorkflowInstanceActiveNode'
        db.create_table('workflows_workflowinstanceactivenode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('workflow_instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workflows.WorkflowInstance'])),
            ('workflow_node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workflows.WorkflowNode'])),
        ))
        db.send_create_signal('workflows', ['WorkflowInstanceActiveNode'])

        # Adding model 'Start'
        db.create_table('workflows_start', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
        ))
        db.send_create_signal('workflows', ['Start'])

        # Adding model 'WorkflowNode'
        db.create_table('workflows_workflownode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('workflow', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workflows.Workflow'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('workflows', ['WorkflowNode'])

        # Adding field 'Workflow.initial_node'
        db.add_column('workflows_workflow', 'initial_node', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='workflow_initial_node', null=True, to=orm['workflows.WorkflowNode']), keep_default=False)

        # Deleting field 'WorkflowInstance.workflow_state'
        db.delete_column('workflows_workflowinstance', 'workflow_state_id')

        # Adding unique constraint on 'WorkflowState', fields ['state', 'workflow']
        db.create_unique('workflows_workflowstate', ['state_id', 'workflow_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'WorkflowState', fields ['state', 'workflow']
        db.delete_unique('workflows_workflowstate', ['state_id', 'workflow_id'])

        # Removing unique constraint on 'WorkflowInstanceActiveState', fields ['workflow_instance', 'state']
        db.delete_unique('workflows_workflowinstanceactivestate', ['workflow_instance_id', 'state_id'])

        # Adding model 'WorkflowStateAbilityGrant'
        db.create_table('workflows_workflowstateabilitygrant', (
            ('workflow_state', self.gf('django.db.models.fields.related.ForeignKey')(related_name='workflow_state_ability', to=orm['workflows.WorkflowState'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='workflow_state_ability_object', to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('workflows', ['WorkflowStateAbilityGrant'])

        # Adding model 'WorkflowStateTransition'
        db.create_table('workflows_workflowstatetransition', (
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('workflow_state_source', self.gf('django.db.models.fields.related.ForeignKey')(related_name='workflow_state_transition_source', to=orm['workflows.WorkflowState'])),
            ('transition', self.gf('django.db.models.fields.related.ForeignKey')(related_name='workflow_state_transition', to=orm['workflows.Transition'])),
            ('workflow_state_destination', self.gf('django.db.models.fields.related.ForeignKey')(related_name='workflow_state_transition_destination', to=orm['workflows.WorkflowState'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('workflows', ['WorkflowStateTransition'])

        # Adding model 'WorkflowStateTransitionAbility'
        db.create_table('workflows_workflowstatetransitionability', (
            ('ability', self.gf('django.db.models.fields.related.ForeignKey')(related_name='workflow_state_transition_ability', to=orm['workflows.Ability'])),
            ('attribute_comparison_operand', self.gf('django.db.models.fields.CharField')(default='and', max_length=8)),
            ('negate', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('workflows', ['WorkflowStateTransitionAbility'])

        # Adding model 'Transition'
        db.create_table('workflows_transition', (
            ('label', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('workflows', ['Transition'])

        # Deleting model 'WorkflowInstanceActiveState'
        db.delete_table('workflows_workflowinstanceactivestate')

        # Deleting model 'End'
        db.delete_table('workflows_end')

        # Deleting model 'WorkflowInstanceActiveNode'
        db.delete_table('workflows_workflowinstanceactivenode')

        # Deleting model 'Start'
        db.delete_table('workflows_start')

        # Deleting model 'WorkflowNode'
        db.delete_table('workflows_workflownode')

        # Deleting field 'Workflow.initial_node'
        db.delete_column('workflows_workflow', 'initial_node_id')

        # User chose to not deal with backwards NULL issues for 'WorkflowInstance.workflow_state'
        raise RuntimeError("Cannot reverse this migration. 'WorkflowInstance.workflow_state' and its values cannot be restored.")

        # Adding unique constraint on 'WorkflowInstance', fields ['object_id', 'content_type', 'workflow']
        db.create_unique('workflows_workflowinstance', ['object_id', 'content_type_id', 'workflow_id'])


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'workflows.ability': {
            'Meta': {'object_name': 'Ability'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'workflows.end': {
            'Meta': {'object_name': 'End'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'workflows.start': {
            'Meta': {'object_name': 'Start'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'})
        },
        'workflows.state': {
            'Meta': {'object_name': 'State'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'workflows.workflow': {
            'Meta': {'object_name': 'Workflow'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_node': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'workflow_initial_node'", 'null': 'True', 'to': "orm['workflows.WorkflowNode']"}),
            'initial_state': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'workflow_initial_state'", 'null': 'True', 'to': "orm['workflows.WorkflowState']"}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'workflows.workflowinstance': {
            'Meta': {'object_name': 'WorkflowInstance'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'workflow_instance_object'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workflows.Workflow']"})
        },
        'workflows.workflowinstanceactivenode': {
            'Meta': {'object_name': 'WorkflowInstanceActiveNode'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'workflow_instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workflows.WorkflowInstance']"}),
            'workflow_node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workflows.WorkflowNode']"})
        },
        'workflows.workflowinstanceactivestate': {
            'Meta': {'unique_together': "(('workflow_instance', 'state'),)", 'object_name': 'WorkflowInstanceActiveState'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workflows.State']", 'null': 'True'}),
            'workflow_instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workflows.WorkflowInstance']"})
        },
        'workflows.workflownode': {
            'Meta': {'object_name': 'WorkflowNode'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workflows.Workflow']"})
        },
        'workflows.workflowstate': {
            'Meta': {'unique_together': "(('workflow', 'state'),)", 'object_name': 'WorkflowState'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workflows.State']"}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workflows.Workflow']"})
        }
    }

    complete_apps = ['workflows']
