FROM debian:8
MAINTAINER "Pavel Studenik" <studenik@varhoo.cz>

RUN apt-get update && apt install -y subversion python virtualenv gcc python-dev

RUN mkdir -p /data/ && \
    svn co http://github.com/Pajinek/vhm/trunk/server/ /data/vhm --non-interactive  --trust-server-cert

WORKDIR /data/vhm
RUN useradd -ms /bin/bash vhm \
    && chown vhm:vhm -R .

USER vhm

RUN virtualenv env && \
    . env/bin/activate && \
    pip install -r requirements/basic.pip && \ 
    python manage.py syncdb --all || true

# create first user
RUN . env/bin/activate && \
    echo 'from django.contrib.sites.models import Site; site = Site.objects.create(domain="localhost", name="localhost"); site.save()' | python manage.py shell && \
    echo 'from django.contrib.auth.models import User; User.objects.create_superuser("admin", "admin@example.com", "pass")' | python manage.py shell

EXPOSE 8000
CMD . env/bin/activate && python manage.py runserver 0.0.0.0:8000



