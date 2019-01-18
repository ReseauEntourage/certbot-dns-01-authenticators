#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pprint
import requests
import os
import json
from config import *

pp = pprint.PrettyPrinter(indent=4)

certbot_domain = os.environ.get("CERTBOT_DOMAIN")
try:
    certbot_domain
except NameError:
    print("CERTBOT_DOMAIN environment variable is missing, exiting")
    exit(1)

certbot_validation = os.environ.get("CERTBOT_VALIDATION")
try:
    certbot_validation
except NameError:
    print("CERTBOT_VALIDATION environment variable is missing, exiting")
    exit(1)

if livedns_sharing_id == None:
    sharing_param = ""
else:
    sharing_param = "?sharing_id=" + livedns_sharing_id

headers = {
    'X-Api-Key': livedns_apikey,
}

challenges_href = livedns_api + "domains/" + certbot_domain + "/records/_acme-challenge/TXT" + sharing_param

response = requests.get(challenges_href, headers=headers)

if (response.ok):
    record = response.json()
elif response.status_code == requests.codes.not_found:
    record = None
else:
    print("Failed to look for existing _acme-challenge records")
    response.raise_for_status()
    exit(1)

quoted_challenge = '"{}"'.format(certbot_validation)

if record == None:
    print("creating record")
    new_record = {
      "rrset_ttl": 300,
      "rrset_values": [certbot_validation]
    }
    response = requests.post(challenges_href, headers=headers, json=new_record)
elif quoted_challenge in record["rrset_values"]:
    print("this challenge already exists in the record")
    exit(0)
else:
    print("adding new challenge to the existing record")
    updated_record = {
      "rrset_ttl": 300,
      "rrset_values": record["rrset_values"] + [certbot_validation]
    }
    response = requests.put(challenges_href, headers=headers, json=updated_record)

if (response.ok):
    print("all good, entry created")
    #pp.pprint(response.content)
else:
    print("something went wrong")
    pp.pprint(response.content)
    response.raise_for_status()
    exit(1)
