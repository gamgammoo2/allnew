#!/bin/bash

input="/etc/passwd"
count=1

cat $input | while IFS=':' read -r username pw uid gid comment home shell
do
	echo "$count : $username - $uid - $gid - $home - $shell"
	count=$[ $count + 1 ]
done < $input
