# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Worker.name'
        db.delete_column('job_processor_worker', 'name')

        # Adding field 'Worker.pid'
        db.add_column('job_processor_worker', 'pid',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1, max_length=255),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Worker.name'
        raise RuntimeError("Cannot reverse this migration. 'Worker.name' and its values cannot be restored.")
        # Deleting field 'Worker.pid'
        db.delete_column('job_processor_worker', 'pid')


    models = {
        'clustering.node': {
            'Meta': {'object_name': 'Node'},
            'cpuload': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'blank': 'True'}),
            'heartbeat': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 7, 30, 0, 0)', 'blank': 'True'}),
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memory_usage': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'blank': 'True'})
        },
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
        'job_processor.worker': {
            'Meta': {'ordering': "('creation_datetime',)", 'object_name': 'Worker'},
            'creation_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 7, 30, 0, 0)'}),
            'heartbeat': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 7, 30, 0, 0)', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_queue_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['job_processor.JobQueueItem']"}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clustering.Node']"}),
            'pid': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '255'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'r'", 'max_length': '4'})
        }
    }

    complete_apps = ['job_processor']