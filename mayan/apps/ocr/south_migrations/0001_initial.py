# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DocumentQueue'
        db.create_table(u'ocr_documentqueue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('state', self.gf('django.db.models.fields.CharField')(default='a', max_length=4)),
        ))
        db.send_create_signal(u'ocr', ['DocumentQueue'])

        # Adding model 'QueueDocument'
        db.create_table(u'ocr_queuedocument', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('document_queue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ocr.DocumentQueue'])),
            ('document', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documents.Document'])),
            ('datetime_submitted', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('delay', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('state', self.gf('django.db.models.fields.CharField')(default='p', max_length=4)),
            ('result', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('node_name', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
        ))
        db.send_create_signal(u'ocr', ['QueueDocument'])

    def backwards(self, orm):
        # Deleting model 'DocumentQueue'
        db.delete_table(u'ocr_documentqueue')

        # Deleting model 'QueueDocument'
        db.delete_table(u'ocr_queuedocument')

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
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'a'", 'max_length': '4'})
        },
        u'ocr.queuedocument': {
            'Meta': {'ordering': "('datetime_submitted',)", 'object_name': 'QueueDocument'},
            'datetime_submitted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'delay': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['documents.Document']"}),
            'document_queue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ocr.DocumentQueue']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node_name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'result': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'p'", 'max_length': '4'})
        }
    }

    complete_apps = ['ocr']
