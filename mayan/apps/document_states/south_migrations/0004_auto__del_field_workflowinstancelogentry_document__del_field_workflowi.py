# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'WorkflowInstanceLogEntry.document'
        db.delete_column(u'document_states_workflowinstancelogentry', 'document_id')

        # Deleting field 'WorkflowInstanceLogEntry.workflow_instace'
        db.delete_column(u'document_states_workflowinstancelogentry', 'workflow_instace_id')

        # Adding field 'WorkflowInstanceLogEntry.workflow_instance'
        db.add_column(u'document_states_workflowinstancelogentry', 'workflow_instance',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name=u'log_entries', to=orm['document_states.WorkflowInstance']),
                      keep_default=False)

        # Adding field 'WorkflowInstanceLogEntry.transition'
        db.add_column(u'document_states_workflowinstancelogentry', 'transition',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['document_states.WorkflowTransition']),
                      keep_default=False)

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'WorkflowInstanceLogEntry.document'
        raise RuntimeError("Cannot reverse this migration. 'WorkflowInstanceLogEntry.document' and its values cannot be restored.")

        # The following code is provided here to aid in writing a correct migration        # Adding field 'WorkflowInstanceLogEntry.document'
        db.add_column(u'document_states_workflowinstancelogentry', 'document',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documents.Document']),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'WorkflowInstanceLogEntry.workflow_instace'
        raise RuntimeError("Cannot reverse this migration. 'WorkflowInstanceLogEntry.workflow_instace' and its values cannot be restored.")

        # The following code is provided here to aid in writing a correct migration        # Adding field 'WorkflowInstanceLogEntry.workflow_instace'
        db.add_column(u'document_states_workflowinstancelogentry', 'workflow_instace',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['document_states.WorkflowInstance']),
                      keep_default=False)

        # Deleting field 'WorkflowInstanceLogEntry.workflow_instance'
        db.delete_column(u'document_states_workflowinstancelogentry', 'workflow_instance_id')

        # Deleting field 'WorkflowInstanceLogEntry.transition'
        db.delete_column(u'document_states_workflowinstancelogentry', 'transition_id')

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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'transition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['document_states.WorkflowTransition']"}),
            'workflow_instance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'log_entries'", 'to': u"orm['document_states.WorkflowInstance']"})
        },
        u'document_states.workflowstate': {
            'Meta': {'object_name': 'WorkflowState'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'states'", 'to': u"orm['document_states.Workflow']"})
        },
        u'document_states.workflowtransition': {
            'Meta': {'unique_together': "((u'workflow', u'origin_state', u'destination_state'),)", 'object_name': 'WorkflowTransition'},
            'destination_state': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'destinations'", 'to': u"orm['document_states.WorkflowState']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'origin_state': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'origins'", 'to': u"orm['document_states.WorkflowState']"}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'transitions'", 'to': u"orm['document_states.Workflow']"})
        },
        u'documents.document': {
            'Meta': {'ordering': "['-date_added']", 'object_name': 'Document'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'document_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'documents'", 'to': u"orm['documents.DocumentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "u'Uninitialized document'", 'max_length': '255', 'db_index': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "u'eng'", 'max_length': '8'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "u'3d36ed9d-3356-4f96-ae65-da677128e0c3'", 'max_length': '48'})
        },
        u'documents.documenttype': {
            'Meta': {'ordering': "['name']", 'object_name': 'DocumentType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'ocr': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['document_states']
