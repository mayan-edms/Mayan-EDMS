# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'StagingFolder'
        db.delete_table(u'sources_stagingfolder')

        # Deleting model 'WebForm'
        db.delete_table(u'sources_webform')

        # Deleting model 'WatchFolder'
        db.delete_table(u'sources_watchfolder')

        # Deleting model 'OutOfProcess'
        db.delete_table(u'sources_outofprocess')

        # Adding model 'Source'
        db.create_table(u'sources_source', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('whitelist', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('blacklist', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'sources', ['Source'])

        # Adding model 'InteractiveSource'
        db.create_table(u'sources_interactivesource', (
            (u'source_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sources.Source'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'sources', ['InteractiveSource'])

        # Adding model 'WatchFolderSource'
        db.create_table(u'sources_watchfoldersource', (
            (u'outofprocesssource_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sources.OutOfProcessSource'], unique=True, primary_key=True)),
            ('folder_path', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('uncompress', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('delete_after_upload', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('interval', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'sources', ['WatchFolderSource'])

        # Adding model 'WebFormSource'
        db.create_table(u'sources_webformsource', (
            (u'interactivesource_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sources.InteractiveSource'], unique=True, primary_key=True)),
            ('uncompress', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'sources', ['WebFormSource'])

        # Adding model 'OutOfProcessSource'
        db.create_table(u'sources_outofprocesssource', (
            (u'source_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sources.Source'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'sources', ['OutOfProcessSource'])

        # Adding model 'StagingFolderSource'
        db.create_table(u'sources_stagingfoldersource', (
            (u'interactivesource_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sources.InteractiveSource'], unique=True, primary_key=True)),
            ('folder_path', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('preview_width', self.gf('django.db.models.fields.IntegerField')()),
            ('preview_height', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('uncompress', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('delete_after_upload', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'sources', ['StagingFolderSource'])

    def backwards(self, orm):
        # Adding model 'StagingFolder'
        db.create_table(u'sources_stagingfolder', (
            ('folder_path', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('uncompress', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('delete_after_upload', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('whitelist', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('preview_height', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('blacklist', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('preview_width', self.gf('django.db.models.fields.IntegerField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'sources', ['StagingFolder'])

        # Adding model 'WebForm'
        db.create_table(u'sources_webform', (
            ('uncompress', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('whitelist', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('blacklist', self.gf('django.db.models.fields.TextField')(blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'sources', ['WebForm'])

        # Adding model 'WatchFolder'
        db.create_table(u'sources_watchfolder', (
            ('blacklist', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('folder_path', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('delete_after_upload', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('whitelist', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('interval', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uncompress', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'sources', ['WatchFolder'])

        # Adding model 'OutOfProcess'
        db.create_table(u'sources_outofprocess', (
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('whitelist', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('blacklist', self.gf('django.db.models.fields.TextField')(blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'sources', ['OutOfProcess'])

        # Deleting model 'Source'
        db.delete_table(u'sources_source')

        # Deleting model 'InteractiveSource'
        db.delete_table(u'sources_interactivesource')

        # Deleting model 'WatchFolderSource'
        db.delete_table(u'sources_watchfoldersource')

        # Deleting model 'WebFormSource'
        db.delete_table(u'sources_webformsource')

        # Deleting model 'OutOfProcessSource'
        db.delete_table(u'sources_outofprocesssource')

        # Deleting model 'StagingFolderSource'
        db.delete_table(u'sources_stagingfoldersource')

    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sources.interactivesource': {
            'Meta': {'ordering': "('title',)", 'object_name': 'InteractiveSource', '_ormbases': [u'sources.Source']},
            u'source_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['sources.Source']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'sources.outofprocesssource': {
            'Meta': {'ordering': "('title',)", 'object_name': 'OutOfProcessSource', '_ormbases': [u'sources.Source']},
            u'source_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['sources.Source']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'sources.source': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Source'},
            'blacklist': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'whitelist': ('django.db.models.fields.TextField', [], {'blank': 'True'})
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
            'Meta': {'ordering': "('title',)", 'object_name': 'WatchFolderSource', '_ormbases': [u'sources.OutOfProcessSource']},
            'delete_after_upload': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'folder_path': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'interval': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'outofprocesssource_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['sources.OutOfProcessSource']", 'unique': 'True', 'primary_key': 'True'}),
            'uncompress': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'sources.webformsource': {
            'Meta': {'ordering': "('title',)", 'object_name': 'WebFormSource', '_ormbases': [u'sources.InteractiveSource']},
            u'interactivesource_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['sources.InteractiveSource']", 'unique': 'True', 'primary_key': 'True'}),
            'uncompress': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        }
    }

    complete_apps = ['sources']
