#!/usr/bin/env python
import sys
import string

LINE_LENGTH = 70

input = []
if (len(sys.argv) > 1):
  input = sys.argv[1].split()
else:
  with open('input.txt') as f:
    for line in f:
      for word in line.split():
        word = word.translate(string.maketrans("",""), string.punctuation)
        input.append(word.lower())

words = {}
with open('words.txt') as f:
  for line in f:
    pair = line.split('\\')
    words[pair[0]] = pair[1]

letter = ""
line = ""
for word in input:
  if word in words:
    line += words[word]
    
    if len(line) > LINE_LENGTH:
      letter += line
      letter += "\n"

letter += "Sincerely,\nDavid Loukidelis\n"
print letter
