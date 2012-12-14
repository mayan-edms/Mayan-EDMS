# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BootstrapSetup'
        db.create_table('bootstrap_bootstrapsetup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('fixture', self.gf('django.db.models.fields.TextField')()),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal('bootstrap', ['BootstrapSetup'])


    def backwards(self, orm):
        # Deleting model 'BootstrapSetup'
        db.delete_table('bootstrap_bootstrapsetup')


    models = {
        'bootstrap.bootstrapsetup': {
            'Meta': {'ordering': "['name']", 'object_name': 'BootstrapSetup'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'fixture': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        }
    }

    complete_apps = ['bootstrap']
