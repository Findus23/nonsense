#!/bin/bash
if [ ! -z $1 ]
then
	loops=$1
else
	loops=1
fi
i=0
while [ $i -lt $loops ]
do
	ikeaname=$(./ikeagen.py)
	text=$(shuf -n 1 adj.txt)
#	adj_count=$(shuf -i 0-2 -n 1)
	adj_count=$(python -c "import random;print '{:1.0f}'.format(round(random.gauss(3.0,3.0)))")
	a=0
	while [ $a -lt $adj_count ]
	do
		if [ $(shuf -i 0-4 -n 1) == "0" ]
		then 
			adj="with $(shuf -n 1 adj.txt)"
		else
			adj=$(shuf -n 1 adj.txt)
		fi
		text="$text $adj"
		((a++))
	done
	echo "$ikeaname: $text"
	echo "$ikeaname: $text" | festival --tts
	((i++))
done
