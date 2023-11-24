terraform {
  required_providers {
    ### AWS: https://registry.terraform.io/providers/hashicorp/aws/latest
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.26.0"
    }
  }
}

provider "aws" {
  region  = "eu-central-1"
  profile = "default"
}