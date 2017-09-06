#!/usr/bin/env python
import argparse
import json
import os
import random
import string
import sys

LINE_LENGTH = 70

# Takes a sentence in the form of a string and splits it into its words with all punctuation removed.
def process_input(line):
  out = []
  for word in line.split():
    word = word.translate(string.maketrans("",""), string.punctuation)
    out.append(word.lower())
  return out

class Letter(object):
  def __init__(self, recipient, sentences, posting, employer):
    self.recipient = recipient
    self.sentences = sentences
    self.posting = posting
    self.employer = employer

  def select_sentence(self, word):
    sentence = self.sentences[word]
    if isinstance(sentence, basestring):
      return sentence
    else:
      index = int(random.uniform(0, len(sentence)))
      return sentence[index]

  def write_body(self):
    letter = ''
    line = ''
    with open(os.path.expanduser(self.posting)) as f:
      for l in f:
        for word in process_input(l):
          if word in self.sentences:
            line += self.select_sentence(word)
            letter += line
            if len(line) > LINE_LENGTH:
              letter += "\n"
              line = ''
    letter += '\nSincerely,\nDavid Loukidelis\n'
    return letter

  def write(self):
    body = self.write_body()
    print "Dear {0},\n\n{1}".format(self.recipient, body)

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
  employer = args.employer or config.get('employer')
  if manager:
    recipient = manager
  elif employer:
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

  letter = Letter(recipient, sentences, args.posting, employer)
  letter.write()

if __name__ == "__main__":
  main()
