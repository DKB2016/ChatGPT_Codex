variable "network_id" { type = string }
variable "vlan_id" { type = number }
variable "name" { type = string }
variable "subnet_cidr" { type = string }
variable "gateway_ip" { type = string }

resource "meraki_networks_appliance_vlans" "this" {
  network_id = var.network_id
  vlan_id    = tostring(var.vlan_id)
  name       = var.name
  subnet     = var.subnet_cidr
  appliance_ip = var.gateway_ip
}
