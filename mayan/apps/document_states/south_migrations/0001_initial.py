# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Workflow'
        db.create_table(u'document_states_workflow', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'document_states', ['Workflow'])

        # Adding model 'WorkflowState'
        db.create_table(u'document_states_workflowstate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('workflow', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['document_states.Workflow'])),
            ('label', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('initial', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'document_states', ['WorkflowState'])

        # Adding model 'WorkflowTransition'
        db.create_table(u'document_states_workflowtransition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('origin_state', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'origins', to=orm['document_states.WorkflowState'])),
            ('destination_state', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'destinations', to=orm['document_states.WorkflowState'])),
        ))
        db.send_create_signal(u'document_states', ['WorkflowTransition'])

        # Adding model 'DocumentTypeWorkflow'
        db.create_table(u'document_states_documenttypeworkflow', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('document_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documents.DocumentType'])),
            ('workflow', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['document_states.Workflow'])),
        ))
        db.send_create_signal(u'document_states', ['DocumentTypeWorkflow'])

        # Adding unique constraint on 'DocumentTypeWorkflow', fields ['document_type', 'workflow']
        db.create_unique(u'document_states_documenttypeworkflow', ['document_type_id', 'workflow_id'])

        # Adding model 'WorkflowInstance'
        db.create_table(u'document_states_workflowinstance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('workflow', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['document_states.Workflow'])),
            ('document', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documents.Document'])),
        ))
        db.send_create_signal(u'document_states', ['WorkflowInstance'])

        # Adding unique constraint on 'WorkflowInstance', fields ['document', 'workflow']
        db.create_unique(u'document_states_workflowinstance', ['document_id', 'workflow_id'])

        # Adding model 'WorkflowInstanceLogEntry'
        db.create_table(u'document_states_workflowinstancelogentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('workflow_instace', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['document_states.WorkflowInstance'])),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('document', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documents.Document'])),
        ))
        db.send_create_signal(u'document_states', ['WorkflowInstanceLogEntry'])

    def backwards(self, orm):
        # Removing unique constraint on 'WorkflowInstance', fields ['document', 'workflow']
        db.delete_unique(u'document_states_workflowinstance', ['document_id', 'workflow_id'])

        # Removing unique constraint on 'DocumentTypeWorkflow', fields ['document_type', 'workflow']
        db.delete_unique(u'document_states_documenttypeworkflow', ['document_type_id', 'workflow_id'])

        # Deleting model 'Workflow'
        db.delete_table(u'document_states_workflow')

        # Deleting model 'WorkflowState'
        db.delete_table(u'document_states_workflowstate')

        # Deleting model 'WorkflowTransition'
        db.delete_table(u'document_states_workflowtransition')

        # Deleting model 'DocumentTypeWorkflow'
        db.delete_table(u'document_states_documenttypeworkflow')

        # Deleting model 'WorkflowInstance'
        db.delete_table(u'document_states_workflowinstance')

        # Deleting model 'WorkflowInstanceLogEntry'
        db.delete_table(u'document_states_workflowinstancelogentry')

    models = {
        u'document_states.documenttypeworkflow': {
            'Meta': {'unique_together': "((u'document_type', u'workflow'),)", 'object_name': 'DocumentTypeWorkflow'},
            'document_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['documents.DocumentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['document_states.Workflow']"})
        },
        u'document_states.workflow': {
            'Meta': {'object_name': 'Workflow'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'document_states.workflowinstance': {
            'Meta': {'unique_together': "((u'document', u'workflow'),)", 'object_name': 'WorkflowInstance'},
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['documents.Document']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['document_states.Workflow']"})
        },
        u'document_states.workflowinstancelogentry': {
            'Meta': {'object_name': 'WorkflowInstanceLogEntry'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['documents.Document']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'workflow_instace': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['document_states.WorkflowInstance']"})
        },
        u'document_states.workflowstate': {
            'Meta': {'object_name': 'WorkflowState'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['document_states.Workflow']"})
        },
        u'document_states.workflowtransition': {
            'Meta': {'object_name': 'WorkflowTransition'},
            'destination_state': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'destinations'", 'to': u"orm['document_states.WorkflowState']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'origin_state': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'origins'", 'to': u"orm['document_states.WorkflowState']"})
        },
        u'documents.document': {
            'Meta': {'ordering': "['-date_added']", 'object_name': 'Document'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'document_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'documents'", 'to': u"orm['documents.DocumentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "u'Uninitialized document'", 'max_length': '255', 'db_index': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "u'eng'", 'max_length': '8'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "u'8fff74c9-2f45-4a2a-bbdc-2ce727ab9380'", 'max_length': '48'})
        },
        u'documents.documenttype': {
            'Meta': {'ordering': "['name']", 'object_name': 'DocumentType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'ocr': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['document_states']
