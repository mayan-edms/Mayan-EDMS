# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Installation.is_first_run'
        db.delete_column(u'installation_installation', 'is_first_run')


    def backwards(self, orm):
        # Adding field 'Installation.is_first_run'
        db.add_column(u'installation_installation', 'is_first_run',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    models = {
        u'installation.installation': {
            'Meta': {'object_name': 'Installation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "u'07356898-9962-44e8-ab5f-1c1735f9e306'", 'max_length': '48', 'blank': 'True'})
        }
    }

    complete_apps = ['installation']