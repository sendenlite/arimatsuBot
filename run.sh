#!/bin/sh



while [ 1 ]
do
    grep=`ps ax | grep stream.py | grep -v grep` 
    if [ "${grep}" = "" ]
    then
        python3 stream.py &
    fi 
    grep=""
    sleep 5m
done
