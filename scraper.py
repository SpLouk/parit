#!/usr/bin/env python

import json
from lxml import html
import os
import requests

LOGIN_URL = 'https://cas.uwaterloo.ca/cas/login?service=https://waterlooworks.uwaterloo.ca/waterloo.htm'
DASH_URL = 'https://waterlooworks.uwaterloo.ca/myAccount/dashboard.htm'
POSTINGS_URL = "https://waterlooworks.uwaterloo.ca/myAccount/co-op/coop-postings.htm"

def login_cas_waterloo_works(credentials_file):
  credentials = json.loads(open(credentials_file).read())
  payload = {
    'username': credentials.get('username'),
    'password': credentials.get('password'),
    'lt': 'e1s1',
    '_eventId': 'submit'
  }
  session = requests.Session()
  session.get(LOGIN_URL) # sets cookies in session
  session.post(LOGIN_URL, data=payload)
  return session

def print_messages(credentials_file):
  session = login_cas_waterloo_works(credentials_file)
  payload = {
   'action': '_-_-vWhTJA86a4chz0G0FO2Fggr-VLSSkAUQmSteqfXOa1pqs1tzsRrDAG-puLCPLDR3fGeedFNboY9UKCCn8nUykOntUtK_Cvjf4bXru3EFBnQg2qfljL3kaqOTbzGS_Lxi0Thuky2wKZMLMCWZdOKO102DaDHHi11ZzdCWckhaYtiAimFf-wnSjA',
   'itemsPerPage':'100'
  }
  page = session.post(DASH_URL, data=payload)
  tree = html.fromstring(page.content)

  # subjects
  messages = tree.xpath('//table/tbody/tr/td[7]/text()')
  print messages

def print_postings(credentials_file, search_term):
  session = login_cas_waterloo_works(credentials_file)
  payload = {
    'action': '_-_-MluhXCvR0n6jA3vbq7A87AJL7KvOHm7xG2EUvL3M9hTt--LmoKJexZQTg-Hc1tVOY51oqx3B0z0B3XfEwyDWpUF7tglFyshhqUlF8289hLmdQbmUc1EoqRENQ8X4t2kUlbPiyEFZ8M3wFKbiTxpVPfKD9t9X5tanfajsPtE',
    'filter': 'all',
    'widget1Keyword': search_term,
    'filter2': 'exact'
  }
  page = session.post(POSTINGS_URL, data=payload)
  tree = html.fromstring(page.content)
  posting_ids = tree.xpath('//table[@id="postingsTable"]/tbody/tr/td[3]/text()')

  for posting_id in posting_ids:
    payload = {
      'action': '_-_-CZAJhGzDi93Ir5yebC9X2QzZQPKmuf0qAY5WqOitfQhUFJT3pAAHQ8WR_qCCCR0IF9vJt6KnkqRkOUMIbOwOiS9iCc2vioHN55ytvgjL1NnXn2kskxVw3GE6CalJ6PidQrNecI9flFNxn6E3C6mMzw4czSk8ygpnu7FlbiWT_Q',
      'postingId': posting_id
    }
    page = session.post(POSTINGS_URL, data=payload)
    tree = html.fromstring(page.content)
    posting = tree.xpath('//div[@id="postingDiv"]/div/div/table/tbody/tr[17]/td[2]/text()')
    print '--------------------------{0}--------------------------'.format(posting_id)
    for item in posting:
      print item.strip()

if __name__ == '__main__':
  print_messages()
