# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Ability'
        db.create_table('workflows_ability', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('workflows', ['Ability'])

        # Adding model 'Workflow'
        db.create_table('workflows_workflow', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('initial_state', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='workflow_initial_state', null=True, to=orm['workflows.WorkflowState'])),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('workflows', ['Workflow'])

        # Adding model 'State'
        db.create_table('workflows_state', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('workflows', ['State'])

        # Adding model 'Transition'
        db.create_table('workflows_transition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('workflows', ['Transition'])

        # Adding model 'WorkflowState'
        db.create_table('workflows_workflowstate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('workflow', self.gf('django.db.models.fields.related.ForeignKey')(related_name='workflow_state_workflow', to=orm['workflows.Workflow'])),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(related_name='workflow_state_state', to=orm['workflows.State'])),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('workflows', ['WorkflowState'])

        # Adding model 'WorkflowStateAbilityGrant'
        db.create_table('workflows_workflowstateabilitygrant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('workflow_state', self.gf('django.db.models.fields.related.ForeignKey')(related_name='workflow_state_ability', to=orm['workflows.WorkflowState'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='workflow_state_ability_object', to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('workflows', ['WorkflowStateAbilityGrant'])

        # Adding model 'WorkflowStateTransition'
        db.create_table('workflows_workflowstatetransition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('workflow_state_source', self.gf('django.db.models.fields.related.ForeignKey')(related_name='workflow_state_transition_source', to=orm['workflows.WorkflowState'])),
            ('transition', self.gf('django.db.models.fields.related.ForeignKey')(related_name='workflow_state_transition', to=orm['workflows.Transition'])),
            ('workflow_state_destination', self.gf('django.db.models.fields.related.ForeignKey')(related_name='workflow_state_transition_destination', to=orm['workflows.WorkflowState'])),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('workflows', ['WorkflowStateTransition'])

        # Adding model 'WorkflowStateTransitionAbility'
        db.create_table('workflows_workflowstatetransitionability', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('attribute_comparison_operand', self.gf('django.db.models.fields.CharField')(default='and', max_length=8)),
            ('negate', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ability', self.gf('django.db.models.fields.related.ForeignKey')(related_name='workflow_state_transition_ability', to=orm['workflows.Ability'])),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('workflows', ['WorkflowStateTransitionAbility'])

        # Adding model 'WorkflowInstance'
        db.create_table('workflows_workflowinstance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('workflow', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workflows.Workflow'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='workflow_instance_object', to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('workflow_state', self.gf('django.db.models.fields.related.ForeignKey')(related_name='workflow_instance_state', to=orm['workflows.WorkflowState'])),
        ))
        db.send_create_signal('workflows', ['WorkflowInstance'])

        # Adding unique constraint on 'WorkflowInstance', fields ['content_type', 'object_id', 'workflow']
        db.create_unique('workflows_workflowinstance', ['content_type_id', 'object_id', 'workflow_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'WorkflowInstance', fields ['content_type', 'object_id', 'workflow']
        db.delete_unique('workflows_workflowinstance', ['content_type_id', 'object_id', 'workflow_id'])

        # Deleting model 'Ability'
        db.delete_table('workflows_ability')

        # Deleting model 'Workflow'
        db.delete_table('workflows_workflow')

        # Deleting model 'State'
        db.delete_table('workflows_state')

        # Deleting model 'Transition'
        db.delete_table('workflows_transition')

        # Deleting model 'WorkflowState'
        db.delete_table('workflows_workflowstate')

        # Deleting model 'WorkflowStateAbilityGrant'
        db.delete_table('workflows_workflowstateabilitygrant')

        # Deleting model 'WorkflowStateTransition'
        db.delete_table('workflows_workflowstatetransition')

        # Deleting model 'WorkflowStateTransitionAbility'
        db.delete_table('workflows_workflowstatetransitionability')

        # Deleting model 'WorkflowInstance'
        db.delete_table('workflows_workflowinstance')


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
        'workflows.state': {
            'Meta': {'object_name': 'State'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'workflows.transition': {
            'Meta': {'object_name': 'Transition'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'workflows.workflow': {
            'Meta': {'object_name': 'Workflow'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_state': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'workflow_initial_state'", 'null': 'True', 'to': "orm['workflows.WorkflowState']"}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'workflows.workflowinstance': {
            'Meta': {'unique_together': "(('content_type', 'object_id', 'workflow'),)", 'object_name': 'WorkflowInstance'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'workflow_instance_object'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workflows.Workflow']"}),
            'workflow_state': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'workflow_instance_state'", 'to': "orm['workflows.WorkflowState']"})
        },
        'workflows.workflowstate': {
            'Meta': {'object_name': 'WorkflowState'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'workflow_state_state'", 'to': "orm['workflows.State']"}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'workflow_state_workflow'", 'to': "orm['workflows.Workflow']"})
        },
        'workflows.workflowstateabilitygrant': {
            'Meta': {'object_name': 'WorkflowStateAbilityGrant'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'workflow_state_ability_object'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'workflow_state': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'workflow_state_ability'", 'to': "orm['workflows.WorkflowState']"})
        },
        'workflows.workflowstatetransition': {
            'Meta': {'object_name': 'WorkflowStateTransition'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'transition': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'workflow_state_transition'", 'to': "orm['workflows.Transition']"}),
            'workflow_state_destination': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'workflow_state_transition_destination'", 'to': "orm['workflows.WorkflowState']"}),
            'workflow_state_source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'workflow_state_transition_source'", 'to': "orm['workflows.WorkflowState']"})
        },
        'workflows.workflowstatetransitionability': {
            'Meta': {'object_name': 'WorkflowStateTransitionAbility'},
            'ability': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'workflow_state_transition_ability'", 'to': "orm['workflows.Ability']"}),
            'attribute_comparison_operand': ('django.db.models.fields.CharField', [], {'default': "'and'", 'max_length': '8'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'negate': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['workflows']
