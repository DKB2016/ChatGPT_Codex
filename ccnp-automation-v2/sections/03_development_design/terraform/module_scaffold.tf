# Section 03 placeholder:
# Build a reusable module with variable validation and outputs.

variable "device_name" {
  type        = string
  description = "Lab device logical name"
}

output "module_ready" {
  value = "Implement resources for ${var.device_name}"
}
