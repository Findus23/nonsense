#!/bin/bash
if [ ! -z $1 ]
then
	loops=$1
else
	loops=1
fi
i=0
function nomen {
	if [ $(shuf -i 0-10 -n 1) == "1" ]
	then
		praf=$(shuf -n 1 präf.txt)
		echo "$praf$(nomen)"
	elif [ $(shuf -i 0-10 -n 1) == "2" ]
	then
		suf=$(shuf -n 1 suf.txt)
		echo "$(nomen)$suf"
	else
		echo $(shuf -n 1 nomen.txt)
	fi
}
while [ $i -lt $loops ]
do
	ikeaname=$(./ikeagen.py)
	text=$(nomen)
#	adj_count=$(shuf -i 0-2 -n 1)
	adj_count=$(python -c "import random;print '{:1.0f}'.format(round(random.gauss(1.0,1.0)))")
	a=0
	while [ $a -lt $adj_count ]
	do
		if [ $(shuf -i 0-4 -n 1) == "0" ]
		then 
			adj="mit $(shuf -n 1 nomen.txt)"
		else
			adj=$(shuf -n 1 adj.txt)
		fi
		text="$text $adj"
		((a++))
	done
	if [ ! -z $2 ] && [ $2 == "tex-export" ]
	then
		echo "$ikeaname & $text \\\\"
	else
		echo -e "$ikeaname:\t$text"
#		espeak -vde+m2 "$ikeaname: $text"
	fi
	((i++))
done
