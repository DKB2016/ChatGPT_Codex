variable "username" {
  type = string
}

variable "password" {
  type      = string
  sensitive = true
}

variable "url" {
  type = string
}
