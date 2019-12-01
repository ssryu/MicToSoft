#!/bin/sh
cp -p $1 $1.bak
gzip $1.bak
cat /dev/null > $1
