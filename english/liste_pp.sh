#!/bin/bash

sort ikeaname.txt | uniq > ikeaname.txt.tmp
sort descr.txt | uniq > descr.txt.tmp
mv ikeaname.txt.tmp ikeaname.txt
mv descr.txt.tmp descr.txt

