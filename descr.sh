#!/bin/bash
rm nomen.txt
rm adj.txt
grep -E -o '(\w|\.|\-)+' descr.txt | sort | uniq > descr_words.txt

while read line; do
	if [ $(echo $line | cut -c 1) == "-" ]
	then
		echo $line >> suf.txt
		echo "Suffix"
	elif [ $(echo $line  | rev | cut -c 1) == "-" ]
	then
		echo $line >> präf.txt
		echo "Präfix"
	elif echo $line | grep [[:upper:]] >/dev/null 
	then
		if echo $line | grep [[:lower:]] >/dev/null
		then #Groß und Klein-> Nomen
			echo $line >>nomen.txt
			echo "Nomen"
		fi # nur Groß -> Ikeaname -> verwerfen
	elif echo $line | egrep  "([[:lower:]]){3,}" >/dev/null
	then # keine Großbuchstaben, aber Kleinbuchstaben -> kein Nomen
		echo $line >>adj.txt
		echo "kein Nomen"
	#weder Großbuchstaben noch Kleinbuchstaben -> Zahl -> verwerfen
	fi
done <descr_words.txt
