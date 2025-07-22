
data "aws_caller_identity" "current" {}
data "aws_region" "current_region" {}

output "account_id" {
  value = data.aws_caller_identity.current.account_id
}

output "account_region" {
  value = data.aws_region.current_region.name
}

output "caller_user" {
  value = data.aws_caller_identity.current.user_id
}

data "aws_ecr_image" "datacontract_image" {
    repository_name = "datacontract_image"
    image_tag       = "latest"
}

data "aws_lambda_function" "lambda_function" {
function_name = format("%s_lambda_tf", var.project_name)
depends_on = [ aws_lambda_function.datacontract_lambda_tf ]
}

output "aws_lambda_function" {
  value = format("%s/%s",data.aws_lambda_function.lambda_function.arn, data.aws_lambda_function.lambda_function.function_name)
}