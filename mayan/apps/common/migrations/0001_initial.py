# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AnonymousUserSingleton'
        db.create_table('common_anonymoususersingleton', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lock_id', self.gf('django.db.models.fields.CharField')(default=1, unique=True, max_length=1)),
        ))
        db.send_create_signal('common', ['AnonymousUserSingleton'])


    def backwards(self, orm):
        # Deleting model 'AnonymousUserSingleton'
        db.delete_table('common_anonymoususersingleton')


    models = {
        'common.anonymoususersingleton': {
            'Meta': {'object_name': 'AnonymousUserSingleton'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lock_id': ('django.db.models.fields.CharField', [], {'default': '1', 'unique': 'True', 'max_length': '1'})
        }
    }

    complete_apps = ['common']