terraform {
  required_providers {
    panos = {
      source  = "PaloAltoNetworks/panos"
      version = ">= 1.11.0"
    }
  }
}

provider "panos" {
  hostname = var.hostname
  username = var.username
  password = var.password
}

module "allow_dns_rule" {
  source      = "../../modules/panos_security_rule"
  rule_name   = "allow-dns-branch"
  source_zone = ["inside"]
  dest_zone   = ["outside"]
  apps        = ["dns"]
  services    = ["application-default"]
}
