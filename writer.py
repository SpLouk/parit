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

def grab_sentence(word, sentences):
  sentence = sentences[word]
  if isinstance(sentence, basestring):
    return sentence
  else:
    return sentence[0]

def write_body(posting, sentences):
  letter = ''
  line = ''
  with open(os.path.expanduser(posting)) as f:
    for l in f:
      for word in process_input(l):
        if word in sentences:
          line += grab_sentence(word, sentences)
          letter += line
          if len(line) > LINE_LENGTH:
            letter += "\n"
            line = ''
  letter += '\nSincerely,\nDavid Loukidelis\n'
  return letter

def main():
  parser = argparse.ArgumentParser(description='This script will write you a cover letter')
  parser.add_argument('-c', '--config', help='Config file', default='~/.config/letter_writer/config.json', required=False)
  parser.add_argument('-e', '--employer', help='Employer name', required=False)
  parser.add_argument('-m', '--manager', help='Hiring manager name', required=False)
  parser.add_argument('-p', '--posting', help='Job posting for which to tailor letter', required=True)
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
  try:
    sentence_file = args.sentence_file or config.get('sentence_file') or '~/.config/letter_writer/sentences.json'
    sentences = json.loads(open(os.path.expanduser(sentence_file)).read())
  except IOError:
    "You must provide a sentences file"
    raise

  body = write_body(args.posting, sentences)
  print "Dear {0},\n{1}".format(recipient, body)

if __name__ == "__main__":
  main()
