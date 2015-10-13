FROM debian:8
MAINTAINER "Pavel Studenik" <studenik@varhoo.cz>

RUN apt-get update && apt install -y subversion vim python python-psutil

RUN svn co https://github.com/Pajinek/vhm/trunk/tools/ /root/tools

WORKDIR /root/tools

CMD python /root/tools/vhm_check.py




