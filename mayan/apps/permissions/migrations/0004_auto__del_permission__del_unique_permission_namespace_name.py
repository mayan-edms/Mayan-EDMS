# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Removing unique constraint on 'Permission', fields ['namespace', 'name']
        db.delete_unique('permissions_permission', ['namespace', 'name'])

        # Deleting model 'Permission'
        db.delete_table('permissions_permission')


    def backwards(self, orm):
        
        # Adding model 'Permission'
        db.create_table('permissions_permission', (
            ('namespace', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=96)),
        ))
        db.send_create_signal('permissions', ['Permission'])

        # Adding unique constraint on 'Permission', fields ['namespace', 'name']
        db.create_unique('permissions_permission', ['namespace', 'name'])


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'permissions.permissionholder': {
            'Meta': {'object_name': 'PermissionHolder'},
            'holder_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'holder_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'permission_holder'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['permissions.StoredPermission']"})
        },
        'permissions.role': {
            'Meta': {'ordering': "('label',)", 'object_name': 'Role'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        'permissions.rolemember': {
            'Meta': {'object_name': 'RoleMember'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'member_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'role_member'", 'to': "orm['contenttypes.ContentType']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['permissions.Role']"})
        },
        'permissions.storedpermission': {
            'Meta': {'ordering': "('namespace',)", 'unique_together': "(('namespace', 'name'),)", 'object_name': 'StoredPermission'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'namespace': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['permissions']
