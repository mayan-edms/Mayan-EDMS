# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Queue'
        db.create_table('queue_manager_queue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('unique_names', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('queue_manager', ['Queue'])

        # Adding model 'QueueItem'
        db.create_table('queue_manager_queueitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('queue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['queue_manager.Queue'])),
            ('creation_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('unique_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('data', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('queue_manager', ['QueueItem'])


    def backwards(self, orm):
        # Deleting model 'Queue'
        db.delete_table('queue_manager_queue')

        # Deleting model 'QueueItem'
        db.delete_table('queue_manager_queueitem')


    models = {
        'queue_manager.queue': {
            'Meta': {'object_name': 'Queue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'unique_names': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'queue_manager.queueitem': {
            'Meta': {'object_name': 'QueueItem'},
            'creation_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'data': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'queue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['queue_manager.Queue']"}),
            'unique_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32', 'blank': 'True'})
        }
    }

    complete_apps = ['queue_manager']