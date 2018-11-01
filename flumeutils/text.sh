#! /bin/bash

folder="$HOME/aprojects/REU/data/25crisis/";
files=$(ls $folder);
zero="0"
for f in $files
do
	haystack=$(jq '.text' $folder$f);
	inarray=$(echo ${haystack[@]} | grep -o 'syria\|assad\|refugee\|chemical attack' | wc -w);
	if [ "$inarray" -ne "$zero" ]
	then
		cp $folder$f "$HOME/aprojects/REU/data/flume/"
	fi
done
