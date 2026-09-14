terraform {
  required_version = ">= 1.16.0"

  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}

provider "local" {}

resource "local_file" "aiopshub_info" {
  filename = "${path.module}/aiopshub-info.txt"

  content = <<-EOT
    AIOpsHub Terraform Test

    Project: AIOpsHub
    Environment: development
    Purpose: Terraform learning and validation
  EOT
}