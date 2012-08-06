# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'JobQueue.priority'
        db.add_column('job_processor_jobqueue', 'priority',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'JobQueue.priority'
        db.delete_column('job_processor_jobqueue', 'priority')


    models = {
        'clustering.node': {
            'Meta': {'object_name': 'Node'},
            'cpuload': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'heartbeat': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 5, 0, 0)', 'blank': 'True'}),
            'hostname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memory_usage': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'d'", 'max_length': '4'})
        },
        'job_processor.jobprocessingconfig': {
            'Meta': {'object_name': 'JobProcessingConfig'},
            'dead_job_removal_interval': ('django.db.models.fields.PositiveIntegerField', [], {'default': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_queue_poll_interval': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2'}),
            'lock_id': ('django.db.models.fields.CharField', [], {'default': '1', 'unique': 'True', 'max_length': '1'})
        },
        'job_processor.jobqueue': {
            'Meta': {'ordering': "('priority',)", 'object_name': 'JobQueue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'r'", 'max_length': '4'}),
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
        'job_processor.worker': {
            'Meta': {'ordering': "('creation_datetime',)", 'unique_together': "(('node', 'pid'),)", 'object_name': 'Worker'},
            'creation_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 5, 0, 0)'}),
            'heartbeat': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 5, 0, 0)', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_queue_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['job_processor.JobQueueItem']", 'null': 'True', 'blank': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clustering.Node']"}),
            'pid': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '255'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'r'", 'max_length': '4'})
        }
    }

    complete_apps = ['job_processor']