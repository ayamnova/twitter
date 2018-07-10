#! /bin/sh

# find all the day folders in the given month
dirs=$(find ./crisis/crisis/2018/05 -type d -maxdepth 1 -mindepth 1 | sort)
# loop through all the days
for directory in $dirs
do
   # find the total number of tweets
   total=$(find $directory -type f -not -iname "*.tmp" | xargs cat | wc -l)
   # print that to the daily total 
   echo $directory,$total >> ./out/daily-totals.txt
done
