#!/usr/bin/env python2
import json
import os
import requests
from panda3d.core import *


username = os.environ['ttiUsername']
password = os.environ['ttiPassword']
distribution = ConfigVariableString('distribution', 'dev').getValue()

accountServerEndpoint = ConfigVariableString(
    'account-server-endpoint',
    'https://toontowninfinite.com/api/').getValue()
request = requests.post(
    accountServerEndpoint + 'login/',
    data={'n': username, 'p': password, 'dist': distribution})

try:
    response = json.loads(request.text)
except ValueError:
    print "Couldn't verify account credentials."
else:
    if not response['success']:
        print response['reason']
    else:
        os.environ['TTI_PLAYCOOKIE'] = response['token']

        # Start the game:
        import toontown.toonbase.ClientStart
