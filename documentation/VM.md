

# VM Folder

## Resources
|Name|Type|Description|
|---|---|---|
|**google_compute_instance.ubuntu-instance**|resource|Main VM instance used to run the app|
|**time_sleep.wait_60_seconds**|resource|Adds 60 second delay to VM creation (for key transfer script)|
|**null_resource.transfer_key**|resource|Null resource used to execute key transfer script|
|**google_compute_address.external-ip**|resource|Public IP address used for the VM instance|
|**google_compute_project_metadata_item.ssh-key**|resource|Adds public SSH key to VM instance to allow SSH connection using privcate key|

## Required variables (infrastructure/dev/common.tfvars)
|Name|Type|Description|
|---|---|---|
|**project**|variable|Name of GCP project|
|**repo_link**|variable|Link to Github repository containing project files|
|**location**|variable|Locationof cloud resources (e.g.: "europe-central2-b")|

## Local variables 
|Name|Type|Description|
|---|---|---|
|**is_windows**|local|Used to detect underlying os|
|**key_transfer_linux**|local|Linux script to transfer key.json to VM|
|**key_transfer_windows**|local|Windows script to transfer key.json to VM|
|**key_transfer_script**|local|Assigns proper script to variable|

## Required files (infrastructure/dev/common.tfvars)
|Name|Type|Description|
|---|---|---|
|**gcp_ssh**|file|Private SSH key used to connect to VM instance|
|**gcp_ssh.pub**|file|Public SSH key, used in VM instance creation|
|**key.json**|file|File containing credentials to GCP|

## Outputs

|Name|Type|Description|
|---|---|---|
|**instance_ip_address**|output|The public IP address of the newly created instance|



