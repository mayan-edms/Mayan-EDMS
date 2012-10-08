# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'BootstrapSetup.created'
        db.add_column('bootstrap_bootstrapsetup', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 10, 8, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'BootstrapSetup.created'
        db.delete_column('bootstrap_bootstrapsetup', 'created')


    models = {
        'bootstrap.bootstrapsetup': {
            'Meta': {'ordering': "['name']", 'object_name': 'BootstrapSetup'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 10, 8, 0, 0)'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'fixture': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        }
    }

    complete_apps = ['bootstrap']