#!/bin/bash
rm ikeaname.txt
rm descr.txt

for i in {0..25}
do
	wget -O download.tmp http://www.ikea.com/at/de/catalog/productsaz/$i/
	grep "productsAzLink" download.tmp > lines.tmp
	while read line; do
		name=$(echo $line | xmllint --xpath 'string(//a)' -)
		ikeaname=$(echo "$name" | egrep -o "((([A-Z])+){2,} *)+")
		descr=${name#$ikeaname}
		echo $ikeaname >> ikeaname.txt
		echo $descr >> descr.txt
	done <lines.tmp
done
rm *.tmp

sort ikeaname.txt | uniq > ikeaname.txt.tmp
sort descr.txt | uniq > descr.txt.tmp
mv ikeaname.txt.tmp ikeaname.txt
mv descr.txt.tmp descr.txt

