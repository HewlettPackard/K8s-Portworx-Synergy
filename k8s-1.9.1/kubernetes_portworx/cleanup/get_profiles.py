###
# (C) Copyright (2012-2017) Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###

#!/usr/bin/env python
import json
from config_loader import try_load_from_file
from hpOneView.exceptions import HPOneViewException
from hpOneView.oneview_client import OneViewClient
import sys


config = {
    "ip": "",
    "credentials": {
        "userName": "",
        "password": ""
    }
}

config_path =sys.argv[1]

config = try_load_from_file(config,config_path)
# Once you get updated oneview_ansible library for api_version 600 comment the line below
config['api_version'] = 600
oneview_client = OneViewClient(config)

hostname_profile_dict = {}

def get_hostname_profile_dict():
    server_profiles = oneview_client.server_profiles.get_all()
    scopes_profile_dict = {}
    
    for profile in server_profiles:
        if (profile['osDeploymentSettings']) is not None :
            for attribute in profile['osDeploymentSettings']['osCustomAttributes']:
                if attribute['name'] == 'ServerFQDN':
                    hostname_profile_dict[attribute['value']] = profile['name']
    print(hostname_profile_dict)

get_hostname_profile_dict()

