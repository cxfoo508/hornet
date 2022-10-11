#!/bin/bash
for id in `docker ps -a|awk '{print $1}'`
do
	if [ ${id} != "05b7de90e2c1" ];then
		docker rm $id
	fi
done

for mid in `docker images|awk '{print $3}'`
do
	if [ $mid != "23fa8b4529d2" ];then
		docker rmi $mid
	fi
done
