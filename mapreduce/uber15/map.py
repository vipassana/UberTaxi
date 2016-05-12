#!/usr/bin/python

import sys

for line in sys.stdin:
    if not line.startswith('Pickup'):
        l = line.strip().split(',')
        t = l[0].strip().split(':')
        if l[2]!='Unknown':
            print l[2]+','+l[3]+','+t[0]+'\t'+str(1)
