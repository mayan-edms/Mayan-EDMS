# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'IntervalBaseModel.document_type'
        db.delete_column(u'sources_intervalbasemodel', 'document_type_id')

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'IntervalBaseModel.document_type'
        raise RuntimeError("Cannot reverse this migration. 'IntervalBaseModel.document_type' and its values cannot be restored.")

        # The following code is provided here to aid in writing a correct migration        # Adding field 'IntervalBaseModel.document_type'
        db.add_column(u'sources_intervalbasemodel', 'document_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documents.DocumentType']),
                      keep_default=False)

    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sources.emailbasemodel': {
            'Meta': {'ordering': "('title',)", 'object_name': 'EmailBaseModel', '_ormbases': [u'sources.IntervalBaseModel']},
            'host': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'intervalbasemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['sources.IntervalBaseModel']", 'unique': 'True', 'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '96'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ssl': ('django.db.models.fields.BooleanField', [], {}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '96'})
        },
        u'sources.imapemail': {
            'Meta': {'ordering': "('title',)", 'object_name': 'IMAPEmail', '_ormbases': [u'sources.EmailBaseModel']},
            u'emailbasemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['sources.EmailBaseModel']", 'unique': 'True', 'primary_key': 'True'}),
            'mailbox': ('django.db.models.fields.CharField', [], {'default': "'INBOX'", 'max_length': '64'})
        },
        u'sources.interactivesource': {
            'Meta': {'ordering': "('title',)", 'object_name': 'InteractiveSource', '_ormbases': [u'sources.Source']},
            u'source_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['sources.Source']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'sources.intervalbasemodel': {
            'Meta': {'ordering': "('title',)", 'object_name': 'IntervalBaseModel', '_ormbases': [u'sources.OutOfProcessSource']},
            'interval': ('django.db.models.fields.PositiveIntegerField', [], {'default': '60'}),
            u'outofprocesssource_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['sources.OutOfProcessSource']", 'unique': 'True', 'primary_key': 'True'}),
            'uncompress': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'sources.outofprocesssource': {
            'Meta': {'ordering': "('title',)", 'object_name': 'OutOfProcessSource', '_ormbases': [u'sources.Source']},
            u'source_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['sources.Source']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'sources.pop3email': {
            'Meta': {'ordering': "('title',)", 'object_name': 'POP3Email', '_ormbases': [u'sources.EmailBaseModel']},
            u'emailbasemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['sources.EmailBaseModel']", 'unique': 'True', 'primary_key': 'True'}),
            'timeout': ('django.db.models.fields.PositiveIntegerField', [], {'default': '60'})
        },
        u'sources.source': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Source'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'sources.sourcetransformation': {
            'Meta': {'ordering': "('order',)", 'object_name': 'SourceTransformation'},
            'arguments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'transformation': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'sources.stagingfoldersource': {
            'Meta': {'ordering': "('title',)", 'object_name': 'StagingFolderSource', '_ormbases': [u'sources.InteractiveSource']},
            'delete_after_upload': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'folder_path': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'interactivesource_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['sources.InteractiveSource']", 'unique': 'True', 'primary_key': 'True'}),
            'preview_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'preview_width': ('django.db.models.fields.IntegerField', [], {}),
            'uncompress': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'sources.watchfoldersource': {
            'Meta': {'ordering': "('title',)", 'object_name': 'WatchFolderSource', '_ormbases': [u'sources.IntervalBaseModel']},
            'delete_after_upload': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'folder_path': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'intervalbasemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['sources.IntervalBaseModel']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'sources.webformsource': {
            'Meta': {'ordering': "('title',)", 'object_name': 'WebFormSource', '_ormbases': [u'sources.InteractiveSource']},
            u'interactivesource_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['sources.InteractiveSource']", 'unique': 'True', 'primary_key': 'True'}),
            'uncompress': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        }
    }

    complete_apps = ['sources']
