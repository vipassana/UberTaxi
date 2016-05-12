#!/usr/bin/python

import sys

prev_key = ''

for line in sys.stdin:
    curr_key, val = line.strip().split('\t')
    if curr_key!=prev_key:
        if prev_key:
            print '%s\t%d'%(prev_key,cnt)
        cnt = int(val)
    else:
	cnt += int(val)
    prev_key = curr_key

print '%s\t%d'%(prev_key,cnt)