#!/usr/bin/env python
import argparse
import json
import os
import random
import scraper
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
  def __init__(self, recipient, sender, sentences, posting, employer):
    self.body = []
    self.recipient = recipient
    self.sender = sender
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

  def write_sentence(self, line):
    for word in line.split():
      if len(self.body[-1]) + len(word) > LINE_LENGTH:
        self.body.append(word)
      elif len(self.body[-1]):
        self.body[-1] += ' ' + word
      else:
        self.body[-1] = word

  def write_body(self):
    self.body = ['']
    for word in process_input(self.posting):
      if word in self.sentences:
        self.write_sentence(self.select_sentence(word))
    self.body.append('\nSincerely,\n{0}\n'.format(self.sender))
    return '\n'.join(self.body)

  def write(self):
    body = self.write_body()
    print "Dear {0},\n\n{1}".format(self.recipient, body)

def main():
  parser = argparse.ArgumentParser(description='This script will write you a cover letter')
  parser.add_argument('-c', '--config', help='Config file', default='~/.config/parit/config.json')
  parser.add_argument('-C', '--credentials', help='Credentials file', default='~/.config/parit/credentials.json')
  parser.add_argument('-e', '--employer', help='Employer name')
  parser.add_argument('-m', '--manager', help='Hiring manager name')
  parser.add_argument('-p', '--posting', help='Job posting for which to tailor letter')
  parser.add_argument('-s', '--sentence-file', help='Map of words to sentences or lists of sentences from which the writer will make its content')
  parser.add_argument('-S', '--sender', help='The sender of the letter (your name)')
  parser.add_argument('-t', '--term', help='Search term for Waterloo Works')
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
    sys.exit('You must provide a hiring manager or an employer name in either your config or an arg')
  try:
    sentence_file = args.sentence_file or config.get('sentence_file') or '~/.config/parit/sentences.json'
    sentences = json.loads(open(os.path.expanduser(sentence_file)).read())
  except IOError:
    sys.exit("You must provide a sentences file")

  sender = args.sender or config.get('sender') or sys.exit('You must provide a sender name in either your config or an arg')

  creds_path = os.path.expanduser(args.credentials)
  credentials = json.loads(open(creds_path).read())
  session = scraper.login_cas_waterloo_works(credentials.get('username'), credentials.get('password'))
  posting = scraper.get_postings(session, args.term)[0]

  letter = Letter(recipient, sender, sentences, posting.get('required_skills'), employer)
  letter.write()

if __name__ == "__main__":
  main()
