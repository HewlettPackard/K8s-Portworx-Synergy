Prerequisites
---------------

- OneView Ansible library 
  https://github.com/HewlettPackard/oneview-ansible
  
- OneView Python SDK
  https://github.com/HewlettPackard/python-hpOneView
  
- Play Books
  1. update_multiple_server_profile_with_storage.yml
  2. update_multiple_server_profile_without_storage.yml
  3. wait_for.yml
  
- Python Files
  1. get_ip_address.py
  2. update_profile.py
  3. config_loader.py
  
- Configuration file
  oneview_config.json
  
- Set Environment Variables File
  set_env_variables  
  
  
Attributes to be set in following files
------------------------------------------
1. In `oneview_config.json` file

	{
		"ip": "10.60.150.10",
		"credentials": {
			"userName": "Administrator",
			"password": "hpent123"
		},
		"api_version": 500,
		"os_custom_attribute_password" : "password"
	}		

		
2. Set following path in `set_env_variables` file		
		
		export ANSIBLE_LIBRARY=/path/to/oneview-ansible/library
		export ANSIBLE_MODULE_UTILS=/path/to/oneview-ansible/library/module_utils/			

	
3. In the play book `update_multiple_server_profile_with_storage.yml` or `update_multiple_server_profile_without_storage.yml`	
		
		
		a. Variables :
		    # number of profiles to be updated
			profile_numbers: 4				
		    # name of the scope for which server profiles has to be updated
			scope_name: "kubeworkergroup1"
		    # networks name
			management_network_name: "Mgmt"
			deployment_network_name: "Deploy"
		    # os deployment plan variables
			os_deployment_plan_name: "RHEL-7.3-Kubernetes-Worker-2017-10-10"
			mgmt_NIC1_connection_id: "1"
			mgmt_NIC1_dhcp: "false"
			mgmt_NIC1_ipv4disable: "false"
			mgmt_NIC1_networkuri: "/rest/ethernet-networks/ce53067d-42c6-4603-aba7-f53df8c2f78c"
			mgmt_NIC1_constraint: "auto"
			mgmt_NIC2_connection_id: "2"
			mgmt_NIC2_dhcp: "true"
			mgmt_NIC2_ipv4disable: "false"
			mgmt_NIC2_networkuri: "/rest/ethernet-networks/ce53067d-42c6-4603-aba7-f53df8c2f78c"
			mgmt_NIC2_constraint: "dhcp"
			nic_teaming: "Yes"
			ntp_server: "10.60.1.123"
			root_password: "password"
			SSH: "Enabled"

		b. OS custom attributes in data :
			osCustomAttributes:
			  -  name: ClusterIP
				 value: "{{ cluster_ip }}"
			  -  name: ClusterJoinToken
				 value: "{{ cluster_join_token }}"
			  -  name: ClusterPort
				 value: "{{ cluster_port }}"
			  -  name: Team0NIC1.connectionid
				 value: "1"
			  -  name: Team0NIC1.dhcp
				 value: "{{ mgmt_NIC1_dhcp }}"
			  -  name: Team0NIC1.ipv4disable
				 value: "{{ mgmt_NIC1_ipv4disable }}"
			  -  name: Team0NIC1.networkuri
				 value: "{{ mgmt_NIC1_networkuri }}"
			  -  name: Team0NIC1.constraint
				 value: "{{ mgmt_NIC1_constraint }}"
			  -  name: Team0NIC2.connectionid
				 value: "2"
			  -  name: Team0NIC2.dhcp
				 value: "{{ mgmt_NIC2_dhcp }}"
			  -  name: Team0NIC2.ipv4disable
				 value: "{{ mgmt_NIC2_ipv4disable }}"
			  -  name: Team0NIC2.networkuri
				 value: "{{ mgmt_NIC2_networkuri }}"
			  -  name: Team0NIC2.constraint
				 value: "{{ mgmt_NIC2_constraint }}"
			  -  name: NtpServer
				 value: "{{ ntp_server }}"
			  -  name: ServerFQDN
				 value: "{{ item }}-Node.cloudra.local"
			  -  name: SSH
				 value: "{{ SSH }}"
			  -  name: NewRootPassword
				 value: "{{ root_password }}"

  
Command to set environment  variables
---------------------------------------

    $ source set_env_variables
        
	
Command to RUN the play book
------------------------------
		
Before running ansible playbook, edit the yaml ( either one of them based on your need ) in the vars section. Especially below fields to specify the number of servers you would to be provisioned and server scope name you have created in the oneview.
		
	profile_numbers: 4
	scope_name: "kubeworkergroup1"		
		
Commands:
			
	$ ansible-playbook -v update_multiple_server_profile_with_storage.yml 
	$ ansible-playbook -v update_multiple_server_profile_without_storage.yml
	

Design considerations
------------------------

- Server profile should exists with or without connections
- Create a Scope/s for list of servers to be part of kubernetes worker nodes ( script takes scope name as one of the input and picks those servers which are marked with scope ) 
- Management network and deployment network is added while updating the server profile/s
	
