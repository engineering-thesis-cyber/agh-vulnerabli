

# VPC Folder

## Resources
|Name|Type|Description|
|---|---|---|
|**google_compute_network.vpc_network**|resource|Main VPC used to provide with networking capabilities of whole infrastructure.|


## Required variables (infrastructure/dev/common.tfvars)
|Name|Type|Description|
|---|---|---|
|**project**|variable|Name of GCP project|
|**repo_link**|variable|Link to Github repository containing project files|
|**location**|variable|Locationof cloud resources (e.g.: "europe-central2-b")|

## Local variables 
-- Not Applicable --

## Required files (infrastructure/dev/common.tfvars)
-- Not Applicable --

## Outputs
|Name|Type|Description|
|---|---|---|
|**vpc_network_name**|output|Name of VPC|
|**vpc_self_link**|output|The URI of the created resource|

