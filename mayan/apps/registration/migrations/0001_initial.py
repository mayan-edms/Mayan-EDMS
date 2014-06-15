# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RegistrationSingleton'
        db.create_table('registration_registrationsingleton', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lock_id', self.gf('django.db.models.fields.CharField')(default=1, unique=True, max_length=1)),
            ('registered', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('registration_data', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('registration', ['RegistrationSingleton'])


    def backwards(self, orm):
        # Deleting model 'RegistrationSingleton'
        db.delete_table('registration_registrationsingleton')


    models = {
        'registration.registrationsingleton': {
            'Meta': {'object_name': 'RegistrationSingleton'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lock_id': ('django.db.models.fields.CharField', [], {'default': '1', 'unique': 'True', 'max_length': '1'}),
            'registered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'registration_data': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['registration']