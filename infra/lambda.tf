

resource "aws_lambda_function" "datacontract_lambda_tf" {

  function_name = format("%s_lambda_tf", var.project_name)
  role          = aws_iam_role.iam_lambda.arn
  package_type  = "Image"
  image_uri     = format("%s:latest", aws_ecr_repository.memory-tf.repository_url)
  depends_on = [
    # aws_iam_role_policy_attachment.lambda_attach_policy,
    aws_cloudwatch_log_group.lambda_log,
    aws_ecr_repository.datacontract-tf,
  ]
}


resource "aws_lambda_function_url" "lambda_function_url" {
  function_name      = aws_lambda_function.datacontract_lambda_tf.function_name
  authorization_type = "NONE"

  cors {
    allow_credentials = false
    allow_origins     = ["*"]

  }
}


resource "aws_lambda_permission" "apigw_lambda" {
  statement_id  = "AllowAPIgatewayInvokation"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.datacontract_lambda_tf.function_name
  principal     = "apigateway.amazonaws.com"

  # More: http://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-control-access-using-iam-policies-to-invoke-api.html
  # source_arn = "arn:aws:execute-api:${data.aws_region.current_region.name}:${var.aws_account_id}:${aws_api_gateway_rest_api.memoryapi.id}/*/*/"
  source_arn = "arn:aws:execute-api:${data.aws_region.current_region.name}:${data.aws_caller_identity.current.account_id
  }:${aws_api_gateway_rest_api.datacontractapi.id}/*/*/"
}
resource "aws_lambda_permission" "apigw_lambda_sub" {
  statement_id  = "AllowAPIgatewayInvokationSub"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.datacontract_lambda_tf.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "arn:aws:execute-api:${data.aws_region.current_region.name}:${data.aws_caller_identity.current.account_id
  }:${aws_api_gateway_rest_api.datacontractapi.id}/*/*/*"
}
