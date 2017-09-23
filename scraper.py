#!/usr/bin/env python

import json
from lxml import html
import os
import requests
import string

LOGIN_URL = 'https://cas.uwaterloo.ca/cas/login?service=https://waterlooworks.uwaterloo.ca/waterloo.htm'
POSTINGS_URL = "https://waterlooworks.uwaterloo.ca/myAccount/co-op/coop-postings.htm"

def login_cas_waterloo_works(username, password):
  payload = {
    'username': username,
    'password': password,
    'lt': 'e1s1',
    '_eventId': 'submit'
  }
  session = requests.Session()
  session.get(LOGIN_URL) # sets cookies in session
  session.post(LOGIN_URL, data=payload)
  return session

def make_key(key):
  return key.translate(string.maketrans(" ","_"), string.punctuation).lower()

def parse_posting(posting):
  # there are malformed unicode characters in the HTML of this page, so we need to process it again and ignore errors
  page = unicode(posting.content, errors='ignore')

  tree = html.fromstring(page)
  posting = {}
  for row in tree.xpath('//div[@id="postingDiv"]/div/div/table/tbody/tr'):
    key = ''.join(row.xpath('td[1]/descendant::text()')).strip()
    val = ''.join(row.xpath('td[2]/descendant::text()')).strip()
    posting[make_key(key)] = val

  return posting


def get_posting(session, posting_id):
  payload = {
    'action': '_-_-CZAJhGzDi93Ir5yebC9X2QzZQPKmuf0qAY5WqOitfQhUFJT3pAAHQ8WR_qCCCR0IF9vJt6KnkqRkOUMIbOwOiS9iCc2vioHN55ytvgjL1NnXn2kskxVw3GE6CalJ6PidQrNecI9flFNxn6E3C6mMzw4czSk8ygpnu7FlbiWT_Q',
    'postingId': posting_id
  }
  return parse_posting(session.post(POSTINGS_URL, data=payload))

def get_postings(session, search_term):
  payload = {
    'action': '_-_-MluhXCvR0n6jA3vbq7A87AJL7KvOHm7xG2EUvL3M9hTt--LmoKJexZQTg-Hc1tVOY51oqx3B0z0B3XfEwyDWpUF7tglFyshhqUlF8289hLmdQbmUc1EoqRENQ8X4t2kUlbPiyEFZ8M3wFKbiTxpVPfKD9t9X5tanfajsPtE',
    'filter': 'all',
    'widget1Keyword': search_term,
    'filter2': 'exact'
  }
  page = session.post(POSTINGS_URL, data=payload)
  tree = html.fromstring(page.content)
  posting_ids = tree.xpath('//table[@id="postingsTable"]/tbody/tr/td[3]/text()')

  postings = []
  for posting_id in posting_ids:
    postings.append(get_posting(session, posting_id))
  return postings
