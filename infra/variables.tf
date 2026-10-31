variable "region" {
  type    = string
  default = "ap-northeast-1"
}
variable "image_uri" {
  type        = string
  description = "Container image URI accessible to the task execution role"
}
variable "db_password" {
  type        = string
  sensitive   = true
  description = "Demo database password; stored in Terraform state"
}
variable "allowed_cidr" {
  type        = string
  description = "Your public IPv4 address as CIDR, for example 203.0.113.4/32"
}
