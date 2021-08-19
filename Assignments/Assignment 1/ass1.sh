#!/usr/bin/bash
traceroute -I $1 > temp.txt
cat temp.txt | while read line || [[ -n $line ]];
do
   echo $line
done