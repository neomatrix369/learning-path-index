# Deployment: Infrastructure as code

The scripts in this folder give the ability to provision and manage compute capacity using [AWS Infrastructure]([link to follow]), in order to deploy the docker container and run the app in it. 

In short the scripts does the below:
- [instructions to follow]

**Table of content**
- [Pre-requisites](#pre-requisites)
- [Provisioning Infrastructure using Terraform](#provisioning-infrastructure-using-terraform)
  + [Create infrastructure from the CLI using Terraform](#create-infrastructure-from-the-cli-using-terraform)
  + [Deploy the docker image with the notebooks and libraries](#deploy-the-docker-image-with-the-notebooks-and-libraries)
  + [Destroy infrastructure (cleanup)](#destroy-infrastructure-cleanup)
- [Security](#security)

## Pre-requisites

- [AWS & Relates stuff]
- [Install Terraform](https://learn.hashicorp.com/terraform/getting-started/install.html) (all methods for the various platforms are mentioned)
- Clone this repo and in the right folder:
```bash
$ git clone https://github.com/neomatrix369/learning-path-index/
$ cd learning-path-index
$ cd app/llm-poc-variant-01/deploy/aws
```

For a summary (also helps to verify the steps) of the above steps please see [here](https://www.terraform.io/docs/providers/aws/index.html).

## Provisioning Infrastructure using Terraform

### Create infrastructure from the CLI using Terraform

- Deploy with terraform

```bash
$ terraform init
$ terraform apply -var "ssh_private_key=$(cat <location of your private ssh key>)" --auto-approve
```

The deployment process should end with a list of private/public ip addresses like so:

```bash
Apply complete! Resources: 9 added, 0 changed, 0 destroyed.

Outputs:

instance_private_ips = [
    10.1.nn.m
]
instance_public_ips = [
    1xx.145.174.85
]

```

The public IP addresses are fairly dynamic in nature and could be between any range (example shown above). Please make a note of the Public IP above as it will be needed in the following steps.

### Deploy the docker image with the notebooks and libraries

- use ssh and docker to make that end meet

```bash
$ ./run-docker-container.sh
```

### Recover/retry from failed attempt

- Apply the fix to the configuration or script or both
- And run the below again:

```bash
$ terraform apply -var "ssh_private_key=$(cat <location of your private ssh key>)" --auto-approve
```

### Start clean after a failed attempt (errors encountered)

- Run the below before proceeding:

```bash
$ terraform destroy -var "ssh_private_key=$(cat <location of your private ssh key>)" --auto-approve
$ terraform apply -var "ssh_private_key=$(cat <location of your private ssh key>)" --auto-approve
```


### Destroy infrastructure (cleanup)

- Remove resources or destroy them with terraform

```bash
$ terraform destroy -var "ssh_private_key=$(cat <location of your private ssh key>)" --auto-approve
```

You should see something like this at the end of a successful run:

```text
.
.
.
Destroy complete! Resources: 7 destroyed.
```

### Security

Note that this setup does not take into account establishing a secure `http` i.e. `https` communication between the Jupyter lab instance and the browser. Please beware when using this in your target domain depending on the prerequisites you need to conform to. This example is good for learning and illustration purposes, please do NOT deploy it in production or public facing environments.

---

Go to [Main page](../../README.md)