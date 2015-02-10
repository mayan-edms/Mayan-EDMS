# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'SmartLinkCondition.foreign_document_data'
        db.alter_column(u'linking_smartlinkcondition', 'foreign_document_data', self.gf('django.db.models.fields.CharField')(max_length=128))

    def backwards(self, orm):

        # Changing field 'SmartLinkCondition.foreign_document_data'
        db.alter_column(u'linking_smartlinkcondition', 'foreign_document_data', self.gf('django.db.models.fields.CharField')(max_length=32))

    models = {
        u'documents.documenttype': {
            'Meta': {'ordering': "['name']", 'object_name': 'DocumentType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'ocr': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'linking.smartlink': {
            'Meta': {'object_name': 'SmartLink'},
            'document_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['documents.DocumentType']", 'symmetrical': 'False'}),
            'dynamic_title': ('django.db.models.fields.CharField', [], {'max_length': '96', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '96'})
        },
        u'linking.smartlinkcondition': {
            'Meta': {'object_name': 'SmartLinkCondition'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'expression': ('django.db.models.fields.TextField', [], {}),
            'foreign_document_data': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inclusion': ('django.db.models.fields.CharField', [], {'default': "u'&'", 'max_length': '16'}),
            'negated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'operator': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'smart_link': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linking.SmartLink']"})
        }
    }

    complete_apps = ['linking']
