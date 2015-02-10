# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    depends_on = (
        ('documents', '0001_initial'),
        ('actstream', '0007_auto__add_field_follow_started'),
    )

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table(u'tags_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal(u'tags', ['Tag'])

        # Adding M2M table for field document on 'Tag'
        m2m_table_name = db.shorten_name(u'tags_tag_document')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(primary_key=True, auto_created=True)),
            ('tag', models.ForeignKey(orm[u'tags.tag'], null=False)),
            ('document', models.ForeignKey(orm[u'documents.document'], null=False))
        ))
        db.create_unique(m2m_table_name, ['tag_id', 'document_id'])

    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table(u'tags_tag')

        # Removing M2M table for field document on 'Tag'
        db.delete_table(db.shorten_name(u'tags_tag_document'))

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
