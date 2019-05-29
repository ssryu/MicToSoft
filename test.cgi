#!/home/mukiaeahy/local/python/bin/python3

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("Content-Type: text/html; charset=utf-8")
print("Access-Control-Allow-Origin: *\n")
print("")

print("hello, NLP and ML!")
