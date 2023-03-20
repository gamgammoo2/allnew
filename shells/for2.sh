#!/bin/bash

row="one two three"

#c style

for mon in $row; do
	for ((i=0; i<9; i++)) do
		echo "$mon $i"
	done
done

