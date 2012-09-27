# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'AutoAdminSingleton'
        db.delete_table('common_autoadminsingleton')


    def backwards(self, orm):
        # Adding model 'AutoAdminSingleton'
        db.create_table('common_autoadminsingleton', (
            ('lock_id', self.gf('django.db.models.fields.CharField')(default=1, max_length=1, unique=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='auto_admin_account', null=True, to=orm['auth.User'], blank=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password_hash', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
        ))
        db.send_create_signal('common', ['AutoAdminSingleton'])


    models = {
        'common.anonymoususersingleton': {
            'Meta': {'object_name': 'AnonymousUserSingleton'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lock_id': ('django.db.models.fields.CharField', [], {'default': '1', 'unique': 'True', 'max_length': '1'})
        }
    }

    complete_apps = ['common']