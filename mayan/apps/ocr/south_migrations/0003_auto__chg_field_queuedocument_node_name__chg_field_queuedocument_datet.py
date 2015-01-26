# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'QueueDocument.node_name'
        db.alter_column(u'ocr_queuedocument', 'node_name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True))

        # Changing field 'QueueDocument.datetime_submitted'
        db.alter_column(u'ocr_queuedocument', 'datetime_submitted', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

    def backwards(self, orm):

        # Changing field 'QueueDocument.node_name'
        db.alter_column(u'ocr_queuedocument', 'node_name', self.gf('django.db.models.fields.CharField')(max_length=32, null=True))

        # Changing field 'QueueDocument.datetime_submitted'
        db.alter_column(u'ocr_queuedocument', 'datetime_submitted', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

    models = {
        u'documents.document': {
            'Meta': {'ordering': "['-date_added']", 'object_name': 'Document'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'document_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'documents'", 'to': u"orm['documents.DocumentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "u'Uninitialized document'", 'max_length': '255', 'db_index': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "u'eng'", 'max_length': '8'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "u'4371aa11-0222-4718-bd94-c198fd7998e0'", 'max_length': '48'})
        },
        u'documents.documenttype': {
            'Meta': {'ordering': "['name']", 'object_name': 'DocumentType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'ocr': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'ocr.documentqueue': {
            'Meta': {'object_name': 'DocumentQueue'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'ocr.queuedocument': {
            'Meta': {'ordering': "('datetime_submitted',)", 'object_name': 'QueueDocument'},
            'datetime_submitted': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['documents.Document']"}),
            'document_queue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'documents'", 'to': u"orm['ocr.DocumentQueue']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'result': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['ocr']
