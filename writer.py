#!/usr/bin/env python
import sys
import string

LINE_LENGTH = 70

def usage():
  print "Usage: " + sys.argv[0] + " company_name [input_text]"

def process_input( line ):
  out = []
  for word in line.split():
    word = word.translate(string.maketrans("",""), string.punctuation)
    out.append(word.lower())
  return out

company_name = ""
if len(sys.argv) > 1:
  company_name = sys.argv[1]
else:
  usage()
  sys.exit(0)
  
input = []
if (len(sys.argv) > 2):
  input = process_input(sys.argv[2])
else:
  with open('input.txt') as f:
    input = process_input(f.read())

words = {}
with open('words.txt') as f:
  for line in f:
    pair = line.split('\\')
    words[pair[0]] = pair[1]

letter = "Dear Hiring Manager,\n\n"
line = ""
for word in input:
  if word in words:
    line += words[word]
    
    if len(line) > LINE_LENGTH:
      letter += line
      letter += "\n"

letter += "Sincerely,\nDavid Loukidelis\n"
print letter
