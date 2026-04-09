variable "name" { type = string }
variable "description" { type = string }
variable "ipv4_addr" { type = string }
variable "ipv4_mask" { type = string }

resource "iosxe_interface_loopback" "this" {
  name        = var.name
  description = var.description
}

resource "iosxe_interface_loopback_ipv4_address" "this" {
  name       = iosxe_interface_loopback.this.name
  ipv4_addr  = var.ipv4_addr
  ipv4_mask  = var.ipv4_mask
  depends_on = [iosxe_interface_loopback.this]
}
