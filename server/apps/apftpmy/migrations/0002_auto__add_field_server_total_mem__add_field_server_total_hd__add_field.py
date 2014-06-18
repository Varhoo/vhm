# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Server.total_mem'
        db.add_column(u'apftpmy_server', 'total_mem',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Server.total_hd'
        db.add_column(u'apftpmy_server', 'total_hd',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Server.last_checked'
        db.add_column(u'apftpmy_server', 'last_checked',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)

        # Adding field 'Server.global_ip'
        db.add_column(u'apftpmy_server', 'global_ip',
                      self.gf('django.db.models.fields.IPAddressField')(default='0.0.0.0', max_length=15),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Server.total_mem'
        db.delete_column(u'apftpmy_server', 'total_mem')

        # Deleting field 'Server.total_hd'
        db.delete_column(u'apftpmy_server', 'total_hd')

        # Deleting field 'Server.last_checked'
        db.delete_column(u'apftpmy_server', 'last_checked')

        # Deleting field 'Server.global_ip'
        db.delete_column(u'apftpmy_server', 'global_ip')


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
            'token': ('django.db.models.fields.CharField', [], {'default': "'has3$43+buo-9mjj&t5l+lsuvh%dazd!c!o8#^+b+lty+y_*2n'", 'max_length': '50'}),
            'uid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'apftpmy.customer': {
            'Meta': {'object_name': 'Customer'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'apftpmy.domain': {
            'Meta': {'object_name': 'Domain'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expirate': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modify': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'apftpmy.domainalias': {
            'Meta': {'object_name': 'DomainAlias'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['apftpmy.Project']"}),
            'site': ('django.db.models.fields.CharField', [], {'max_length': '126'})
        },
        u'apftpmy.ftpuser': {
            'Meta': {'object_name': 'Ftpuser', 'db_table': "'ftpusers'"},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['apftpmy.Account']"}),
            'gid': ('django.db.models.fields.IntegerField', [], {}),
            'homedir': ('django.db.models.fields.CharField', [], {'default': "'/var/www/'", 'max_length': '150'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'passwd': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'shell': ('django.db.models.fields.CharField', [], {'default': "'/bin/false'", 'max_length': '50'}),
            'uid': ('django.db.models.fields.IntegerField', [], {}),
            'userid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'apftpmy.invoice': {
            'Meta': {'object_name': 'Invoice'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['apftpmy.Account']"}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 6, 18, 0, 0)'}),
            'file': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'month': ('django.db.models.fields.IntegerField', [], {}),
            'price': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sale': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'size': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['apftpmy.Customer']"})
        },
        u'apftpmy.project': {
            'Meta': {'object_name': 'Project'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['apftpmy.Account']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 18, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_modify': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 18, 0, 0)', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '126'}),
            'site': ('django.db.models.fields.CharField', [], {'max_length': '126'})
        },
        u'apftpmy.projectproc': {
            'Meta': {'object_name': 'ProjectProc'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mode': ('django.db.models.fields.IntegerField', [], {}),
            'mode_params': ('django.db.models.fields.TextField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'power': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['apftpmy.ProjectSetting']"})
        },
        u'apftpmy.projectsetting': {
            'Meta': {'object_name': 'ProjectSetting', '_ormbases': [u'apftpmy.Project']},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'project_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['apftpmy.Project']", 'unique': 'True', 'primary_key': 'True'}),
            'repo_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'repo_url': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'repo_version': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        u'apftpmy.server': {
            'Meta': {'object_name': 'Server'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'global_ip': ('django.db.models.fields.IPAddressField', [], {'default': "'0.0.0.0'", 'max_length': '15'}),
            'hostname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_checked': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'os_type': ('django.db.models.fields.IntegerField', [], {}),
            'token': ('django.db.models.fields.CharField', [], {'default': "'t7r$y)f!u3v$loxos0a^$==y-)&^h!zn0lrfq(ofi3qtew*^k&'", 'max_length': '50'}),
            'total_hd': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_mem': ('django.db.models.fields.IntegerField', [], {'default': '0'})
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
        }
    }

    complete_apps = ['apftpmy']