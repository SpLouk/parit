#!/usr/bin/env python
import argparse
import os
from pylatex import Command, Document, NewLine, NoEscape
import random
import scraper
import string
import sys
import yaml

# Takes a sentence in the form of a string and splits it into its words with all punctuation removed.
def process_input(line):
    line = line.translate(string.maketrans("/"," "), string.punctuation.replace('+', ''))
    return line.split()

class Letter(object):
    def __init__(self, config, sentences, posting):
        self.config = config
        self.sentences = sentences
        self.posting = posting
        self.body = []

    def employer_address(self):
        return '{0}{1}{2}{3}{4}{5}'.format(
                ('{0}\n'.format(self.posting.get('organization')) if self.posting.get('organization') else ''),
                ('{0}\n'.format(self.posting.get('address_one')) if self.posting.get('address_one') else ''),
                ('{0}\n'.format(self.posting.get('address_two')) if self.posting.get('address_two') else ''),
                ('{0} '.format(self.posting.get('city')) if self.posting.get('city') else ''),
                ('{0} '.format(self.posting.get('province')) if self.posting.get('province') else ''),
                (self.posting.get('postal_code') if self.posting.get('postal_code') else ''))

    def return_address(self):
        return '{0}{1}{2} {3} {4}'.format(
                ('{0}\\\\'.format(self.config.get('address_one')) if self.config.get('address_one') else ''),
                ('{0}\\\\'.format(self.config.get('address_two')) if self.config.get('address_two') else ''),
                self.config.get('city', ''),
                self.config.get('province', ''),
                self.config.get('postal_code', ''))

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
        opening = self.config['opening'].replace('$organization', self.posting.get('organization'))
        closing = self.config['closing'].replace('$organization', self.posting.get('organization'))
        output = Document(documentclass='letter')
        output.preamble.append(Command('signature', self.config['sender']))
        output.preamble.append(Command('address', NoEscape(self.return_address())))
        output.preamble.append(Command('date', NoEscape(r'\today')))
        output.append(Command('begin', ['letter', self.employer_address()]))
        output.append(Command('opening', 'Dear Hiring Manager,'))
        output.append(opening + self.write_body())
        output.append(NewLine())
        output.append(NewLine())
        output.append(closing)
        output.append(Command('closing', 'Sincerely,'))
        output.append(Command('end', 'letter'))

        filename = '{0}_{1}'.format(self.posting['organization'], ' '.join(process_input(self.posting['job_title']))).replace(' ', '_').lower()
        output.generate_pdf(filename)
        output.generate_tex(filename)

def main():
    parser = argparse.ArgumentParser(description='This script will write you a cover letter')
    parser.add_argument('-c', '--config', help=('Directory containing config file (config.yml), '
        'sentences file (sentences.yml), and credentials file (credentials.yml). You must have these '
        'files for the program to run properly. (default: ~/.config/parit/)'),
        default='~/.config/parit/')
    parser.add_argument('-p', '--posting-id', help='Waterloo Works job posting Id')
    parser.add_argument('-t', '--term', help='Search term for Waterloo Works')
    args = parser.parse_args()

    config_path = os.path.expanduser(args.config)
    try:
        with open('{0}/config.yml'.format(config_path)) as f:
            config = yaml.load(f)
    except IOError:
        config = {}

    try:
        with open('{0}/sentences.yml'.format(config_path)) as f:
            sentences = yaml.load(f)
    except IOError:
        sys.exit("You must provide a sentences file")

    sender = config.get('sender') or sys.exit('You must provide a sender name in either your config or an arg')

    try:
        with open('{0}/credentials.yml'.format(config_path)) as f:
            credentials = yaml.load(f)
    except IOError:
        sys.exit("You must provide a credentials file")

    session = scraper.login_cas_waterloo_works(credentials.get('username'), credentials.get('password'))

    postings = [scraper.get_posting(session, args.posting_id)] if args.posting_id else scraper.get_postings(session, args.term)

    for posting in postings:
        print 'Generating cover letter for {0}'.format(posting['organization'])
        letter = Letter(config, sentences, posting)
        letter.write()
        print 'Done!'

if __name__ == "__main__":
    main()
