#!/usr/bin/python

import sys

prev_key = ''

for line in sys.stdin:
    l = line.strip().split('\t')
    curr_key = l[0]
    if curr_key!=prev_key:
        if prev_key:
            print '%s\t%d'%(prev_key,cnt)
        cnt = 1
    else:
        cnt += 1
    prev_key = curr_key

print '%s\t%d'%(prev_key,cnt)
