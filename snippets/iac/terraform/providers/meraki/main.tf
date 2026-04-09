terraform {
  required_providers {
    meraki = {
      source  = "cisco-open/meraki"
      version = ">= 0.1.0"
    }
  }
}

provider "meraki" {
  api_key = var.api_key
}

module "branch_vlan_30" {
  source      = "../../modules/meraki_vlan"
  network_id  = var.network_id
  vlan_id     = 30
  name        = "USERS"
  subnet_cidr = "10.30.0.0/24"
  gateway_ip  = "10.30.0.1"
}
