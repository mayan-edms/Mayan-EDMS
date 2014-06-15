# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Installation'
        db.create_table('installation_installation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lock_id', self.gf('django.db.models.fields.CharField')(default=1, unique=True, max_length=1)),
            ('is_first_run', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=48, blank=True)),
        ))
        db.send_create_signal('installation', ['Installation'])


    def backwards(self, orm):
        # Deleting model 'Installation'
        db.delete_table('installation_installation')


    models = {
        'installation.installation': {
            'Meta': {'object_name': 'Installation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_first_run': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lock_id': ('django.db.models.fields.CharField', [], {'default': '1', 'unique': 'True', 'max_length': '1'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '48', 'blank': 'True'})
        }
    }

    complete_apps = ['installation']