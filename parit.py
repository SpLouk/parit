#!/usr/bin/env python
import argparse
import json
import os
from pylatex import Command, Document, NewLine, NoEscape
import random
import scraper
import string
import sys

# Takes a sentence in the form of a string and splits it into its words with all punctuation removed.
def process_input(line):
  line = line.translate(string.maketrans("/"," "), string.punctuation.replace('+', ''))
  return line.split()

class Letter(object):
  def __init__(self, opening, closing, sender, address, sentences, posting):
    self.body = []
    self.opening = opening.replace('$organization', posting['organization'])
    self.closing = closing.replace('$organization', posting['organization'])
    self.sender = sender
    self.address = address
    self.sentences = sentences
    self.posting = posting

  def select_sentence(self, word):
    sentence = self.sentences[word]
    if isinstance(sentence, basestring):
      return sentence
    else:
      index = int(random.uniform(0, len(sentence)))
      return sentence[index]

  def write_body(self):
    self.body = ['']
    words = {}
    for word in process_input(self.posting.get('job_responsibilities') + self.posting.get('required_skills')):
      if word.lower() in self.sentences:
        if word in words:
          words[word] += 1
        else:
          words[word] = 1

    for word in sorted(words, key=words.get, reverse=True):
      self.body.append(self.select_sentence(word.lower()))

    return ' '.join(self.body)

  def write(self):

    employer_address = '{0}\n{1}\n{2} {3} {4}'.format(
      self.posting.get('organization'),
      self.posting.get('job__address_line_one'),
      self.posting.get('job__city'),
      self.posting.get('job__province__state'),
      self.posting.get('job__postal_code__zip_code_xx_x'))

    return_address = '{0}\\\\{1} {2} {3}'.format(
      self.address[0],
      self.address[1],
      self.address[2],
      self.address[3])
    output = Document(documentclass='letter')
    output.preamble.append(Command('signature', self.sender))
    output.preamble.append(Command('address', NoEscape(return_address)))
    output.preamble.append(Command('date', NoEscape(r'\today')))
    output.append(Command('begin', ['letter', employer_address]))
    output.append(Command('opening', 'Dear Hiring Manager,'))
    output.append(self.opening + self.write_body())
    output.append(NewLine())
    output.append(NewLine())
    output.append(self.closing)
    output.append(Command('closing', 'Sincerely,'))
    output.append(Command('end', 'letter'))

    filename = '{0}_{1}'.format(self.posting['organization'], ' '.join(process_input(self.posting['job_title']))).replace(' ', '_').lower()
    output.generate_pdf(filename)

def main():
  parser = argparse.ArgumentParser(description='This script will write you a cover letter')
  parser.add_argument('-c', '--config', help=('Directory containing config file (config.json), '
    'sentences file (sentences.json), and credentials file (credentials.json). You must have these '
    'files for the program to run properly. (default: ~/.config/parit/)'),
    default='~/.config/parit/')
  parser.add_argument('-p', '--posting-id', help='Waterloo Works job posting Id')
  parser.add_argument('-t', '--term', help='Search term for Waterloo Works')
  args = parser.parse_args()

  config_path = os.path.expanduser(args.config)
  try:
    with open('{0}/config.json'.format(config_path)) as f:
      config = json.loads(f.read())
  except IOError:
    config = {}

  try:
    with open('{0}/sentences.json'.format(config_path)) as f:
      sentences = json.loads(f.read())
  except IOError:
    sys.exit("You must provide a sentences file")

  sender = config.get('sender') or sys.exit('You must provide a sender name in either your config or an arg')

  try:
    with open('{0}/credentials.json'.format(config_path)) as f:
      credentials = json.loads(f.read())
  except IOError:
    sys.exit("You must provide a credentials file")

  session = scraper.login_cas_waterloo_works(credentials.get('username'), credentials.get('password'))
  postings = [scraper.get_posting(session, args.posting_id)] if args.posting_id else  scraper.get_postings(session, args.term)

  with open(os.path.expanduser('~/.config/parit/opening'), 'r') as f:
      opening = f.read().replace('\n', ' ')
  with open(os.path.expanduser('~/.config/parit/closing'), 'r') as f:
      closing = f.read().replace('\n', ' ')

  for posting in postings:
    print 'Generating cover letter for {0}'.format(posting['organization'])
    letter = Letter(opening, closing, sender, config.get('address').split('/'), sentences, posting)
    letter.write()
    print 'Done!'

if __name__ == "__main__":
  main()
