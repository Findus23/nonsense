#!/usr/bin/python3
import random
import sys

table= [ [ 0 for i in range(2210) ] for j in range(2210) ]
contents = open("ikeaname.txt").read().splitlines()
anzahl=0
for name in contents:
	name= " " + name + " "
	zeichen=list(name)
	zeichenl=len(zeichen)
	zeichenl += -1
	a=0
	while a < zeichenl:
		table[ord(zeichen[a])][ord(zeichen[a+1])] +=1
		anzahl +=1
		a +=1
#row=0
#col=0
#for coln in range(221):
#	for rown in range(221):
#		if table[coln][rown] != 0:
#			print(table[coln][rown],chr(rown),chr(coln))
#print(anzahl)
def letter(a):
	mylist=[]
	for b in range(221):
		for x in range(table[a][b]):
			mylist.append(b)

	return random.choice(mylist)
try:
	num=int(sys.argv[1])
except:
	num=1
textnr=0
while textnr < num:
	a=32
	wort=[]
	while a != 32 or wort == []:
		a=letter(a)
		wort.append(chr(a))
	if len(wort) > 3:
		print("".join(wort))
		textnr +=1
