# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TrashCan'
        db.create_table('trash_trashcan', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
        ))
        db.send_create_signal('trash', ['TrashCan'])

        # Adding model 'TrashCanItem'
        db.create_table('trash_trashcanitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trash_can', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trash.TrashCan'])),
            ('trashed_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('trash', ['TrashCanItem'])

        # Adding unique constraint on 'TrashCanItem', fields ['trash_can', 'content_type', 'object_id']
        db.create_unique('trash_trashcanitem', ['trash_can_id', 'content_type_id', 'object_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'TrashCanItem', fields ['trash_can', 'content_type', 'object_id']
        db.delete_unique('trash_trashcanitem', ['trash_can_id', 'content_type_id', 'object_id'])

        # Deleting model 'TrashCan'
        db.delete_table('trash_trashcan')

        # Deleting model 'TrashCanItem'
        db.delete_table('trash_trashcanitem')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'trash.trashcan': {
            'Meta': {'object_name': 'TrashCan'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        },
        'trash.trashcanitem': {
            'Meta': {'unique_together': "(('trash_can', 'content_type', 'object_id'),)", 'object_name': 'TrashCanItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'trash_can': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['trash.TrashCan']"}),
            'trashed_at': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['trash']