# HPE Reference Configuration for Kubernetes, Portworx PX-Enterprise on HPE Synergy
This Reference Configuration provides architectural guidance for deploying, scaling, and managing 
stateful cloud-native applications with Kubernetes as a scale-out and efficient container orchestrator and Portworx PX-Enterprise edition as a cloud-native software-defined storage platform on HPE Synergy composable infrastructure. More 
specifically, it shows how to:
•  Deploy Container-as-a-Service (CaaS) and managed container functionality within IT organizations 
using Kubernetes as the orchestration engine
•  Run stateful workloads using Portworx PX-Enterprise as the cloud-native storage platform
•  Automate deployment and scale of an integrated Portworx + Kubernetes platform leveraging HPE 
Synergy strengths in rapid provisioning
using HPE Synergy Image Streamer by orchestrating through Ansible.


### This repo helps in deploying kubernetes stateful pods with portworx on HPE Synergy
- automating setting up kubernetes master HA cluster,
- automating worker nodes provisioning using HPE Synergy OneView
- automating deploying stateful pods using portworx ( storage volume provider for kubernetes )

Automation orchestration is done using ansible

## Pre-requisites
- HPE OneView 3.1 ( tested on 3.1, it should work with 3.0 by passing correct X-API-Version )
  -  basic server profile template should be created
- HPE Synergy Image Streamer for OS deployment
  - RHEL 7.3 Deployment plan
- 3 VMs for k8s master nodes ( in HA )
- Physical nodes (tested with HPE Synergy Blades & i3s) or VMs. 
- Scritp VM ( tested on Linux flavor of VM ) to run the ansible playbooks. Need following packages on the VM
  - Ansible >= 2.4 or above
  - Python >= 2.7.9
  - HPE OneView Python SDK ([Install HPE OneView Python SDK](https://github.com/HewlettPackard/python-hpOneView#installation))
  - HPE OneView Ansible SDK ([Install HPE OneView Ansible SDK](https://github.com/HewlettPackard/oneview-ansible))
  - configure yum to install packages.
  - Add master host IPs to **/etc/ansible/hosts** as shown below:
    ```
     [master-1]
     <master 1 IP>

     [master-2]
     <master 2 IP>

     [master-3]
     <master 3 IP>
     ```
## Software stack

- Synergy Composer v3.1
- Synergy Image Streamer v3.1
- Docker EE 17.06
- Portworx PX 1.2.10
- Kubernetes v1.7.4
- RHEL 7.3

## Steps to bootstrap Kubernetes HA master cluster

- Step 1: On Ansible machine:

    Generate ssh keys using command below (Press Enter for default values)
    
      $ ssh-keygen -t rsa
      
    Copy ssh keys to all nodes by entering passwords
    
    ```$ IPlist="<master1_ip> <master2_ip> <master3_ip>"```
	
    ```$ for ip in $IPlist;do ssh-copy-id -i ~/.ssh/id_rsa.pub root@$ip ; done```
- Step 2: (Optional) Keep snapshots of all 3 masters , If anything goes wrong during kubernetes cluster configuration you can revert it back.
    
- Step 3: Edit the file **./k8s-<version>/kubernetes_portworx/vars/variables.yml** with respective values.
	For creating custom kubernetes token update KUBERNETES_JOIN_TOKEN specified in variables.yml ( to set no expiry for token. K8s default token expirey time is 24 hr). Follow the below link to create your own token and update it.
	https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-token/ 

- Step 4: RUN this for configuring kubernetes HA cluster

    Run boostrap_kubernetes_HA_master_nodes.yml using command below  
	
    ```	$ cd ./k8s-<version>/kubernetes_portworx/ ```
	
	``` $ ansible-playbook -v bootstrap_kubernetes_HA_master_nodes.yml```
## Steps to capture Golden Image.
Follow steps from ([capture Golden Image](https://github.com/prakashmirji/hpe-synergy-portworx-kubernetes/blob/master/imagestreamer/README.md))
## Steps to configure portworx
  Step 1: Make sure that all worker node IPs present under **[worker-nodes]** group in **/etc/ansible/hosts file**.

  Step 2: Edit the yml file **deploy_portworx.yml** with as per your needs. for example specifying drives, network interfaces, etcd..etc.

  Step 3: Run the command below to deploy portworx.

    $ ansible-playbook -v deploy_portworx.yml

## Validation of Synergy and Image streamer for resource availability 

Run the script below with appropriate parameters to validate the resources availability (This is to validate resources before start deploying worker nodes)
	
	 $ python oneview_playbooks/validate_resources.py "<path_to_config>" "<scope_name>" "<dp_name>" "<deploy_network>" "<mgmt_network>" 

## Steps to join Synergy worker nodes to kubernetes cluster

  Follow steps from ([join Synergy worker nodes](https://github.com/prakashmirji/hpe-synergy-portworx-kubernetes/blob/master/oneview_playbooks/Readme.md))
  
## Steps to join VMs as worker nodes  : Commands mentioned in below steps needs to be executed from script VM.

Note: Design and scripts are tested with RHEL 7.3

- Step 1: configure yum to install packages on all the worker nodes.
 
- Step 2: Copy ssh keys to all nodes by entering passwords

	```$ IPlist="<worker1_ip> <worker_ip> <worker3_ip> ..."```
	
	```$ for ip in $IPlist;do ssh-copy-id -i ~/.ssh/id_rsa.pub root@$ip ; done```

- Step 3: Any VM hots which needs to be added as worker nodes , add those worker node IPs under the group **[unconfigured-worker-nodes]** in **/etc/ansible/hosts** ansible script pic those worker node IPs and joins to the kubernetes cluster.

- Step 4: Run the following command to add all VM worker nodes to kubernetes cluster.

	```	$ cd ./vm_worker_node/ ```
	
	```	$ ansible-playbook -v configure_worker_nodes.yml```
  
## high level testing commands
  ```
  export ANSIBLE_LIBRARY=/path/to/oneview-ansible/library
  export ANSIBLE_MODULE_UTILS=/path/to/oneview-ansible/library/module_utils/
  ````
  edit /etc/ansible/hosts
 
  Run following commands

  Bootstapping k8s master nodes
  >ansible-playbook -v bootstrap_kubernetes_HA_master_nodes.yml

  provision synergy nodes with OS
  >ansible-playbook -v update_multiple_server_profile_with_storage.yml
  
  >ansible-playbook -v update_multiple_server_profile_without_storage.yml

  deploy portworx
  >ansible-playbook -v deploy_portworx.yml

  deploy stateful pod
  >ansible-playbook -v deploy_mysql.yml

  View and monitor kubernetes resources at Dashboard at
  https:<cluster_ip>:30000
## Clean-up master nodes
  Revert to the snapshot taken before configuring cluster.
## Clean-up worker nodes
  refer this ([cleanup](https://github.com/prakashmirji/k8s-sy-px/blob/master/k8s-1.9.1/kubernetes_portworx/cleanup/README.md))
## Troubleshooting notes
Few troubleshooting notes based on our testing
- Disable the server secure boot option
- Don’t specify resource limits in the pods spec file ( it is more of docker issue )
- Be mindful about ports ( we spent more effort on troubleshooting issues related to firewall. Easiest ( may not be safe ) option was to disable the firewalld )
- Please make all master nodes and workers have same date/timezone or setup the right ntp in all nodes
