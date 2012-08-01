# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Node'
        db.create_table('job_processor_node', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hostname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('cpuload', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True)),
            ('heartbeat', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 7, 30, 0, 0), blank=True)),
            ('memory_usage', self.gf('django.db.models.fields.FloatField')(blank=True)),
        ))
        db.send_create_signal('job_processor', ['Node'])

        # Adding model 'JobQueue'
        db.create_table('job_processor_jobqueue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('unique_jobs', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('job_processor', ['JobQueue'])

        # Adding model 'JobQueueItem'
        db.create_table('job_processor_jobqueueitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('job_queue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['job_processor.JobQueue'])),
            ('creation_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('unique_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64, blank=True)),
            ('job_type', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('kwargs', self.gf('django.db.models.fields.TextField')()),
            ('state', self.gf('django.db.models.fields.CharField')(default='p', max_length=4)),
            ('result', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('job_processor', ['JobQueueItem'])

        # Adding model 'Worker'
        db.create_table('job_processor_worker', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['job_processor.Node'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('creation_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 7, 30, 0, 0))),
            ('heartbeat', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 7, 30, 0, 0), blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(default='r', max_length=4)),
        ))
        db.send_create_signal('job_processor', ['Worker'])


    def backwards(self, orm):
        # Deleting model 'Node'
        db.delete_table('job_processor_node')

        # Deleting model 'JobQueue'
        db.delete_table('job_processor_jobqueue')

        # Deleting model 'JobQueueItem'
        db.delete_table('job_processor_jobqueueitem')

        # Deleting model 'Worker'
        db.delete_table('job_processor_worker')


    models = {
        'job_processor.jobqueue': {
            'Meta': {'object_name': 'JobQueue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'unique_jobs': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'job_processor.jobqueueitem': {
            'Meta': {'ordering': "('creation_datetime',)", 'object_name': 'JobQueueItem'},
            'creation_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_queue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['job_processor.JobQueue']"}),
            'job_type': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'kwargs': ('django.db.models.fields.TextField', [], {}),
            'result': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'p'", 'max_length': '4'}),
            'unique_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'blank': 'True'})
        },
        'job_processor.node': {
            'Meta': {'object_name': 'Node'},
            'cpuload': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'heartbeat': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 7, 30, 0, 0)', 'blank': 'True'}),
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memory_usage': ('django.db.models.fields.FloatField', [], {'blank': 'True'})
        },
        'job_processor.worker': {
            'Meta': {'ordering': "('creation_datetime',)", 'object_name': 'Worker'},
            'creation_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 7, 30, 0, 0)'}),
            'heartbeat': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 7, 30, 0, 0)', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['job_processor.Node']"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'r'", 'max_length': '4'})
        }
    }

    complete_apps = ['job_processor']