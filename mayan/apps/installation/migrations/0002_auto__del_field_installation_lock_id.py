# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Installation.lock_id'
        db.delete_column(u'installation_installation', 'lock_id')

    def backwards(self, orm):
        # Adding field 'Installation.lock_id'
        db.add_column(u'installation_installation', 'lock_id',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=1, unique=True),
                      keep_default=False)

    models = {
        u'installation.installation': {
            'Meta': {'object_name': 'Installation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_first_run': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "u'745d2184-d011-4a19-a3d9-df3bab80f82c'", 'max_length': '48', 'blank': 'True'})
        }
    }

    complete_apps = ['installation']
