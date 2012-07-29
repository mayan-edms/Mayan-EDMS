# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SmartLink'
        db.create_table('linking_smartlink', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=96)),
            ('dynamic_title', self.gf('django.db.models.fields.CharField')(max_length=96, blank=True)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('linking', ['SmartLink'])

        # Adding model 'SmartLinkCondition'
        db.create_table('linking_smartlinkcondition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('smart_link', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linking.SmartLink'])),
            ('inclusion', self.gf('django.db.models.fields.CharField')(default=u'&', max_length=16)),
            ('foreign_document_data', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('operator', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('expression', self.gf('django.db.models.fields.TextField')()),
            ('negated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('linking', ['SmartLinkCondition'])


    def backwards(self, orm):
        # Deleting model 'SmartLink'
        db.delete_table('linking_smartlink')

        # Deleting model 'SmartLinkCondition'
        db.delete_table('linking_smartlinkcondition')


    models = {
        'linking.smartlink': {
            'Meta': {'object_name': 'SmartLink'},
            'dynamic_title': ('django.db.models.fields.CharField', [], {'max_length': '96', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '96'})
        },
        'linking.smartlinkcondition': {
            'Meta': {'object_name': 'SmartLinkCondition'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'expression': ('django.db.models.fields.TextField', [], {}),
            'foreign_document_data': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inclusion': ('django.db.models.fields.CharField', [], {'default': "u'&'", 'max_length': '16'}),
            'negated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'operator': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'smart_link': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['linking.SmartLink']"})
        }
    }

    complete_apps = ['linking']
