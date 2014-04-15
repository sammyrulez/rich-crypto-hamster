# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Currency'
        db.create_table(u'exchange_currency', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('base_value', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
        ))
        db.send_create_signal(u'exchange', ['Currency'])

        # Deleting field 'ExchangeRatio.currentRatio'
        db.delete_column(u'exchange_exchangeratio', 'currentRatio')

        # Adding field 'ExchangeRatio.ratio'
        db.add_column(u'exchange_exchangeratio', 'ratio',
                      self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=12, decimal_places=2),
                      keep_default=False)


        # Renaming column for 'ExchangeRatio.currency' to match new field type.
        db.rename_column(u'exchange_exchangeratio', 'currency', 'currency_id')
        # Changing field 'ExchangeRatio.currency'
        db.alter_column(u'exchange_exchangeratio', 'currency_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exchange.Currency']))
        # Adding index on 'ExchangeRatio', fields ['currency']
        db.create_index(u'exchange_exchangeratio', ['currency_id'])


    def backwards(self, orm):
        # Removing index on 'ExchangeRatio', fields ['currency']
        db.delete_index(u'exchange_exchangeratio', ['currency_id'])

        # Deleting model 'Currency'
        db.delete_table(u'exchange_currency')


        # User chose to not deal with backwards NULL issues for 'ExchangeRatio.currentRatio'
        raise RuntimeError("Cannot reverse this migration. 'ExchangeRatio.currentRatio' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ExchangeRatio.currentRatio'
        db.add_column(u'exchange_exchangeratio', 'currentRatio',
                      self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2),
                      keep_default=False)

        # Deleting field 'ExchangeRatio.ratio'
        db.delete_column(u'exchange_exchangeratio', 'ratio')


        # Renaming column for 'ExchangeRatio.currency' to match new field type.
        db.rename_column(u'exchange_exchangeratio', 'currency_id', 'currency')
        # Changing field 'ExchangeRatio.currency'
        db.alter_column(u'exchange_exchangeratio', 'currency', self.gf('django.db.models.fields.CharField')(max_length=3))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'exchange.balance': {
            'Meta': {'object_name': 'Balance'},
            'current_value': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'exchange.currency': {
            'Meta': {'object_name': 'Currency'},
            'base_value': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        u'exchange.exchangeratio': {
            'Meta': {'object_name': 'ExchangeRatio'},
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exchange.Currency']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ratio': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'})
        }
    }

    complete_apps = ['exchange']