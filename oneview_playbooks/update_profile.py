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
profile_number =int(sys.argv[1])
scope_name = str(sys.argv[2])
profile_name_list = []
profile_uri_list = []
config = try_load_from_file(config,"oneview_config.json")
oneview_client = OneViewClient(config)

def get_scope_uri(scope_name):
    if scope_name:
        scope_response = oneview_client.scopes.get_by_name(scope_name)
        scope_uri = scope_response['uri']
        return scope_uri

def get_server_with_scope(scope_uri):
    server_response = oneview_client.server_hardware.get_all(filter="\"scopeUris=\'"+scope_uri+"\'\"")
    for server in server_response:
        if (server['serverProfileUri']) :
            profile_uri_list.append(server['serverProfileUri'])

def get_all_profiles(profile_uri_list):
    profile_count = 0
    if profile_uri_list:
        for uri in profile_uri_list: 
            profile_response = oneview_client.server_profiles.get(uri)
            if (not (profile_response['osDeploymentSettings'])) and (profile_count < profile_number):
                profile_count = profile_count + 1
                profile_name_list.append(profile_response['name'])
        print(profile_name_list)

scope_uri = get_scope_uri(scope_name)
get_server_with_scope(scope_uri)
get_all_profiles(profile_uri_list)
