#!/bin/env bash
tmp=$(mktemp);ans=$(mktemp)
cat mirrorlist.txt|grep 'http'|head -n 10 | cut -d '/' -f3 > $tmp
while read line
do 
	echo $line $(ping -c 3 -q $line|grep 'avg'|cut -d '/' -f5) >> $ans
done < $tmp
sort -nk 2 $ans | cut -d ' ' -f1
rm $tmp;rm $ans
