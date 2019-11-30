#!/bin/sh
cp -p test.txt test.txt.bak
gzip test.txt.bak
cat /dev/null > text.txt
