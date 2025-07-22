

resource "aws_api_gateway_rest_api" "datacontractapi" {
  name = "momo1"
}   


resource "aws_api_gateway_method" "api_gateway_method" {
  rest_api_id   = aws_api_gateway_rest_api.datacontractapi.id
  resource_id   = aws_api_gateway_rest_api.datacontractapi.root_resource_id
  http_method   = "ANY" # Assuming only one method for simplicity
  authorization = "NONE"
  request_parameters = {
    "method.request.path.proxy" = true
  }
}

resource "aws_api_gateway_integration" "api_getway_lambda" {
  rest_api_id             = aws_api_gateway_rest_api.datacontractapi.id
  resource_id             = aws_api_gateway_rest_api.datacontractapi.root_resource_id
  http_method             = aws_api_gateway_method.api_gateway_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.datacontract_lambda_tf.invoke_arn
  }

resource "aws_api_gateway_method_response" "method_200_response" {
  rest_api_id = aws_api_gateway_rest_api.datacontractapi.id
  resource_id = aws_api_gateway_rest_api.datacontractapi.root_resource_id
  http_method = aws_api_gateway_method.api_gateway_method.http_method
  status_code = "200"
  response_models = {
    "application/json" = "Empty"
} 
depends_on = [aws_api_gateway_method.api_gateway_method]

}
resource "aws_api_gateway_integration_response" "response_200" {
  rest_api_id = aws_api_gateway_rest_api.datacontractapi.id
  resource_id = aws_api_gateway_rest_api.datacontractapi.root_resource_id
  http_method = aws_api_gateway_method.api_gateway_method.http_method
  status_code = aws_api_gateway_method_response.method_200_response.status_code
  depends_on = [aws_api_gateway_integration.api_getway_lambda]

}


resource "aws_api_gateway_resource" "proxy_resource" {
  rest_api_id = aws_api_gateway_rest_api.datacontractapi.id
  parent_id   = aws_api_gateway_rest_api.datacontractapi.root_resource_id
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "api_gateway_method_proxy" {
  rest_api_id   = aws_api_gateway_rest_api.datacontractapi.id
  resource_id   = aws_api_gateway_resource.proxy_resource.id
  http_method   = "ANY" 
  authorization = "NONE"
  request_parameters = {
    "method.request.path.proxy" = true
  }
}
resource "aws_api_gateway_integration" "api_getway_lambda_proxy" {
  rest_api_id             = aws_api_gateway_rest_api.datacontractapi.id
  resource_id             = aws_api_gateway_resource.proxy_resource.id
  http_method             = aws_api_gateway_method.api_gateway_method_proxy.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.datacontract_lambda_tf.invoke_arn

  }

resource "aws_api_gateway_method_response" "method_200_response_proxy" {
  rest_api_id = aws_api_gateway_rest_api.datacontractapi.id
  resource_id = aws_api_gateway_resource.proxy_resource.id
  http_method = aws_api_gateway_method.api_gateway_method_proxy.http_method
  status_code = "200"
  response_models = {
    "application/json" = "Empty"
} 
depends_on = [aws_api_gateway_method.api_gateway_method_proxy]
}
resource "aws_api_gateway_integration_response" "response_200_proxy" {
  rest_api_id = aws_api_gateway_rest_api.datacontractapi.id
  resource_id = aws_api_gateway_resource.proxy_resource.id
  http_method = aws_api_gateway_method.api_gateway_method_proxy.http_method
  status_code = aws_api_gateway_method_response.method_200_response_proxy.status_code
  depends_on = [
    aws_api_gateway_method_response.method_200_response_proxy,
    aws_api_gateway_integration.api_getway_lambda_proxy
  ]


}

resource "aws_api_gateway_deployment" "MyDemoDeployment" {
  depends_on = [ aws_api_gateway_integration.api_getway_lambda, aws_api_gateway_integration.api_getway_lambda_proxy ]
  rest_api_id = aws_api_gateway_rest_api.datacontractapi.id

}