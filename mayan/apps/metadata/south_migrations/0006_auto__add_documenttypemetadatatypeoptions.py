# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DocumentTypeMetadataTypeOptions'
        db.create_table(u'metadata_documenttypemetadatatypeoptions', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('document_type_defaults', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['metadata.DocumentTypeDefaults'])),
            ('metadata_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['metadata.MetadataType'])),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'metadata', ['DocumentTypeMetadataTypeOptions'])

        # Removing M2M table for field default_metadata on 'DocumentTypeDefaults'
        db.delete_table(db.shorten_name(u'metadata_documenttypedefaults_default_metadata'))

    def backwards(self, orm):
        # Deleting model 'DocumentTypeMetadataTypeOptions'
        db.delete_table(u'metadata_documenttypemetadatatypeoptions')

        # Adding M2M table for field default_metadata on 'DocumentTypeDefaults'
        m2m_table_name = db.shorten_name(u'metadata_documenttypedefaults_default_metadata')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('documenttypedefaults', models.ForeignKey(orm[u'metadata.documenttypedefaults'], null=False)),
            ('metadatatype', models.ForeignKey(orm[u'metadata.metadatatype'], null=False))
        ))
        db.create_unique(m2m_table_name, ['documenttypedefaults_id', 'metadatatype_id'])

    models = {
        u'documents.document': {
            'Meta': {'ordering': "['-date_added']", 'object_name': 'Document'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'document_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'documents'", 'to': u"orm['documents.DocumentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "u'Uninitialized document'", 'max_length': '255', 'db_index': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "u'eng'", 'max_length': '8'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "u'e432f139-04cf-49e3-a9d1-3644dda3026e'", 'max_length': '48'})
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
        u'metadata.documenttypedefaults': {
            'Meta': {'object_name': 'DocumentTypeDefaults'},
            'default_metadata': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['metadata.MetadataType']", 'symmetrical': 'False', 'through': u"orm['metadata.DocumentTypeMetadataTypeOptions']", 'blank': 'True'}),
            'document_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['documents.DocumentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'metadata.documenttypemetadatatypeoptions': {
            'Meta': {'object_name': 'DocumentTypeMetadataTypeOptions'},
            'document_type_defaults': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['metadata.DocumentTypeDefaults']"}),
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
