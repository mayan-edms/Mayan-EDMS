# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'DocumentQueue.state'
        db.delete_column(u'ocr_documentqueue', 'state')

        # Deleting field 'QueueDocument.delay'
        db.delete_column(u'ocr_queuedocument', 'delay')

        # Deleting field 'QueueDocument.state'
        db.delete_column(u'ocr_queuedocument', 'state')

    def backwards(self, orm):
        # Adding field 'DocumentQueue.state'
        db.add_column(u'ocr_documentqueue', 'state',
                      self.gf('django.db.models.fields.CharField')(default='a', max_length=4),
                      keep_default=False)

        # Adding field 'QueueDocument.delay'
        db.add_column(u'ocr_queuedocument', 'delay',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'QueueDocument.state'
        db.add_column(u'ocr_queuedocument', 'state',
                      self.gf('django.db.models.fields.CharField')(default='p', max_length=4),
                      keep_default=False)

    models = {
        u'documents.document': {
            'Meta': {'ordering': "['-date_added']", 'object_name': 'Document'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'document_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['documents.DocumentType']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '48', 'blank': 'True'})
        },
        u'documents.documenttype': {
            'Meta': {'ordering': "['name']", 'object_name': 'DocumentType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        },
        u'ocr.documentqueue': {
            'Meta': {'object_name': 'DocumentQueue'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'ocr.queuedocument': {
            'Meta': {'ordering': "('datetime_submitted',)", 'object_name': 'QueueDocument'},
            'datetime_submitted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['documents.Document']"}),
            'document_queue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'documents'", 'to': u"orm['ocr.DocumentQueue']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node_name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'result': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['ocr']
