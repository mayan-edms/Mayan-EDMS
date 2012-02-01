# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'DocumentRenameCount'
        db.delete_table('document_indexing_documentrenamecount')

        # Deleting model 'IndexInstance'
        db.delete_table('document_indexing_indexinstance')

        # Removing M2M table for field documents on 'IndexInstance'
        db.delete_table('document_indexing_indexinstance_documents')

        # Deleting model 'Index'
        db.delete_table('document_indexing_index')


    def backwards(self, orm):
        
        # Adding model 'DocumentRenameCount'
        db.create_table('document_indexing_documentrenamecount', (
            ('suffix', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True)),
            ('index_instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['document_indexing.IndexInstance'])),
            ('document', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documents.Document'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('document_indexing', ['DocumentRenameCount'])

        # Adding model 'IndexInstance'
        db.create_table('document_indexing_indexinstance', (
            ('index', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['document_indexing.Index'])),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(related_name='index_meta_instance', null=True, to=orm['document_indexing.IndexInstance'], blank=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('document_indexing', ['IndexInstance'])

        # Adding M2M table for field documents on 'IndexInstance'
        db.create_table('document_indexing_indexinstance_documents', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('indexinstance', models.ForeignKey(orm['document_indexing.indexinstance'], null=False)),
            ('document', models.ForeignKey(orm['documents.document'], null=False))
        ))
        db.create_unique('document_indexing_indexinstance_documents', ['indexinstance_id', 'document_id'])

        # Adding model 'Index'
        db.create_table('document_indexing_index', (
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(related_name='index_meta_class', null=True, to=orm['document_indexing.Index'], blank=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('link_documents', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('expression', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('document_indexing', ['Index'])


    models = {
        
    }

    complete_apps = ['document_indexing']
