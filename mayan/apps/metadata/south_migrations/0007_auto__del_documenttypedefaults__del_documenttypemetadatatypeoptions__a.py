# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'DocumentTypeDefaults'
        db.delete_table(u'metadata_documenttypedefaults')

        # Deleting model 'DocumentTypeMetadataTypeOptions'
        db.delete_table(u'metadata_documenttypemetadatatypeoptions')

        # Adding model 'DocumentTypeMetadataType'
        db.create_table(u'metadata_documenttypemetadatatype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('document_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documents.DocumentType'])),
            ('metadata_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['metadata.MetadataType'])),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'metadata', ['DocumentTypeMetadataType'])

    def backwards(self, orm):
        # Adding model 'DocumentTypeDefaults'
        db.create_table(u'metadata_documenttypedefaults', (
            ('document_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documents.DocumentType'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'metadata', ['DocumentTypeDefaults'])

        # Adding model 'DocumentTypeMetadataTypeOptions'
        db.create_table(u'metadata_documenttypemetadatatypeoptions', (
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('metadata_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['metadata.MetadataType'])),
            ('document_type_defaults', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['metadata.DocumentTypeDefaults'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'metadata', ['DocumentTypeMetadataTypeOptions'])

        # Deleting model 'DocumentTypeMetadataType'
        db.delete_table(u'metadata_documenttypemetadatatype')

    models = {
        u'documents.document': {
            'Meta': {'ordering': "['-date_added']", 'object_name': 'Document'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'document_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'documents'", 'to': u"orm['documents.DocumentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "u'Uninitialized document'", 'max_length': '255', 'db_index': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "u'eng'", 'max_length': '8'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "u'7f0e4ea9-c307-4395-ab9e-63979ea1c4ae'", 'max_length': '48'})
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
            'value': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'metadata.documenttypemetadatatype': {
            'Meta': {'object_name': 'DocumentTypeMetadataType'},
            'document_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['documents.DocumentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['metadata.MetadataType']"}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
