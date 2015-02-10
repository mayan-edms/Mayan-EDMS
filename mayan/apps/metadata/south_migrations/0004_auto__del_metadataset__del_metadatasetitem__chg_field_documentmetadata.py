# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'MetadataSet'
        db.delete_table(u'metadata_metadataset')

        # Deleting model 'MetadataSetItem'
        db.delete_table(u'metadata_metadatasetitem')

        # Removing M2M table for field default_metadata_sets on 'DocumentTypeDefaults'
        db.delete_table(db.shorten_name(u'metadata_documenttypedefaults_default_metadata_sets'))

        # Changing field 'DocumentMetadata.value'
        db.alter_column(u'metadata_documentmetadata', 'value', self.gf('django.db.models.fields.CharField')(max_length=255))

    def backwards(self, orm):
        # Adding model 'MetadataSet'
        db.create_table(u'metadata_metadataset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=48, unique=True)),
        ))
        db.send_create_signal('metadata', ['MetadataSet'])

        # Adding model 'MetadataSetItem'
        db.create_table(u'metadata_metadatasetitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('metadata_set', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['metadata.MetadataSet'])),
            ('metadata_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['metadata.MetadataType'])),
        ))
        db.send_create_signal('metadata', ['MetadataSetItem'])

        # Adding M2M table for field default_metadata_sets on 'DocumentTypeDefaults'
        m2m_table_name = db.shorten_name(u'metadata_documenttypedefaults_default_metadata_sets')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('documenttypedefaults', models.ForeignKey(orm['metadata.documenttypedefaults'], null=False)),
            ('metadataset', models.ForeignKey(orm['metadata.metadataset'], null=False))
        ))
        db.create_unique(m2m_table_name, ['documenttypedefaults_id', 'metadataset_id'])

        # Changing field 'DocumentMetadata.value'
        db.alter_column(u'metadata_documentmetadata', 'value', self.gf('django.db.models.fields.CharField')(max_length=256))

    models = {
        u'documents.document': {
            'Meta': {'ordering': "['-date_added']", 'object_name': 'Document'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'document_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'documents'", 'to': u"orm['documents.DocumentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '48', 'blank': 'True'})
        },
        u'documents.documenttype': {
            'Meta': {'ordering': "['name']", 'object_name': 'DocumentType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'ocr': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'metadata.documentmetadata': {
            'Meta': {'object_name': 'DocumentMetadata'},
            'document': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'metadata'", 'to': u"orm['documents.Document']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['metadata.MetadataType']"}),
            'value': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'blank': 'True'})
        },
        u'metadata.documenttypedefaults': {
            'Meta': {'object_name': 'DocumentTypeDefaults'},
            'default_metadata': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['metadata.MetadataType']", 'symmetrical': 'False', 'blank': 'True'}),
            'document_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['documents.DocumentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'metadata.metadatatype': {
            'Meta': {'ordering': "('title',)", 'object_name': 'MetadataType'},
            'default': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lookup': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '48'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '48', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['metadata']
