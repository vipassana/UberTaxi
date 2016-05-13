#!/usr/bin/python

import sys

for line in sys.stdin:
    key, val = line.strip()[1:-1].split(', ')
    print key.strip('"').strip("'")+'\t'+val
