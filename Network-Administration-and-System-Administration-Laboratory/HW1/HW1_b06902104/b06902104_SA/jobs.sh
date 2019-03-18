#!/bin/env bash
list=0;mem=0;cpu=0;help_=0 #set show information false
part=""                    #ask for parts of command
full=""                    #ask for full command
for argument               #detemine if it is part or full argument
do
	if echo "."$argument | grep -q ".\-\-";then
		full=$full$argument" "
		#echo full $full
	elif echo "."$argument | grep -q ".\-";then
		part=$part$argument" "
		#echo part $part
	else 
		echo Extra arguments -- "$argument"
		echo Try 'jobs.sh -h' for more information.
		exit
	fi
done
for argument in $full
do
	if [ "$argument" = "--list" ];then
		list=1
	elif [ "$argument" = "--mem" ];then
		mem=1
	elif [ "$argument" = "--cpu" ];then
		cpu=1
	elif [ "$argument" = "--help" ];then
		help_=1
	else
		echo Invalid option: "$argument"
		echo Try 'jobs.sh -h' for more information.
		exit
	fi
done
if [ "$part" != "" ];then
	while getopts ":lmch" argument $part
	do
		#echo $argument
		if [ "$argument" = "l" ];then
			list=1
			#echo 1
		elif [ "$argument" = "m" ];then
			mem=1
			#echo 2
		elif [ "$argument" = "c" ];then
			cpu=1
			#echo 3
		elif [ "$argument" = "h" ];then
			help_=1
			#echo 4
		else
			help_=1
			echo getopt: invalid option -- "$OPTARG"
		fi
	done
fi
if [ "$help_" = "1" ];then 
	echo jobs.sh '[OPTION...]'
	echo -l, --list		list all grades in descendant order of consuming resourse
	echo '(according to CPU usage first, then memory usage)'
	echo -m, --mem		print the usage of memory '(in KB)'
	echo -c, --cpu		print the usage of CPU '(in %)'
	echo -h, --help		print this help message
	exit
fi
file=$(mktemp)
ps aux | awk '{print $1 " " $3 " " $6}' | sed '1d' >"$file"
t1=$(mktemp)
t2=$(mktemp)
use_list=$(mktemp)
name_list=$(mktemp)
cat "$file"|awk '{print $1}'|cut -c 1-3 > "$t1"
cat "$file"|awk '{print $2 "\t" $3}' >"$t2"
#cat "$file"|awk '{print $1 "\t" $2 "\t" $3}'

sed -i 's/[^brp][a-z,0-9][a-z,0-9]/other/' "$t1" 
sed -i 's/[brp][a-z][a-z]/other/' "$t1"
paste "$t1" "$t2" |sort -u > "$use_list"
#cat $use_list
cat "$use_list" | awk '{print $1}'| sort -u >"$name_list"
rm -f "$file";rm -f "$t1";rm -f "$t2";
a=$(mktemp)
answer=$(mktemp)
while read line
do
	cat "$use_list"| grep "$line" |awk '{		
		c += $2
		m += $3
	}END {print c "\t" m}' >> $a
done < "$name_list" 
paste "$name_list" "$a" | sort -nrk 2 -nrk 3 |sed '1 iGROUP	CPU(%)	MEM(KB)' >"$answer"
#cat answer
rm -f "$use_list";rm -f "$name_list";rm -f "$a"
cat "$answer" | awk -v l="$list" -v c="$cpu" -v m="$mem" '{
	if(l==1) 
		printf "%s\t",$1
	if(c==1)
		printf "%s\t",$2
	if(m==1)
		printf "%s\n",$3
	else
		printf "\n"}' |if [ "$list" = "0" ];then
		if [ "$cpu" = "0" ];then
			if [ "$mem" = "0" ];then
				cat "$answer"|awk '{print $1}'|head -n2
			else
				cat
			fi
		else 
			cat
		fi
	else
		cat
	fi
rm -f "$answer"
