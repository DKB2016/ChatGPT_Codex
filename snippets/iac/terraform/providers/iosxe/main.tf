terraform {
  required_version = ">= 1.5.0"
  required_providers {
    iosxe = {
      source  = "CiscoDevNet/iosxe"
      version = ">= 0.5.0"
    }
  }
}

provider "iosxe" {
  username = var.username
  password = var.password
  url      = var.url
}

module "loopback_automation" {
  source      = "../../modules/iosxe_interface"
  name        = "Loopback200"
  description = "Created via Terraform"
  ipv4_addr   = "10.200.200.1"
  ipv4_mask   = "255.255.255.255"
}
