#! /usr/bin/bash
cd /home/bitnami/DEVholos2/backend
#echo $(pwd) >> /home/bitnami/restart-holos.log 
#var=`ps -aux | grep -v grep | grep -c guni` 
#echo $var
#var=`pgrep -c guni` 
#echo "Var = $var"
#if  [ $var -le 1 ] 
#then
	echo "Restarting holos guni: $(date) " >> /home/bitnami/devtestholos-restart-guni.log
        nohup gunicorn --env DJANGO_SETTINGS_MODULE=proj_1.settings -b 172.31.23.62:6666 proj_1.wsgi > /home/bitnami/devtestholos.log 2>&1 &
	echo "guni  holos restarted" >> /home/bitnami/devtestholos-restart-guni.log
#else
#	echo "guni already running $(date)" >> /home/bitnami/restart-guni.log
#fi
