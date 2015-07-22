# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ActionServer.msg_result'
        db.delete_column(u'xmlrpc_actionserver', 'msg_result')

        # Adding field 'ActionServer.role'
        db.add_column(u'xmlrpc_actionserver', 'role',
                      self.gf('django.db.models.fields.CharField')(
                          default='root', max_length=64),
                      keep_default=False)

        # Adding field 'ActionServer.result'
        db.add_column(u'xmlrpc_actionserver', 'result',
                      self.gf('django.db.models.fields.TextField')(
                          default='', blank=True),
                      keep_default=False)

    def backwards(self, orm):
        # Adding field 'ActionServer.msg_result'
        db.add_column(u'xmlrpc_actionserver', 'msg_result',
                      self.gf('django.db.models.fields.TextField')(
                          default='', blank=True),
                      keep_default=False)

        # Deleting field 'ActionServer.role'
        db.delete_column(u'xmlrpc_actionserver', 'role')

        # Deleting field 'ActionServer.result'
        db.delete_column(u'xmlrpc_actionserver', 'result')

    models = {
        u'apftpmy.account': {
            'Meta': {'object_name': 'Account'},
            'gid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'path': ('django.db.models.fields.CharField', [], {'default': "'/var/www/'", 'max_length': '64'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['apftpmy.Server']"}),
            'size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'token': ('django.db.models.fields.CharField', [], {'default': "'44b&eeg1_p0x*cve81py^+d8)$c094#g@l8thjx63fp^=ik#n0'", 'max_length': '50'}),
            'uid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'apftpmy.server': {
            'Meta': {'object_name': 'Server'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'hostname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'os_type': ('django.db.models.fields.IntegerField', [], {}),
            'token': ('django.db.models.fields.CharField', [], {'default': "'fin2$ip&re8=2z&=y+ilni_=avg=5hwd$+9a457t+pzw3fark#'", 'max_length': '50'})
        },
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'xmlrpc.action': {
            'Meta': {'object_name': 'Action'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['apftpmy.Account']"}),
            'command': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modify': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'xmlrpc.actionserver': {
            'Meta': {'object_name': 'ActionServer'},
            'command': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'exit_code': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modify': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'result': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'default': "'root'", 'max_length': '64'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['apftpmy.Server']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['xmlrpc']
