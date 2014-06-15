# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MetadataType'
        db.create_table('metadata_metadatatype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=48)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=48, null=True, blank=True)),
            ('default', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('lookup', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
        ))
        db.send_create_signal('metadata', ['MetadataType'])

        # Adding model 'MetadataSet'
        db.create_table('metadata_metadataset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=48)),
        ))
        db.send_create_signal('metadata', ['MetadataSet'])

        # Adding model 'MetadataSetItem'
        db.create_table('metadata_metadatasetitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('metadata_set', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['metadata.MetadataSet'])),
            ('metadata_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['metadata.MetadataType'])),
        ))
        db.send_create_signal('metadata', ['MetadataSetItem'])

        # Adding model 'DocumentMetadata'
        db.create_table('metadata_documentmetadata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('document', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documents.Document'])),
            ('metadata_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['metadata.MetadataType'])),
            ('value', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=255, blank=True)),
        ))
        db.send_create_signal('metadata', ['DocumentMetadata'])

        # Adding model 'DocumentTypeDefaults'
        db.create_table('metadata_documenttypedefaults', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('document_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documents.DocumentType'])),
        ))
        db.send_create_signal('metadata', ['DocumentTypeDefaults'])

        # Adding M2M table for field default_metadata_sets on 'DocumentTypeDefaults'
        db.create_table('metadata_documenttypedefaults_default_metadata_sets', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('documenttypedefaults', models.ForeignKey(orm['metadata.documenttypedefaults'], null=False)),
            ('metadataset', models.ForeignKey(orm['metadata.metadataset'], null=False))
        ))
        db.create_unique('metadata_documenttypedefaults_default_metadata_sets', ['documenttypedefaults_id', 'metadataset_id'])

        # Adding M2M table for field default_metadata on 'DocumentTypeDefaults'
        db.create_table('metadata_documenttypedefaults_default_metadata', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('documenttypedefaults', models.ForeignKey(orm['metadata.documenttypedefaults'], null=False)),
            ('metadatatype', models.ForeignKey(orm['metadata.metadatatype'], null=False))
        ))
        db.create_unique('metadata_documenttypedefaults_default_metadata', ['documenttypedefaults_id', 'metadatatype_id'])


    def backwards(self, orm):
        # Deleting model 'MetadataType'
        db.delete_table('metadata_metadatatype')

        # Deleting model 'MetadataSet'
        db.delete_table('metadata_metadataset')

        # Deleting model 'MetadataSetItem'
        db.delete_table('metadata_metadatasetitem')

        # Deleting model 'DocumentMetadata'
        db.delete_table('metadata_documentmetadata')

        # Deleting model 'DocumentTypeDefaults'
        db.delete_table('metadata_documenttypedefaults')

        # Removing M2M table for field default_metadata_sets on 'DocumentTypeDefaults'
        db.delete_table('metadata_documenttypedefaults_default_metadata_sets')

        # Removing M2M table for field default_metadata on 'DocumentTypeDefaults'
        db.delete_table('metadata_documenttypedefaults_default_metadata')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'comments.comment': {
            'Meta': {'ordering': "('submit_date',)", 'object_name': 'Comment', 'db_table': "'django_comments'"},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '3000'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type_set_for_comment'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_pk': ('django.db.models.fields.TextField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'submit_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'comment_comments'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'user_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'documents.document': {
            'Meta': {'ordering': "['-date_added']", 'object_name': 'Document'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'document_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['documents.DocumentType']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '48', 'blank': 'True'})
        },
        'documents.documenttype': {
            'Meta': {'ordering': "['name']", 'object_name': 'DocumentType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        },
        'metadata.documentmetadata': {
            'Meta': {'object_name': 'DocumentMetadata'},
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['documents.Document']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['metadata.MetadataType']"}),
            'value': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '256', 'blank': 'True'})
        },
        'metadata.documenttypedefaults': {
            'Meta': {'object_name': 'DocumentTypeDefaults'},
            'default_metadata': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['metadata.MetadataType']", 'symmetrical': 'False', 'blank': 'True'}),
            'default_metadata_sets': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['metadata.MetadataSet']", 'symmetrical': 'False', 'blank': 'True'}),
            'document_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['documents.DocumentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'metadata.metadataset': {
            'Meta': {'ordering': "('title',)", 'object_name': 'MetadataSet'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '48'})
        },
        'metadata.metadatasetitem': {
            'Meta': {'object_name': 'MetadataSetItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata_set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['metadata.MetadataSet']"}),
            'metadata_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['metadata.MetadataType']"})
        },
        'metadata.metadatatype': {
            'Meta': {'ordering': "('title',)", 'object_name': 'MetadataType'},
            'default': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lookup': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '48'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '48', 'null': 'True', 'blank': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"})
        }
    }

    complete_apps = ['metadata']
