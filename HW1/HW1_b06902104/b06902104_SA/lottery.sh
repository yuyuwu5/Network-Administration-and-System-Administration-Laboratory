#!/bin/env bash
#win_list=$1
#receipt=$2
echo the number of receipts: $(wc -l $2|cut -d ' ' -f1)
valid=0;money=0;win_rec=0;
for rec_line in $(sed -En '/(^[0-9]{8}$)|(^[A-Za-z]{2}-[0-9]{8}$)|(^[A-Za-z]{2}[0-9]{8}$)/p' $2)
do
	((valid++))
	special=$(sed -n '1p' $1) 
	if [ "$special" = "$rec_line" ];then
		((money+=10000000))
		win[win_rec]=$rec_line
		win_money[win_rec]=10000000
		((win_rec++))
	fi
	grand=$(sed -n '2p' $1)
	if [ "$grand" = "$rec_line" ];then
		((money+=2000000))
		win[win_rec]=$rec_line
		win_money[win_rec]=2000000
		((win_rec++))
	fi
	for prize_line in $(sed -n '3,5p' $1)
	do
		count=0
		for i in {3..8}
		do
			a=$(echo $prize_line|rev|cut -c 1-$i)
			b=$(echo $rec_line|rev|cut -c 1-$i)
			if [ "$a" = "$b" ];then
				count=$i
			else
				break
			fi
		done
		if [ "$count" = "3" ];then
			((money+=200))
			win[win_rec]=$rec_line
			win_money[win_rec]=200
			((win_rec++))
		elif [ "$count" = "4" ];then
			((money+=1000))
			win[win_rec]=$rec_line
			win_money[win_rec]=1000
			((win_rec++))
		elif [ "$count" = "5" ];then
			((money+=4000))
			win[win_rec]=$rec_line
			win_money[win_rec]=4000
			((win_rec++))
		elif [ "$count" = "6" ];then
			((money+=10000))
			win[win_rec]=$rec_line
			win_money[win_rec]=10000
			((win_rec++))
		elif [ "$count" = "7" ];then
			((money+=40000))
			win[win_rec]=$rec_line
			win_money[win_rec]=40000
			((win_rec++))
		elif [ "$count" = "8" ];then
			((money+=200000))
			win[win_rec]=$rec_line
			win_money[win_rec]=200000
			((win_rec++))
		fi

	done
	for sorry_prize in $(sed -n '5,8p' $1)
	do
		a=$(echo $sorry_prize|rev)
		b=$(echo $rec_line|rev|cut -c 1-3)
		if [ "$a" = "$b" ];then
			((money+=200))
			win[win_rec]=$rec_line
			win_money[win_rec]=200
			((win_rec++))
		fi

	done
	
done
echo The number of valid receipts: $valid
echo The number of winning lotteries: $win_rec
echo The winning money: $money
index=1;i=0
while read line
do
	if [ "$line" = "${win[$i]}" ];then
		printf "%-4s%-12s%-5s%-3s\n" $(($i+1)). $line '('$index')' '$'${win_money[i]}
		((i++))
	fi
	((index++))
done < $2
