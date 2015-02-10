# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TagProperties'
        db.create_table(u'tags_tagproperties', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag_id', self.gf('django.db.models.fields.IntegerField')()),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal(u'tags', ['TagProperties'])

    def backwards(self, orm):
        # Deleting model 'TagProperties'
        db.delete_table(u'tags_tagproperties')

    models = {
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'tags.tagproperties': {
            'Meta': {'object_name': 'TagProperties'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag_id': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['tags']
