# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'DocumentType'
        db.create_table('documents_documenttype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('documents', ['DocumentType'])

        # Adding model 'Document'
        db.create_table('documents_document', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('document_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documents.DocumentType'])),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default=u'9637cae5-b772-46b5-84ee-bca22925d66f', max_length=48, blank=True)),
            ('file_mimetype', self.gf('django.db.models.fields.CharField')(default='', max_length=64)),
            ('file_mime_encoding', self.gf('django.db.models.fields.CharField')(default='', max_length=64)),
            ('file_filename', self.gf('django.db.models.fields.CharField')(default='', max_length=255, db_index=True)),
            ('file_extension', self.gf('django.db.models.fields.CharField')(default='', max_length=16, db_index=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('checksum', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(db_index=True, null=True, blank=True)),
        ))
        db.send_create_signal('documents', ['Document'])

        # Adding model 'MetadataType'
        db.create_table('documents_metadatatype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=48)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=48, null=True, blank=True)),
            ('default', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('lookup', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
        ))
        db.send_create_signal('documents', ['MetadataType'])

        # Adding model 'DocumentTypeMetadataType'
        db.create_table('documents_documenttypemetadatatype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('document_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documents.DocumentType'])),
            ('metadata_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documents.MetadataType'])),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('documents', ['DocumentTypeMetadataType'])

        # Adding model 'MetadataIndex'
        db.create_table('documents_metadataindex', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('document_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documents.DocumentType'])),
            ('expression', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('documents', ['MetadataIndex'])

        # Adding model 'DocumentMetadata'
        db.create_table('documents_documentmetadata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('document', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documents.Document'])),
            ('metadata_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documents.MetadataType'])),
            ('value', self.gf('django.db.models.fields.TextField')(db_index=True, null=True, blank=True)),
        ))
        db.send_create_signal('documents', ['DocumentMetadata'])

        # Adding model 'DocumentTypeFilename'
        db.create_table('documents_documenttypefilename', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('document_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documents.DocumentType'])),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('documents', ['DocumentTypeFilename'])

        # Adding model 'DocumentPage'
        db.create_table('documents_documentpage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('document', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documents.Document'])),
            ('content', self.gf('django.db.models.fields.TextField')(db_index=True, null=True, blank=True)),
            ('page_label', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('page_number', self.gf('django.db.models.fields.PositiveIntegerField')(default=1, db_index=True)),
        ))
        db.send_create_signal('documents', ['DocumentPage'])

        # Adding model 'MetadataGroup'
        db.create_table('documents_metadatagroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('documents', ['MetadataGroup'])

        # Adding M2M table for field document_type on 'MetadataGroup'
        db.create_table('documents_metadatagroup_document_type', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('metadatagroup', models.ForeignKey(orm['documents.metadatagroup'], null=False)),
            ('documenttype', models.ForeignKey(orm['documents.documenttype'], null=False))
        ))
        db.create_unique('documents_metadatagroup_document_type', ['metadatagroup_id', 'documenttype_id'])

        # Adding model 'MetadataGroupItem'
        db.create_table('documents_metadatagroupitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('metadata_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documents.MetadataGroup'])),
            ('inclusion', self.gf('django.db.models.fields.CharField')(default=u'&', max_length=16)),
            ('metadata_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documents.MetadataType'])),
            ('operator', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('expression', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('negated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('documents', ['MetadataGroupItem'])

        # Adding model 'DocumentPageTransformation'
        db.create_table('documents_documentpagetransformation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('document_page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documents.DocumentPage'])),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True, db_index=True, blank=True)),
            ('transformation', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('arguments', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('documents', ['DocumentPageTransformation'])

        # Adding model 'RecentDocument'
        db.create_table('documents_recentdocument', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('document', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documents.Document'])),
            ('datetime_accessed', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
        ))
        db.send_create_signal('documents', ['RecentDocument'])


    def backwards(self, orm):
        
        # Deleting model 'DocumentType'
        db.delete_table('documents_documenttype')

        # Deleting model 'Document'
        db.delete_table('documents_document')

        # Deleting model 'MetadataType'
        db.delete_table('documents_metadatatype')

        # Deleting model 'DocumentTypeMetadataType'
        db.delete_table('documents_documenttypemetadatatype')

        # Deleting model 'MetadataIndex'
        db.delete_table('documents_metadataindex')

        # Deleting model 'DocumentMetadata'
        db.delete_table('documents_documentmetadata')

        # Deleting model 'DocumentTypeFilename'
        db.delete_table('documents_documenttypefilename')

        # Deleting model 'DocumentPage'
        db.delete_table('documents_documentpage')

        # Deleting model 'MetadataGroup'
        db.delete_table('documents_metadatagroup')

        # Removing M2M table for field document_type on 'MetadataGroup'
        db.delete_table('documents_metadatagroup_document_type')

        # Deleting model 'MetadataGroupItem'
        db.delete_table('documents_metadatagroupitem')

        # Deleting model 'DocumentPageTransformation'
        db.delete_table('documents_documentpagetransformation')

        # Deleting model 'RecentDocument'
        db.delete_table('documents_recentdocument')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'comments.comment': {
            'Meta': {'ordering': "('submit_date',)", 'object_name': 'Comment', 'db_table': "'django_comments'"},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '3000'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type_set_for_comment'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_pk': ('django.db.models.fields.TextField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'submit_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'comment_comments'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'user_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'documents.document': {
            'Meta': {'ordering': "['-date_added']", 'object_name': 'Document'},
            'checksum': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'document_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['documents.DocumentType']"}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'file_extension': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '16', 'db_index': 'True'}),
            'file_filename': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'db_index': 'True'}),
            'file_mime_encoding': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64'}),
            'file_mimetype': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "u'9637cae5-b772-46b5-84ee-bca22925d66f'", 'max_length': '48', 'blank': 'True'})
        },
        'documents.documentmetadata': {
            'Meta': {'object_name': 'DocumentMetadata'},
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['documents.Document']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['documents.MetadataType']"}),
            'value': ('django.db.models.fields.TextField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'})
        },
        'documents.documentpage': {
            'Meta': {'ordering': "['page_number']", 'object_name': 'DocumentPage'},
            'content': ('django.db.models.fields.TextField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['documents.Document']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page_label': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'page_number': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'db_index': 'True'})
        },
        'documents.documentpagetransformation': {
            'Meta': {'ordering': "('order',)", 'object_name': 'DocumentPageTransformation'},
            'arguments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'document_page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['documents.DocumentPage']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'transformation': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'documents.documenttype': {
            'Meta': {'object_name': 'DocumentType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'documents.documenttypefilename': {
            'Meta': {'ordering': "['filename']", 'object_name': 'DocumentTypeFilename'},
            'document_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['documents.DocumentType']"}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'documents.documenttypemetadatatype': {
            'Meta': {'object_name': 'DocumentTypeMetadataType'},
            'document_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['documents.DocumentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['documents.MetadataType']"}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'documents.metadatagroup': {
            'Meta': {'object_name': 'MetadataGroup'},
            'document_type': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['documents.DocumentType']", 'null': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'documents.metadatagroupitem': {
            'Meta': {'object_name': 'MetadataGroupItem'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'expression': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inclusion': ('django.db.models.fields.CharField', [], {'default': "u'&'", 'max_length': '16'}),
            'metadata_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['documents.MetadataGroup']"}),
            'metadata_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['documents.MetadataType']"}),
            'negated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'operator': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'documents.metadataindex': {
            'Meta': {'object_name': 'MetadataIndex'},
            'document_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['documents.DocumentType']"}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'expression': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'documents.metadatatype': {
            'Meta': {'object_name': 'MetadataType'},
            'default': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lookup': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '48', 'null': 'True', 'blank': 'True'})
        },
        'documents.recentdocument': {
            'Meta': {'ordering': "('-datetime_accessed',)", 'object_name': 'RecentDocument'},
            'datetime_accessed': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['documents.Document']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"})
        }
    }

    complete_apps = ['documents']
