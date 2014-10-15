# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DocumentTypeStateCollection'
        db.create_table(u'states_documenttypestatecollection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('document_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='state_collections', to=orm['documents.DocumentType'])),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'states', ['DocumentTypeStateCollection'])

        # Adding model 'State'
        db.create_table(u'states_state', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('document_type_state_collection', self.gf('django.db.models.fields.related.ForeignKey')(related_name='states', to=orm['states.DocumentTypeStateCollection'])),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('initial', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'states', ['State'])

        # Adding model 'StateTransition'
        db.create_table(u'states_statetransition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source_state_template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['states.State'])),
            ('destination_state_template', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transitions', to=orm['states.State'])),
        ))
        db.send_create_signal(u'states', ['StateTransition'])

        # Adding model 'DocumentStateLog'
        db.create_table(u'states_documentstatelog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('document', self.gf('django.db.models.fields.related.ForeignKey')(related_name='states_log', to=orm['documents.Document'])),
            ('document_type_state_collection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['states.DocumentTypeStateCollection'])),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['states.State'])),
        ))
        db.send_create_signal(u'states', ['DocumentStateLog'])

        # Adding unique constraint on 'DocumentStateLog', fields ['document', 'document_type_state_collection']
        db.create_unique(u'states_documentstatelog', ['document_id', 'document_type_state_collection_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'DocumentStateLog', fields ['document', 'document_type_state_collection']
        db.delete_unique(u'states_documentstatelog', ['document_id', 'document_type_state_collection_id'])

        # Deleting model 'DocumentTypeStateCollection'
        db.delete_table(u'states_documenttypestatecollection')

        # Deleting model 'State'
        db.delete_table(u'states_state')

        # Deleting model 'StateTransition'
        db.delete_table(u'states_statetransition')

        # Deleting model 'DocumentStateLog'
        db.delete_table(u'states_documentstatelog')


    models = {
        u'documents.document': {
            'Meta': {'ordering': "['-date_added']", 'object_name': 'Document'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'document_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'documents'", 'null': 'True', 'to': u"orm['documents.DocumentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '48', 'blank': 'True'})
        },
        u'documents.documenttype': {
            'Meta': {'ordering': "['name']", 'object_name': 'DocumentType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        },
        u'states.documentstatelog': {
            'Meta': {'unique_together': "(('document', 'document_type_state_collection'),)", 'object_name': 'DocumentStateLog'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'states_log'", 'to': u"orm['documents.Document']"}),
            'document_type_state_collection': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['states.DocumentTypeStateCollection']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['states.State']"})
        },
        u'states.documenttypestatecollection': {
            'Meta': {'object_name': 'DocumentTypeStateCollection'},
            'document_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'state_collections'", 'to': u"orm['documents.DocumentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'states.state': {
            'Meta': {'object_name': 'State'},
            'document_type_state_collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'states'", 'to': u"orm['states.DocumentTypeStateCollection']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'states.statetransition': {
            'Meta': {'object_name': 'StateTransition'},
            'destination_state_template': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transitions'", 'to': u"orm['states.State']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source_state_template': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['states.State']"})
        }
    }

    complete_apps = ['states']