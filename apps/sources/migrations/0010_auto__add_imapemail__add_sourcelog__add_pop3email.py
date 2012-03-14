# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ImapEmail'
        db.create_table('sources_imapemail', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('whitelist', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('blacklist', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('interval', self.gf('django.db.models.fields.PositiveIntegerField')(default=900)),
            ('document_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documents.DocumentType'], null=True, blank=True)),
            ('uncompress', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('ssl', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('port', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('mailbox', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
        ))
        db.send_create_signal('sources', ['ImapEmail'])

        # Adding model 'SourceLog'
        db.create_table('sources_sourcelog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('creation_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('status', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('sources', ['SourceLog'])

        # Adding model 'POP3Email'
        db.create_table('sources_pop3email', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('whitelist', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('blacklist', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('interval', self.gf('django.db.models.fields.PositiveIntegerField')(default=900)),
            ('document_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documents.DocumentType'], null=True, blank=True)),
            ('uncompress', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('ssl', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('port', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('sources', ['POP3Email'])


    def backwards(self, orm):
        
        # Deleting model 'ImapEmail'
        db.delete_table('sources_imapemail')

        # Deleting model 'SourceLog'
        db.delete_table('sources_sourcelog')

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
        'documents.documenttype': {
            'Meta': {'ordering': "['name']", 'object_name': 'DocumentType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'sources.imapemail': {
            'Meta': {'ordering': "('title',)", 'object_name': 'ImapEmail'},
            'blacklist': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'document_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['documents.DocumentType']", 'null': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.PositiveIntegerField', [], {'default': '900'}),
            'mailbox': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ssl': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'uncompress': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'whitelist': ('django.db.models.fields.TextField', [], {'blank': 'True'})
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
            'document_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['documents.DocumentType']", 'null': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.PositiveIntegerField', [], {'default': '900'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ssl': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'uncompress': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'whitelist': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'sources.sourcelog': {
            'Meta': {'ordering': "('creation_datetime',)", 'object_name': 'SourceLog'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'creation_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'status': ('django.db.models.fields.TextField', [], {})
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
