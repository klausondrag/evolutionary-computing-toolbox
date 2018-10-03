#!/bin/bash
sleep 1m
echo "check:------------------------------------------checking..."
grep "Manager has exited with status code 1, restarting experiment..." output.txt #&> /dev/null
if [ $? == 0 ] 
then
	echo "check:------------------------------------------ERROR FOUND!"
	echo "ERROR" > elog.txt
	bash kill.sh
	rm output.txt
	echo "Restarting..."
	bash start.sh&
	echo "Restarted!"
	kill -9 $$
	break
else
	echo "check:------------------------------------------NO ERROR FOUND" 
	echo "check:" > output.txt
	sleep 1m
fi
tail -1 output.txt | grep "check:" #&> /dev/null
if [ $? == 0 ] 
then
	echo "check:------------------------------------------TIMED OUT!"
	echo "Timed out" > elog.txt
	bash kill.sh
	rm output.txt
	echo "check:------------------------------------------Restarting..."
	bash start.sh&
	echo "check:------------------------------------------Restarted!"
	kill -9 $$
	break
fi
bash check.sh&
kill -9 $$
