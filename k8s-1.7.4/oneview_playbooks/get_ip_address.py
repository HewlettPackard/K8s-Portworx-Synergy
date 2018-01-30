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

with open('oscustom_attribute.json','r') as file_data:
    json_data = json.load(file_data) 



server_name_list=[]
ip_list=[]



def get_ip(response):
    file = open('ipaddress.txt',"w+")
    for resp in response['results']:
        try:
            if resp['ansible_facts']:
                for osattr in resp['ansible_facts']['server_profile']['osDeploymentSettings']['osCustomAttributes']:
                    if osattr['name'] == 'Team0NIC1.ipaddress':
                        ip = (osattr['value'])
                        file.write(ip + "\n")
        except:
            pass
    file.close()


def power_state(response):
    for profile in response['results']:
        try:
            if profile['ansible_facts']:
                name = profile['ansible_facts']['server_hardware']['name'].encode("utf-8")
                server_name_list.append(name)
        except:
            pass
    if server_name_list:
        print(server_name_list)



get_ip(json_data)
power_state(json_data)

            
    


               
				
                       





















#if __name__ == '__main__':
#    import sys
#    get_ip(sys.argv)
  
