# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'RegistrationSingleton.lock_id'
        db.delete_column(u'registration_registrationsingleton', 'lock_id')

    def backwards(self, orm):
        # Adding field 'RegistrationSingleton.lock_id'
        db.add_column(u'registration_registrationsingleton', 'lock_id',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=1, unique=True),
                      keep_default=False)

    models = {
        u'registration.registrationsingleton': {
            'Meta': {'object_name': 'RegistrationSingleton'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'registered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'registration_data': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['registration']
