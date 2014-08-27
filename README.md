Varhoo Manager
=============

It's client/server application for manage django, php projects on remote servers. Application supports followin operations:

* Manage projects, systems
* Production running due to uwsgi, proxy, appache2
* Repository SVN, GIT
* Automation for update project
* Monitoring remote systems

Installation

<pre>
pip install -r requirements.txt
</pre>
 

Run server

<pre>
cd server
python manage.py runserver
</pre>
 

Run client

<pre>
cd tools
python vhm_check.py
</pre>


Default template for uwsgi socket (Python):
<pre>
&#x3C;uwsgi id=&#x22;{{id}}&#x22;&#x3E;
      &#x3C;wsgi-file&#x3E;{{root_proc}}/wsgi.py&#x3C;/wsgi-file&#x3E;
      &#x3C;processes&#x3E;1&#x3C;/processes&#x3E;
      &#x3C;chdir&#x3E;{{root_proc}}&#x3C;/chdir&#x3E;
      &#x3C;uid&#x3E;{{uid}}&#x3C;/uid&#x3E;
      &#x3C;gid&#x3E;{{gid}}&#x3C;/gid&#x3E;
      &#x3C;pythonpath&#x3E;{{root_proc}}&#x3C;/pythonpath&#x3E;
      &#x3C;limit-as&#x3E;256&#x3C;/limit-as&#x3E;
      &#x3C;optimize&#x3E;0&#x3C;/optimize&#x3E;
      &#x3C;daemonize&#x3E;{{root}}log/{{id}}-{{name}}.log&#x3C;/daemonize&#x3E;
      &#x3C;master/&#x3E;
      &#x3C;home&#x3E;/opt/env&#x3C;/home&#x3E;
      &#x3C;no-orphans/&#x3E;
      &#x3C;pidfile&#x3E;{{root}}{{id}}-{{name}}.pid&#x3C;/pidfile&#x3E;
      &#x3C;socket&#x3E;0.0.0.0:{{port}}&#x3C;/socket&#x3E;
&#x3C;/uwsgi&#x3E;
</pre>

And basic template looks as follows (PHP):
<pre>
&#x3C;VirtualHost *:80&#x3E;
        ServerAdmin {{ admin_email }}
        ServerName {{domain}}
{% for alias in alias_list %}
        ServerAlias {{ alias }}
{% endfor %}
        DocumentRoot {{root_proc}}
&#x3C;/VirtualHost&#x3E;
</pre>

Basic apache proxy configuration:

<pre>
&lt;VirtualHost _default_:443&gt;
        ServerAdmin {{ admin_email }}
        ServerName {{domain}}
{% for alias in alias_list %}
        ServerAlias {{ alias }}
{% endfor %}
          ProxyPass / uwsgi://0.0.0.0:{{port}}/
        ProxyPassReverse / uwsgi://0.0.0.0:{{port}}/
&lt;/VirtualHost&gt;
</pre>

advanced way to configure apache proxy looks following:

<pre>
&lt;VirtualHost _default_:443&gt;
        ServerAdmin {{ admin_email }}
        ServerName {{domain}}
{% for alias in alias_list %}
        ServerAlias {{ alias }}
{% endfor %}
  &lt;Location /media/&gt;
       SetHandler None
       Order deny,allow
       Allow from all
       Options -Indexes
  &lt;/Location&gt;
  &lt;Location /static/&gt;
       SetHandler None
       Order deny,allow
       Allow from all
       Options -Indexes
  &lt;/Location&gt;
  alias /media/ {{root_proc}}{{media}}
  alias /static/ {{root_proc}}{{static}}
  ProxyPreserveHost On
        ProxyErrorOverride Off
  ProxyPass /media !
  ProxyPass /static !
        ProxyPass / uwsgi://0.0.0.0:{{port}}/
        ProxyPassReverse / uwsgi://0.0.0.0:{{port}}/
&lt;/VirtualHost&gt;
</pre>