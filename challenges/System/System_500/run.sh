#!/bin/bash

if [ $# -ne 1 ]
then
	echo "Usage: $0 ./hecho"
	exit
fi

# HeCHO runs on socat, so if you want to test in local you have to install socat.
# sudo apt-get install socat
# and use below command ( when do local test, use bind=localhost )
# socat TCP-LISTEN:12345,reuseaddr,fork,bind=localhost EXEC:"$1"
socat TCP-LISTEN:12345,reuseaddr,fork,bind=192.168.58.131 EXEC:"$1"
