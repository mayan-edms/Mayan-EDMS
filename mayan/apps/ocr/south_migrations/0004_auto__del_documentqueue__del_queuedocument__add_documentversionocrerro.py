# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'DocumentQueue'
        db.delete_table(u'ocr_documentqueue')

        # Deleting model 'QueueDocument'
        db.delete_table(u'ocr_queuedocument')

        # Adding model 'DocumentVersionOCRError'
        db.create_table(u'ocr_documentversionocrerror', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('document_version', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documents.DocumentVersion'])),
            ('datetime_submitted', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
            ('result', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'ocr', ['DocumentVersionOCRError'])

    def backwards(self, orm):
        # Adding model 'DocumentQueue'
        db.create_table(u'ocr_documentqueue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, unique=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'ocr', ['DocumentQueue'])

        # Adding model 'QueueDocument'
        db.create_table(u'ocr_queuedocument', (
            ('node_name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('result', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('datetime_submitted', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True, db_index=True)),
            ('document_queue', self.gf('django.db.models.fields.related.ForeignKey')(related_name='documents', to=orm['ocr.DocumentQueue'])),
            ('document', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documents.Document'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'ocr', ['QueueDocument'])

        # Deleting model 'DocumentVersionOCRError'
        db.delete_table(u'ocr_documentversionocrerror')

    models = {
        u'documents.document': {
            'Meta': {'ordering': "['-date_added']", 'object_name': 'Document'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'document_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'documents'", 'to': u"orm['documents.DocumentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "u'Uninitialized document'", 'max_length': '255', 'db_index': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "u'eng'", 'max_length': '8'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "u'b5b498b5-ffe5-4b70-b8a6-6c875ed11bf2'", 'max_length': '48'})
        },
        u'documents.documenttype': {
            'Meta': {'ordering': "['name']", 'object_name': 'DocumentType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'ocr': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'documents.documentversion': {
            'Meta': {'object_name': 'DocumentVersion'},
            'checksum': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'versions'", 'to': u"orm['documents.Document']"}),
            'encoding': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mimetype': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'ocr.documentversionocrerror': {
            'Meta': {'ordering': "('datetime_submitted',)", 'object_name': 'DocumentVersionOCRError'},
            'datetime_submitted': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'document_version': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['documents.DocumentVersion']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'result': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['ocr']
