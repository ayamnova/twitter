#! /bin/bash
filename='userMatrix'
echo "lineNum    0s     1s"
num=1
while read data; do
	  # ones=$(echo data | awk -F '1' '{print NF-1}')
	  ones=$(echo $data | awk -F '1' '{print NF}')
	  zeros=$(echo $data | awk -F '0' '{print NF-1}')
	  total=$((zeros+$ones))
	  printf "%4d   %5d    %6d    %7d\n" $num $zeros $ones $total
	  num=$(($num+1))
done < $filename
