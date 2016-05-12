#!/usr/bin/python

import sys

for line in sys.stdin:
    l = line.strip().split(',')
    t = l[2].strip().split(':')
    print l[0]+','+l[1]+','+t[0]+'\t'+l[3]