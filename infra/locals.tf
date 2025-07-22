locals {
  aws_account_id = "${var.aws_account_id == "" ? data.aws_caller_identity.current.account_id : var.aws_account_id}"
}
locals {
  bucket_name = format("%s-%s", tostring(data.aws_caller_identity.current.account_id),var.project_name)
}