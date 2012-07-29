# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TagProperties'
        db.create_table('tags_tagproperties', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['taggit.Tag'])),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal('tags', ['TagProperties'])


    def backwards(self, orm):
        # Deleting model 'TagProperties'
        db.delete_table('tags_tagproperties')


    models = {
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'tags.tagproperties': {
            'Meta': {'object_name': 'TagProperties'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['taggit.Tag']"})
        }
    }

    complete_apps = ['tags']