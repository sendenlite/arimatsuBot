#!/bin/sh

end()
{
echo "    exit"
ps aux | grep stream.py | grep -v grep | awk '{ print "kill -9", $2 }' | sh
exit
}

trap end 2


while [ 1 ]
do
    grep=`ps ax | grep stream.py | grep -v grep` 
    if [ "${grep}" = "" ]
    then
        python3 stream.py &
        echo "start on bash"
    fi 
    grep=""
    sleep 5m
done
