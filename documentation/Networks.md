
# Networks Folder

## Resources
|Name|Type|Description|
|---|---|---|
|**google_compute_subnetwork.subnet**|resource|Main subnet used for the VM instance and K8s cluster.|
|**google_compute_firewall.firewall**|resource|Firewall used to controll access to cloud resources.Allows connections on three TCP ports: 80, 443, 22 from IP adressess defined in **ip_public_workers** variable.|

## Required variables (infrastructure/dev/common.tfvars)
|Name|Type|Description|
|---|---|---|
|**ip_public_workers**|variable|List of IP adressess allowed to connect to VM and K8s cluster|
|**env**|variable|Environment (dev/qa/prod)|
|**project**|variable|Name of GCP project|
|**region**|variable|Region of cloud resources (e.g.: "europe-central2")|

## Outputs

|Name|Type|Description|
|---|---|---|
|**subnet_name**|output|GCP name of created subnet|


