

# VM Folder

## Resources
|Name|Type|Description|
|---|---|---|
|**google_container_cluster.primary**|resource|Main GKE Cluster|
|**google_container_node_pool.primary_nodes**|resource|Additional Managed Node Pool for GKE|
|**null_resource.add_context**|resource|Null resource is used to add Kubernetes context, to actor which Applies Terraform code|

## Required variables (infrastructure/dev/common.tfvars)
|Name|Type|Description|
|---|---|---|
|**project**|variable|Name of GCP project|
|**repo_link**|variable|Link to Github repository containing project files|
|**location**|variable|Locationof cloud resources (e.g.: "europe-central2-b")|

## Local variables 
|Name|Type|Description|
|---|---|---|
|**gke_num_nodes**|variable|Count of Kubernetes nodes to create|

## Required files (infrastructure/dev/common.tfvars)
-- Not Applicable --

## Outputs
-- Not Applicable --



