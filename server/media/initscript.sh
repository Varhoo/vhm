#/bin/bash
# init script 
# run  curl http://localhost:8000/media/initscript.sh -s | xargs -l sh 

pip install vhm-client --upgrade
vhm_check -v
