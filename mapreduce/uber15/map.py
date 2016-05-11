#!/usr/bin/python

import sys

for line in sys.stdin:
    if not line.startswith('Pickup'):
        l = line.strip().split(',')
        day, time = l[0].strip().split(' ')
        hour = time.strip().split(':')[0]
        if l[2]!='Unknown':
            print l[2]+','+l[3]+','+day+','+hour+'\t'+str(1)
