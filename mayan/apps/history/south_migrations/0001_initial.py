# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'HistoryType'
        db.create_table(u'history_historytype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('namespace', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'history', ['HistoryType'])

        # Adding unique constraint on 'HistoryType', fields ['namespace', 'name']
        db.create_unique(u'history_historytype', ['namespace', 'name'])

        # Adding model 'History'
        db.create_table(u'history_history', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('history_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['history.HistoryType'])),
            ('dictionary', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'history', ['History'])

    def backwards(self, orm):
        # Removing unique constraint on 'HistoryType', fields ['namespace', 'name']
        db.delete_unique(u'history_historytype', ['namespace', 'name'])

        # Deleting model 'HistoryType'
        db.delete_table(u'history_historytype')

        # Deleting model 'History'
        db.delete_table(u'history_history')

    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'history.history': {
            'Meta': {'ordering': "('-datetime',)", 'object_name': 'History'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'dictionary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'history_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['history.HistoryType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'history.historytype': {
            'Meta': {'ordering': "('namespace', 'name')", 'unique_together': "(('namespace', 'name'),)", 'object_name': 'HistoryType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'namespace': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['history']
