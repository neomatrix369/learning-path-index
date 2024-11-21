Guide to setup Terraform Account on GCP - https://gcloud.devoteam.com/blog/a-step-by-step-guide-to-set-up-a-gcp-project-to-start-using-terraform/

Enable IAM Service API https://console.cloud.google.com/apis/api/iamcredentials.googleapis.com/overview?project=kagglex-llm-demo&inv=1&invt=Abho-A

terraform plan --out tf.plan --var-file=project.tfvars

terraform apply "tf.plan"

gcloud compute ssh --project=kagglex-llm-demo --zone=europe-west1-b lpi-llm-cpu-vm

pip install chroma-migrate

## Outputs
Outputs:

network_interface_0_access_config_0_nat_ip = "35.187.8.179"
network_interface_0_network_ip = "10.132.0.2"
self_link = "https://www.googleapis.com/compute/v1/projects/kagglex-llm-demo/zones/europe-west1-b/instances/lpi-cpu-vm"
tags = toset([
  "lpi-sg",
])
