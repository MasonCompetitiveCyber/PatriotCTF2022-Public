#!/bin/bash

curr=0
currHex=0

while [ $curr -le 65535 ]
do
    currHex=$(printf '%x\n' $curr)
    echo $currHex | ./flowing | grep "pctf{"
    ((curr++))
done