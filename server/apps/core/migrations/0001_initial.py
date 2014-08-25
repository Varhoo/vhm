# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Domain'
        db.create_table(u'core_domain', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('expirate', self.gf('django.db.models.fields.DateField')(default=datetime.datetime.now, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('last_modify', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Domain'])

        # Adding model 'Server'
        db.create_table(u'core_server', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hostname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('total_mem', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_hd', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('last_checked', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('global_ip', self.gf('django.db.models.fields.IPAddressField')(default='0.0.0.0', max_length=15)),
            ('os_type', self.gf('django.db.models.fields.IntegerField')()),
            ('token', self.gf('django.db.models.fields.CharField')(default='sf6tge@)(a_#!btve-2)8sr0fs_0bh-7*ymdjuavof!(oe-w!k', max_length=50)),
        ))
        db.send_create_signal(u'core', ['Server'])

        # Adding model 'Account'
        db.create_table(u'core_account', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('server', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Server'])),
            ('name', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=64)),
            ('path', self.gf('django.db.models.fields.CharField')(default='/var/www/', max_length=64)),
            ('size', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('token', self.gf('django.db.models.fields.CharField')(default='0pomgpdpha0#rj0&f-31$j9k^tw-@4h!&u9#n@c0v157s_7c$2', max_length=50)),
            ('user', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('uid', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('gid', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Account'])

        # Adding model 'Project'
        db.create_table(u'core_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Account'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('site', self.gf('django.db.models.fields.CharField')(max_length=126)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=126)),
            ('is_enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('last_modify', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'core', ['Project'])

        # Adding model 'ProjectSetting'
        db.create_table(u'core_projectsetting', (
            (u'project_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.Project'], unique=True, primary_key=True)),
            ('repo_type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('repo_url', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('repo_version', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['ProjectSetting'])

        # Adding model 'TemplateProc'
        db.create_table(u'core_templateproc', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('file_type', self.gf('django.db.models.fields.IntegerField')()),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'core', ['TemplateProc'])

        # Adding model 'ProjectProc'
        db.create_table(u'core_projectproc', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.ProjectSetting'])),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.TemplateProc'])),
            ('params', self.gf('django.db.models.fields.TextField')(max_length=256, null=True, blank=True)),
            ('is_running', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'core', ['ProjectProc'])

        # Adding model 'DomainAlias'
        db.create_table(u'core_domainalias', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.CharField')(max_length=126)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Project'])),
        ))
        db.send_create_signal(u'core', ['DomainAlias'])

        # Adding model 'Ftpuser'
        db.create_table('ftpusers', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Account'])),
            ('userid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('passwd', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('uid', self.gf('django.db.models.fields.IntegerField')()),
            ('gid', self.gf('django.db.models.fields.IntegerField')()),
            ('homedir', self.gf('django.db.models.fields.CharField')(default='/var/www/', max_length=150)),
            ('shell', self.gf('django.db.models.fields.CharField')(default='/bin/false', max_length=50)),
        ))
        db.send_create_signal(u'core', ['Ftpuser'])


    def backwards(self, orm):
        # Deleting model 'Domain'
        db.delete_table(u'core_domain')

        # Deleting model 'Server'
        db.delete_table(u'core_server')

        # Deleting model 'Account'
        db.delete_table(u'core_account')

        # Deleting model 'Project'
        db.delete_table(u'core_project')

        # Deleting model 'ProjectSetting'
        db.delete_table(u'core_projectsetting')

        # Deleting model 'TemplateProc'
        db.delete_table(u'core_templateproc')

        # Deleting model 'ProjectProc'
        db.delete_table(u'core_projectproc')

        # Deleting model 'DomainAlias'
        db.delete_table(u'core_domainalias')

        # Deleting model 'Ftpuser'
        db.delete_table('ftpusers')


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
        u'core.account': {
            'Meta': {'object_name': 'Account'},
            'gid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'path': ('django.db.models.fields.CharField', [], {'default': "'/var/www/'", 'max_length': '64'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Server']"}),
            'size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'token': ('django.db.models.fields.CharField', [], {'default': "'0pomgpdpha0#rj0&f-31$j9k^tw-@4h!&u9#n@c0v157s_7c$2'", 'max_length': '50'}),
            'uid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'core.domain': {
            'Meta': {'object_name': 'Domain'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expirate': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modify': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'core.domainalias': {
            'Meta': {'object_name': 'DomainAlias'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Project']"}),
            'site': ('django.db.models.fields.CharField', [], {'max_length': '126'})
        },
        u'core.ftpuser': {
            'Meta': {'object_name': 'Ftpuser', 'db_table': "'ftpusers'"},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Account']"}),
            'gid': ('django.db.models.fields.IntegerField', [], {}),
            'homedir': ('django.db.models.fields.CharField', [], {'default': "'/var/www/'", 'max_length': '150'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'passwd': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'shell': ('django.db.models.fields.CharField', [], {'default': "'/bin/false'", 'max_length': '50'}),
            'uid': ('django.db.models.fields.IntegerField', [], {}),
            'userid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'core.project': {
            'Meta': {'object_name': 'Project'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Account']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_modify': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '126'}),
            'site': ('django.db.models.fields.CharField', [], {'max_length': '126'})
        },
        u'core.projectproc': {
            'Meta': {'object_name': 'ProjectProc'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_running': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'params': ('django.db.models.fields.TextField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.ProjectSetting']"}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.TemplateProc']"})
        },
        u'core.projectsetting': {
            'Meta': {'object_name': 'ProjectSetting', '_ormbases': [u'core.Project']},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'project_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Project']", 'unique': 'True', 'primary_key': 'True'}),
            'repo_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'repo_url': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'repo_version': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        u'core.server': {
            'Meta': {'object_name': 'Server'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'global_ip': ('django.db.models.fields.IPAddressField', [], {'default': "'0.0.0.0'", 'max_length': '15'}),
            'hostname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_checked': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'os_type': ('django.db.models.fields.IntegerField', [], {}),
            'token': ('django.db.models.fields.CharField', [], {'default': "'sf6tge@)(a_#!btve-2)8sr0fs_0bh-7*ymdjuavof!(oe-w!k'", 'max_length': '50'}),
            'total_hd': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_mem': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'core.templateproc': {
            'Meta': {'object_name': 'TemplateProc'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'file_type': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['core']