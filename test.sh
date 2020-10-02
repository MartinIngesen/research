#!/bin/bash

# 1) save it as xssaminer
# 2) allow execution: chmod +x xssaminer
# 3) run it & check usage: ./xssaminer

if [ -z $1 ]
then
	echo -e "Usage:\n$0 FILE\n$0 -r FOLDER"
	exit
else
	f=$1
fi

sources=(GET POST REQUEST "SERVER\['PHP" "SERVER\['PATH_" "SERVER\['REQUEST_U")
sinks=(? echo die print printf print_r var_dump)

xssam(){
	for i in ${sources[@]}
	do
		a=$(grep -in "\$_${i}" $f | grep -o "\$.*=" | sed "s/[ ]\?=//g" | sort -u)

		for j in ${sinks[@]}
		do
			grep --color -in "${j}.*\$_${i}" $f

			for k in $a
			do
				grep --color -in "${j}.*$k" $f
			done
		done
	done
}

if [ $f != "-r" ]
then
	xssam
else
	for i in $(find $2 -type f -name "*.php")
	do
		echo "File: $i"
		f=$i
		xssam
	done
fi
