# Clean-up nodes
## Steps to be followed.
- step 1:
	Keep **/etc/hosts** updated 
	
- step 2:
    Copy ssh keys to all nodes to be cleaned-up by entering passwords(if not copied before)
    
    ```$ IPlist="<node1_hostname> <node2_hostname> <node3_hostname>"```
	
    ```$ for ip in $IPlist;do ssh-copy-id -i ~/.ssh/id_rsa.pub root@$ip ; done```
	
- step 3:
	Update **/etc/ansible/hosts** file and add all hostnames under the group **[delete-nodes]**
	
- step 4: Update **vars/variables** file

- step 5: Run playbook using the following command
	```$ ansible-playbook -v cleanup.yml```