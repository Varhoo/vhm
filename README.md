Varhoo Manager
=============

It's client/server application for manage django, php projects on remote servers. Applicion support:

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
