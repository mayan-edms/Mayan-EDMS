# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'WorkflowTransition', fields ['workflow', 'origin_state', 'destination_state']
        db.delete_unique(u'document_states_workflowtransition', ['workflow_id', 'origin_state_id', 'destination_state_id'])

        # Removing unique constraint on 'WorkflowTransition', fields ['label']
        db.delete_unique(u'document_states_workflowtransition', ['label'])

        # Adding unique constraint on 'WorkflowTransition', fields ['workflow', 'label', 'origin_state', 'destination_state']
        db.create_unique(u'document_states_workflowtransition', ['workflow_id', 'label', 'origin_state_id', 'destination_state_id'])

    def backwards(self, orm):
        # Removing unique constraint on 'WorkflowTransition', fields ['workflow', 'label', 'origin_state', 'destination_state']
        db.delete_unique(u'document_states_workflowtransition', ['workflow_id', 'label', 'origin_state_id', 'destination_state_id'])

        # Adding unique constraint on 'WorkflowTransition', fields ['label']
        db.create_unique(u'document_states_workflowtransition', ['label'])

        # Adding unique constraint on 'WorkflowTransition', fields ['workflow', 'origin_state', 'destination_state']
        db.create_unique(u'document_states_workflowtransition', ['workflow_id', 'origin_state_id', 'destination_state_id'])

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
            'Meta': {'unique_together': "((u'workflow', u'label'),)", 'object_name': 'WorkflowState'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'states'", 'to': u"orm['document_states.Workflow']"})
        },
        u'document_states.workflowtransition': {
            'Meta': {'unique_together': "((u'workflow', u'label', u'origin_state', u'destination_state'),)", 'object_name': 'WorkflowTransition'},
            'destination_state': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'destinations'", 'to': u"orm['document_states.WorkflowState']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "u'59ce9910-80b7-48b3-8a1a-e9ac0fb412f0'", 'max_length': '48'})
        },
        u'documents.documenttype': {
            'Meta': {'ordering': "['name']", 'object_name': 'DocumentType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'ocr': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['document_states']
