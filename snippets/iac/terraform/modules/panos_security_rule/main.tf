variable "rule_name" { type = string }
variable "source_zone" { type = list(string) }
variable "dest_zone" { type = list(string) }
variable "apps" { type = list(string) }
variable "services" { type = list(string) }

resource "panos_security_policy" "this" {
  rule {
    name                  = var.rule_name
    source_zones          = var.source_zone
    destination_zones     = var.dest_zone
    applications          = var.apps
    services              = var.services
    action                = "allow"
    log_start             = true
    log_end               = true
  }
}
