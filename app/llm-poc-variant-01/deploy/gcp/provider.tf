terraform {
  backend "gcs" {
    bucket= "llm-project-sbx-tf-state"
    prefix = "static.tfstate.d"
  }

  required_providers {
    ### GCP: https://registry.terraform.io/providers/hashicorp/google/latest
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

variable "project_id" {
  type = string
  description = "The ID of the GCP project"
}

variable "region" {
  type = string
  description = "The region of the GCP project"
}

variable "zone" {
  type = string
  description = "The zone of the GCP project"
}

provider "google" {
  project = var.project_id
  region  = var.region
}
