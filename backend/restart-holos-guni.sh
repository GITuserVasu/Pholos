#! /usr/bin/bash
<<<<<<< HEAD
cd /home/bitnami/Pholos/backend
=======
cd /home/bitnami/DEVholos2/backend
>>>>>>> f5ff564bb5d8a849c0a81fece49fb0b8366204e6
#echo $(pwd) >> /home/bitnami/restart-holos.log 
#var=`ps -aux | grep -v grep | grep -c guni` 
#echo $var
#var=`pgrep -c guni` 
#echo "Var = $var"
#if  [ $var -le 1 ] 
#then
<<<<<<< HEAD
	echo "Restarting Prod holos guni: $(date) " >> /home/bitnami/prodholos-restart-guni.log
        nohup gunicorn --env DJANGO_SETTINGS_MODULE=proj_1.settings -b 172.31.23.62:6666 proj_1.wsgi > /home/bitnami/prodholos.log 2>&1 &
	echo "guni  holos restarted" >> /home/bitnami/prodholos-restart-guni.log
=======
	echo "Restarting holos guni: $(date) " >> /home/bitnami/devtestholos-restart-guni.log
        nohup gunicorn --env DJANGO_SETTINGS_MODULE=proj_1.settings -b 172.31.23.62:6666 proj_1.wsgi > /home/bitnami/devtestholos.log 2>&1 &
	echo "guni  holos restarted" >> /home/bitnami/devtestholos-restart-guni.log
>>>>>>> f5ff564bb5d8a849c0a81fece49fb0b8366204e6
#else
#	echo "guni already running $(date)" >> /home/bitnami/restart-guni.log
#fi
