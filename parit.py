#!/usr/bin/env python
import argparse
import json
import os
from pylatex import Command, Document, NewLine, NoEscape
import random
import scraper
import string
import sys

LINE_LENGTH = 70

# Takes a sentence in the form of a string and splits it into its words with all punctuation removed.
def process_input(line):
  line = line.translate(string.maketrans("/"," "), string.punctuation)
  return line.split()

class Letter(object):
  def __init__(self, sender, address, sentences, posting):
    self.body = []
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
    languages = []
    for word in process_input(self.posting.get('required_skills')):
      key = word.lower()
      if key in self.sentences:
        languages.append(word)
        self.body.append(self.select_sentence(key))

    last_lang = languages.pop()
    opening = 'Your job posting indicated that you are looking for someone who is skilled in ' + ', '.join(languages) + ' and ' + last_lang + '.'
    return opening + ' '.join(self.body)

  def write(self):
    with open(os.path.expanduser('~/.config/parit/opening'), 'r') as f:
        opening = f.read().replace('\n', ' ').replace('$organization', self.posting['organization'])
    with open(os.path.expanduser('~/.config/parit/closing'), 'r') as f:
        closing = f.read().replace('\n', ' ')

    pdf_name = 'pdfs/{0}_{1}'.format(self.posting['organization'], self.posting['job_title']).replace(' ', '_').lower()

    employer_address = '{0}\n{1}\n{2} {3} {4}'.format(
      self.posting.get('organization'),
      self.posting.get('job__address_line_one'),
      self.posting.get('job__city'),
      self.posting.get('job__province__state'),
      self.posting['job__postal_code__zip_code_xx_x'])
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
    output.append(opening + self.write_body())
    output.append(NewLine())
    output.append(NewLine())
    output.append(closing)
    output.append(Command('closing', 'Sincerely,'))
    output.append(Command('end', 'letter'))
    output.generate_pdf(pdf_name)

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
  parser.add_argument('-P', '--posting-id', help='Waterloo Works job posting Id')
  args = parser.parse_args()

  try:
    config_path = os.path.expanduser(args.config)
    config = json.loads(open(config_path).read())
  except IOError:
    config = {}

  try:
    sentence_file = args.sentence_file or config.get('sentence_file') or '~/.config/parit/sentences.json'
    sentences = json.loads(open(os.path.expanduser(sentence_file)).read())
  except IOError:
    sys.exit("You must provide a sentences file")

  sender = args.sender or config.get('sender') or sys.exit('You must provide a sender name in either your config or an arg')

  creds_path = os.path.expanduser(args.credentials)
  credentials = json.loads(open(creds_path).read())
  session = scraper.login_cas_waterloo_works(credentials.get('username'), credentials.get('password'))
  posting = scraper.get_posting(session, args.posting_id) or scraper.get_postings(session, args.term)[0]

  letter = Letter(sender, config.get('address').split('/'), sentences, posting)
  letter.write()

if __name__ == "__main__":
  main()
