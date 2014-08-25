#!/bin/bash

#DIR_SCRIPT=`pwd`/$0
DIR_SCRIPT=`echo $0 | sed 's/[^\/]*$//' `
TMP_DIR=/tmp/django-apache-tmp/
APACHE_DIR_ENABLE=/etc/apache2/sites-enabled/
APACHE_DIR_AVAIBLE=/etc/apache2/sites-available/

mkdir -p $TMP_DIR
$DIR_SCRIPT"generate.py" --set-chown --dir $TMP_DIR

COUNT=0
for file in `ls $TMP_DIR`
do
	TMP_NAME="$TMP_DIR$file" 
	#echo $SITE_NAME $TMP_NAME
	if [ -f $APACHE_DIR_AVAIBLE$file ] 
	then
		if [ `diff $APACHE_DIR_AVAIBLE$file $TMP_NAME | wc -l` -gt 0 ]
		then
			STATUS="0"
			echo -n "Update record $file...   "
			cp $TMP_NAME "$APACHE_DIR_AVAIBLE$file"
			STATUS=`expr $STATUS + $?`
			if [ $STATUS = 0 ]
			then
				echo "[OK]"
				COUNT=`expr $COUNT + 1`
			else
				echo "[FAIL]"
			fi  
		fi
	else
		STATUS="0"
		echo -n "Create record $file...   "
		cp $TMP_NAME "$APACHE_DIR_AVAIBLE$file"
		STATUS=`expr $STATUS + $?`
		ln -s "$APACHE_DIR_AVAIBLE$file" "$APACHE_DIR_ENABLE$file"
		STATUS=`expr $STATUS + $?`
		if [ $STATUS = 0 ]
		then
			echo "[OK]"
			COUNT=`expr $COUNT + 1`
		else
			echo "[FAIL]"
		fi  
	fi
done

if [ $COUNT != "0" ]; then
	service apache2 status
	service apache2 reload
fi

if [ $COUNT != 0 ] || [ "$1" = '--test' ]; then
   for SITE in `cat  ${TMP_DIR}* | grep ServerName | awk '{print $2}'` 
   do
	wget -q -O /dev/null http://$SITE
	if [ "$?" = "0" ]; then
		echo "Site $SITE ... [OK]"
	else
		echo "Site $SITE ... [FAIL]"
		echo "Site is down" | mail studenik@varhoo.cz -s "$SITE is down"
	fi
   done
fi
	
#rm ${TMP_DIR}0*
#rmdir ${TMP_DIR}
