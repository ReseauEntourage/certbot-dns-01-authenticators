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
    print("No record found")
    exit(0)
else:
    print("Failed to look for existing _acme-challenge record")
    response.raise_for_status()
    exit(1)

quoted_challenge = '"{}"'.format(certbot_validation)

if quoted_challenge in record["rrset_values"] == False:
    print("This challenge is not in the record")
    exit(0)

updated_challenges = list(record["rrset_values"])
updated_challenges.remove(quoted_challenge)

if len(updated_challenges) == 0:
    print("No challenges left, deleting entry")
    response = requests.delete(challenges_href, headers=headers)
else:
    print(str(len(updated_challenges)) + " challenges left, updating entry")
    updated_record = {
      "rrset_ttl": 300,
      "rrset_values": updated_challenges
    }
    response = requests.put(challenges_href, headers=headers, json=updated_record)

if (response.ok):
    print("all good, entry deleted")
    #pp.pprint(response.content)
else:
    print("something went wrong")
    pp.pprint(response.content)
    response.raise_for_status()
    exit(1)
