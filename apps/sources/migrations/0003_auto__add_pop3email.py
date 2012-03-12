# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'POP3Email'
        db.create_table('sources_pop3email', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('whitelist', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('blacklist', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('uncompress', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('ssl', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('port', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('delete', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('sources', ['POP3Email'])


    def backwards(self, orm):
        
        # Deleting model 'POP3Email'
        db.delete_table('sources_pop3email')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'sources.outofprocess': {
            'Meta': {'ordering': "('title',)", 'object_name': 'OutOfProcess'},
            'blacklist': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'whitelist': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'sources.pop3email': {
            'Meta': {'ordering': "('title',)", 'object_name': 'POP3Email'},
            'blacklist': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'delete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'}),
            'ssl': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'uncompress': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'whitelist': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'sources.sourcetransformation': {
            'Meta': {'ordering': "('order',)", 'object_name': 'SourceTransformation'},
            'arguments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'transformation': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'sources.stagingfolder': {
            'Meta': {'ordering': "('title',)", 'object_name': 'StagingFolder'},
            'blacklist': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'delete_after_upload': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'folder_path': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '24', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'preview_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'preview_width': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'uncompress': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'whitelist': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'sources.watchfolder': {
            'Meta': {'ordering': "('title',)", 'object_name': 'WatchFolder'},
            'blacklist': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'delete_after_upload': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'folder_path': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'uncompress': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'whitelist': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'sources.webform': {
            'Meta': {'ordering': "('title',)", 'object_name': 'WebForm'},
            'blacklist': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '24', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'uncompress': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'whitelist': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['sources']
