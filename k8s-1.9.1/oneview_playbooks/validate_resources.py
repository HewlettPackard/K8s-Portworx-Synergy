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
from pprint import pprint
import sys


config = {
    "ip": "",
    "credentials": {
        "userName": "",
        "password": ""
    }
}

config_path = sys.argv[1]
config = try_load_from_file(config,config_path)
oneview_client = OneViewClient(config)

image_streamer_client = oneview_client.create_image_streamer_client()

validation_dict = {}
validation_result = "True"
 
resource_names_dict = {}
resource_names_dict['scope'] = sys.argv[2]
resource_names_dict['deployment_plan'] = sys.argv[3]
resource_names_dict['deploy_network'] = sys.argv[4]
resource_names_dict['mgmt_network'] = sys.argv[5]

def validate_scope():
    scope_resp = oneview_client.scopes.get_by_name(resource_names_dict['scope'])
    if scope_resp != None:
        validation_dict['scope'] = True
    elif scope_resp == None:
        validation_dict['scope'] = False

def validate_dp():
    dp_resp = oneview_client.os_deployment_plans.get_by_name(resource_names_dict['deployment_plan'])
    if dp_resp != None:
        validation_dict['deployment_plan'] = True
    elif dp_resp == None:
        validation_dict['deployment_plan'] = False

def validate_deploy_net():
    conn_resp = oneview_client.ethernet_networks.get_by('name',resource_names_dict['deploy_network'])
    if conn_resp != []:
        validation_dict['deploy_network'] = True
    elif conn_resp == []:
        validation_dict['deploy_network'] = False

def validate_mgmt_net():
    conn_resp = oneview_client.ethernet_networks.get_by('name', resource_names_dict['mgmt_network'])
    if conn_resp != []:
        validation_dict['mgmt_network'] = True
    elif conn_resp == []:
        validation_dict['mgmt_network'] = False

def main():
    validate_scope()
    validate_dp()
    validate_deploy_net()
    validate_mgmt_net()
    validation_result = ""
    for key, value in validation_dict.items():
        if value == True:
            print(key+" validation successfull!")
        elif value == False:
            print(key+" "+"'"+resource_names_dict[key]+"'"+" not found!")
            validation_result = "Failed"
    if validation_result == "Failed":
        exit(1)
if __name__ == "__main__":
    sys.exit(main())
