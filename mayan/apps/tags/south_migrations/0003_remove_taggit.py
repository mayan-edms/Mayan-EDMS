# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import DataMigration
from django.db import models, transaction
from django.db.utils import ProgrammingError


class Migration(DataMigration):
    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName".
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.

        try:
            with transaction.atomic():
                for tag in orm['taggit.tag'].objects.all():
                    color = orm.TagProperties.objects.get(tag=tag).color
                    orm.Tag.objects.create(label=tag.name, color=color)
        except ProgrammingError:
            # Ignore this error because it is expected when migrating a new
            # install, in this situation the django-taggit table never existed
            pass

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        u'documents.document': {
            'Meta': {'ordering': "['-date_added']", 'object_name': 'Document'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'document_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'documents'", 'null': 'True', 'to': u"orm['documents.DocumentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '48', 'blank': 'True'})
        },
        u'documents.documenttype': {
            'Meta': {'ordering': "['name']", 'object_name': 'DocumentType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        },
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'tags.tag': {
            'Meta': {'object_name': 'Tag'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'document': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['documents.Document']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'})
        },
        u'tags.tagproperties': {
            'Meta': {'object_name': 'TagProperties'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'properties'", 'to': u"orm['tags.Tag']"})
        }
    }

    complete_apps = ['tags']
    symmetrical = True
