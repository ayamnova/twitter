#! /bin/sh
# find all the day folders in the given month
#dirs=$(find ./crisis/crisis/2018/06 -type d -maxdepth 1 -mindepth 1 | sort)
# loop through all the days
#for directory in $dirs
#do
   # find all the files
   #files=$(find $directory -type f -not -iname "*.tmp") 
   # find the total number of tweets
   #total=$(cat $files | wc -l)
   # find the total number of English tweets
   #eng=$(jq '.lang' $files | grep en | wc -l)
   # print that to the daily total 
   #echo $directory,$total,$eng >> ./out/daily-totals-test.txt
#done
directory=$1
# files=$(find $directory -type f -not -iname "*.tmp") 
# find the total number of tweets
# total=$(cat $files | wc -l)
# find the total number of English tweets
# eng=$(jq '.lang' $files | grep en | wc -l)
# print that to the daily total 
total=$(find $directory -type f -not -iname "*.tmp" -exec cat {} + | wc -l)
echo $total
eng=$(find $directory -type f -not -iname "*.tmp" -exec jq '.lang' {} + | grep en | wc -l)
echo $eng
# echo $directory,$total,$eng >> ./out/daily-totals-test.txt
echo $directory,$total,$eng
