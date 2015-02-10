# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    depends_on = (
        ('events', '0002_migrate_history_data'),
    )

    def forwards(self, orm):
        # Removing unique constraint on 'HistoryType', fields ['namespace', 'name']
        db.delete_unique(u'history_historytype', ['namespace', 'name'])

        # Deleting model 'History'
        db.delete_table(u'history_history')

        # Deleting model 'HistoryType'
        db.delete_table(u'history_historytype')

    def backwards(self, orm):
        # Adding model 'History'
        db.create_table(u'history_history', (
            ('history_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['history.HistoryType'])),
            ('dictionary', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'history', ['History'])

        # Adding model 'HistoryType'
        db.create_table(u'history_historytype', (
            ('namespace', self.gf('django.db.models.fields.CharField')(max_length=64)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'history', ['HistoryType'])

        # Adding unique constraint on 'HistoryType', fields ['namespace', 'name']
        db.create_unique(u'history_historytype', ['namespace', 'name'])

    models = {}

    complete_apps = ['history']
