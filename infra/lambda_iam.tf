data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "iam_lambda" {
  name               = format("iam_%s_lambda", var.project_name)
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}


resource "aws_cloudwatch_log_group" "lambda_log" {
  name              = format("/aws/lambda/%s", var.project_name)
  retention_in_days = 14
}


data "aws_iam_policy_document" "lambda_policy" {
  statement {
    sid = "awslog"
    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]

    resources = ["arn:aws:logs:*:*:*"]
  }
  statement {
    sid = "awslambdas3"
    effect = "Allow"

    actions = [
      "s3:GetObject",
      "s3:PutObject",
    ]

    resources = [aws_s3_bucket.project_bucket.arn]
  }

}


resource "aws_iam_policy" "datacontract_lambda_policy" {
  name        = format("%s_lambada_policy", var.project_name)
  path        = "/"
  description = "IAM policy for logging from a lambda"
  policy      = data.aws_iam_policy_document.lambda_policy.json
}

resource "aws_iam_role_policy_attachment" "lambda_attach_policy" {
  role       = aws_iam_role.iam_lambda.name
  policy_arn = aws_iam_policy.datacontract_lambda_policy.arn
}