## Change/replace below plan script in image streamer to support 1.9.1
RHEL-7.3-Kubernetes-worker-configure

above plan script will disable:
 - swap
 - skips ca verification ( while joining worker node. Optionally you can modify to pass ca cert hash )

## Steps to capture Golden image.
- Step 1: Deploy Plane RHEL 7.3 OS on one of the HPE Synergy blade using respective Deployment plan.

- Step 2: Login to the OS and Install following packages.
```
	Docker EE 17.06
	Kubernetes v1.7.4
	kernel-devel
```

- Step 3: make sure to chenge --cgroup-driver from **systemd** to **cgroupfs** in **/etc/systemd/system/kubelet.service.d/10-kubeadm.conf**

- Step 4: Delete all temporary files (network scripts or any conf script created) and shutdown the OS.

- Step 5: Navigate to Image Streamer and go to create golden images section.

- Step 6: Create Golden Image by capturing the respective OS volume by using proper Buildplan.

- Step 7: Use the captured Golden Image in the Deployment plan.

## Note:
- Artifact bundle **RHEL-7.3-Kubernetes-Worker-2017-10-10.zip** has following fetature
	1. Only Nic teaming is supported 
	2. Does not configure proxy.
- Artifact bundle **RHEL-7.3-Kubernetes-Worker-2017-08-28.zip** has following fetature
	1. Supports both individual NIC and NIC teaming configuration.
	2. Configures proxy.
	3. Include cluster IP in the custom attribute ProxyExclusionList ( you can specify list of IPs for noproxy )




