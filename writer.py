#!/usr/bin/env python
import sys

input = []
if (len(sys.argv) > 1):
  input = sys.argv[1].split()
else:
  with open('input.txt') as f:
    for line in f:
      input = input + line.split()

print input
