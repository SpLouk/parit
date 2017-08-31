#!/usr/bin/env python
import argparse
import json
import os
import string
import sys

LINE_LENGTH = 70

def process_input( line ):
  out = []
  for word in line.split():
    word = word.translate(string.maketrans("",""), string.punctuation)
    out.append(word.lower())
  return out

def write_letter():
  company_name = ""

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

def main():
  parser = argparse.ArgumentParser(description='This script will write you a cover letter')
  parser.add_argument('-c', '--config', help='Config file', default='~/.config/letter_writer/config.json', required=False)
  parser.add_argument('-e', '--employer', help='Employer name', required=False)
  parser.add_argument('-m', '--manager', help='Hiring manager name', required=False)
  parser.add_argument('-p', '--posting', help='Job posting for which to tailor letter', required=False)
  parser.add_argument('-s', '--sentence-file', help='Map of words to sentences or lists of sentences from which the writer will make its content', required=False)
  args = parser.parse_args()

  try:
    config_path = os.path.expanduser(args.config)
    config = json.loads(open(config_path).read())
  except IOError:
    config = {}

  manager = args.manager or config.get('manager')
  if manager:
    recipient = manager
  else:
    employer = args.employer or config.get('employer')
    if employer:
      recipient = 'Hiring Manager for {0}'.format(employer)
    else:
      print 'You must provide a hiring manager or an employer name in either your config or script args'
      raise SystemExit
  print recipient
  try:
    sentence_file = args.sentence_file or config.get('sentence_file') or '~/.config/letter_writer/sentences.json'
    sentences = json.loads(open(os.path.expanduser(sentence_file)).read())
  except IOError:
    "You must provide a sentences file"
    raise

if __name__ == "__main__":
  main()
