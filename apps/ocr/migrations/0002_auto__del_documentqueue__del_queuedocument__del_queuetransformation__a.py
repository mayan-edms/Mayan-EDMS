# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'DocumentQueue'
        db.delete_table('ocr_documentqueue')

        # Deleting model 'QueueDocument'
        db.delete_table('ocr_queuedocument')

        # Deleting model 'QueueTransformation'
        db.delete_table('ocr_queuetransformation')

        # Adding model 'OCRProcessingSingleton'
        db.create_table('ocr_ocrprocessingsingleton', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lock_id', self.gf('django.db.models.fields.CharField')(default=1, unique=True, max_length=1)),
            ('state', self.gf('django.db.models.fields.CharField')(default='a', max_length=4)),
        ))
        db.send_create_signal('ocr', ['OCRProcessingSingleton'])


    def backwards(self, orm):
        # Adding model 'DocumentQueue'
        db.create_table('ocr_documentqueue', (
            ('state', self.gf('django.db.models.fields.CharField')(default='a', max_length=4)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, unique=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('ocr', ['DocumentQueue'])

        # Adding model 'QueueDocument'
        db.create_table('ocr_queuedocument', (
            ('delay', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('state', self.gf('django.db.models.fields.CharField')(default='p', max_length=4)),
            ('result', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('datetime_submitted', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True, db_index=True)),
            ('document_queue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ocr.DocumentQueue'])),
            ('document_version', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documents.DocumentVersion'])),
            ('document', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documents.Document'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('node_name', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
        ))
        db.send_create_signal('ocr', ['QueueDocument'])

        # Adding model 'QueueTransformation'
        db.create_table('ocr_queuetransformation', (
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('arguments', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True, blank=True, db_index=True)),
            ('transformation', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('ocr', ['QueueTransformation'])

        # Deleting model 'OCRProcessingSingleton'
        db.delete_table('ocr_ocrprocessingsingleton')


    models = {
        'ocr.ocrprocessingsingleton': {
            'Meta': {'object_name': 'OCRProcessingSingleton'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lock_id': ('django.db.models.fields.CharField', [], {'default': '1', 'unique': 'True', 'max_length': '1'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'a'", 'max_length': '4'})
        }
    }

    complete_apps = ['ocr']