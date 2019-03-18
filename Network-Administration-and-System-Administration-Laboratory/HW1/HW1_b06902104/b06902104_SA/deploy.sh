#!/bin/env bash
if [ "$1" != "-d" ];then		#if -d option is not set
	eval $(ssh-agent)
	key_path=$(getent passwd "$1" | cut -d ':' -f6)/$2
	#echo $key_path
	ssh-add $key_path
	for i in {1..15}
	do
		ssh -A $1@linux$i.csie.org $(echo $@ | cut -d ' ' -f 3-$# );
	done
	for i in {1..3}
	do
		ssh -A $1@oasis$i.csie.org $(echo $@ | cut -d ' ' -f 3-$#);
	done
	ssh -A $1@bsd1.csie.org $(echo $@ | cut -d ' ' -f 3-$#);
	ssh-agent -k
else					#if -d option is set
	eval $(ssh-agent)
	key_path=$(getent passwd "$2" | cut -d ':' -f6)/$3
	#echo $key_path
	ssh-add $key_path
	for i in {1..15}
	do
		ssh -A -t $2@linux$i.csie.org  screen -d -m $(echo $@ | cut -d ' ' -f 4-$#) #use screen -d -m to let the commend to run in the background.( start screen in detached mode )
	done
	for i in {1..3}
	do
		ssh -A -t $2@oasis$i.csie.org screen -d -m $(echo $@ | cut -d ' ' -f 4-$#) #use screen -d -m to let the commend to run in the background.( start screen in detached mode )
	
	done
	ssh -A -t $2@bsd1.csie.org screen -d -m $(echo $@ | cut -d ' ' -f 4-$#); #use screen -d -m to let the commend to run in the background.( start screen in detached mode )
	
	ssh-agent -k
fi

