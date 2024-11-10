terraform {
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

provider "google" {
  project = var.project_id
  region  = "europe-west1"
  credentials = file("~/.gcp/service-account-file.json")
}
