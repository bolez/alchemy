resource "aws_ecr_repository" "datacontract-tf" {
  name                 = format("%s", var.project_name)
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }
}
