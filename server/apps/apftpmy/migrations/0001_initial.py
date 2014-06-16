# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Domain'
        db.create_table(u'apftpmy_domain', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('expirate', self.gf('django.db.models.fields.DateField')(default=datetime.datetime.now, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('last_modify', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'apftpmy', ['Domain'])

        # Adding model 'Server'
        db.create_table(u'apftpmy_server', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hostname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('os_type', self.gf('django.db.models.fields.IntegerField')()),
            ('token', self.gf('django.db.models.fields.CharField')(default='y+dcgca)u$@ff90^-u!e)_#x@3mn*ce1*@*d35q2xk!bu5tk&@', max_length=50)),
        ))
        db.send_create_signal(u'apftpmy', ['Server'])

        # Adding model 'Account'
        db.create_table(u'apftpmy_account', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('server', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apftpmy.Server'])),
            ('name', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=64)),
            ('path', self.gf('django.db.models.fields.CharField')(default='/var/www/', max_length=64)),
            ('size', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('token', self.gf('django.db.models.fields.CharField')(default='v0vl24^mf#4w@_u6v&shsmmc-clcqipvx!^1in4eoc7n9@gc(9', max_length=50)),
            ('user', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('uid', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('gid', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'apftpmy', ['Account'])

        # Adding model 'Project'
        db.create_table(u'apftpmy_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apftpmy.Account'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('site', self.gf('django.db.models.fields.CharField')(max_length=126)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=126)),
            ('is_enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 6, 16, 0, 0))),
            ('last_modify', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 6, 16, 0, 0), blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'apftpmy', ['Project'])

        # Adding model 'ProjectSetting'
        db.create_table(u'apftpmy_projectsetting', (
            (u'project_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['apftpmy.Project'], unique=True, primary_key=True)),
            ('repo_type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('repo_url', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('repo_version', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'apftpmy', ['ProjectSetting'])

        # Adding model 'ProjectProc'
        db.create_table(u'apftpmy_projectproc', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apftpmy.ProjectSetting'])),
            ('power', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('mode', self.gf('django.db.models.fields.IntegerField')()),
            ('mode_params', self.gf('django.db.models.fields.TextField')(max_length=256, null=True, blank=True)),
        ))
        db.send_create_signal(u'apftpmy', ['ProjectProc'])

        # Adding model 'DomainAlias'
        db.create_table(u'apftpmy_domainalias', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.CharField')(max_length=126)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apftpmy.Project'])),
        ))
        db.send_create_signal(u'apftpmy', ['DomainAlias'])

        # Adding model 'Ftpuser'
        db.create_table('ftpusers', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apftpmy.Account'])),
            ('userid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('passwd', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('uid', self.gf('django.db.models.fields.IntegerField')()),
            ('gid', self.gf('django.db.models.fields.IntegerField')()),
            ('homedir', self.gf('django.db.models.fields.CharField')(default='/var/www/', max_length=150)),
            ('shell', self.gf('django.db.models.fields.CharField')(default='/bin/false', max_length=50)),
        ))
        db.send_create_signal(u'apftpmy', ['Ftpuser'])

        # Adding model 'Customer'
        db.create_table(u'apftpmy_customer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('tel', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=200)),
        ))
        db.send_create_signal(u'apftpmy', ['Customer'])

        # Adding model 'Invoice'
        db.create_table(u'apftpmy_invoice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apftpmy.Customer'])),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apftpmy.Account'])),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 6, 16, 0, 0))),
            ('month', self.gf('django.db.models.fields.IntegerField')()),
            ('size', self.gf('django.db.models.fields.IntegerField')()),
            ('sale', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('price', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('file', self.gf('filebrowser.fields.FileBrowseField')(max_length=200, null=True, blank=True)),
            ('is_paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'apftpmy', ['Invoice'])


    def backwards(self, orm):
        # Deleting model 'Domain'
        db.delete_table(u'apftpmy_domain')

        # Deleting model 'Server'
        db.delete_table(u'apftpmy_server')

        # Deleting model 'Account'
        db.delete_table(u'apftpmy_account')

        # Deleting model 'Project'
        db.delete_table(u'apftpmy_project')

        # Deleting model 'ProjectSetting'
        db.delete_table(u'apftpmy_projectsetting')

        # Deleting model 'ProjectProc'
        db.delete_table(u'apftpmy_projectproc')

        # Deleting model 'DomainAlias'
        db.delete_table(u'apftpmy_domainalias')

        # Deleting model 'Ftpuser'
        db.delete_table('ftpusers')

        # Deleting model 'Customer'
        db.delete_table(u'apftpmy_customer')

        # Deleting model 'Invoice'
        db.delete_table(u'apftpmy_invoice')


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
            'token': ('django.db.models.fields.CharField', [], {'default': "'v0vl24^mf#4w@_u6v&shsmmc-clcqipvx!^1in4eoc7n9@gc(9'", 'max_length': '50'}),
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
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 6, 16, 0, 0)'}),
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
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 16, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_modify': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 16, 0, 0)', 'blank': 'True'}),
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
            'hostname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'os_type': ('django.db.models.fields.IntegerField', [], {}),
            'token': ('django.db.models.fields.CharField', [], {'default': "'y+dcgca)u$@ff90^-u!e)_#x@3mn*ce1*@*d35q2xk!bu5tk&@'", 'max_length': '50'})
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