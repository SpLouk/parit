#!/usr/bin/env python

import json
from lxml import html
import os
import requests

LOGIN_URL = 'https://cas.uwaterloo.ca/cas/login?service=https://waterlooworks.uwaterloo.ca/waterloo.htm'
DASH_URL = 'https://waterlooworks.uwaterloo.ca/myAccount/dashboard.htm'

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

if __name__ == '__main__':
  print_messages()
