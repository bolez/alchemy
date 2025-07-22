resource "aws_s3_bucket" "project_bucket" {
  bucket = format("%s-media",local.bucket_name)
  tags = {
    Name        = "Environmanet"
    Environment = var.environmanet
  }
}
resource "aws_s3_bucket_public_access_block" "bucket_access_policy" {
  bucket = aws_s3_bucket.project_bucket.id
  block_public_acls       = false
  block_public_policy     = false
#   ignore_public_acls      = false
#   restrict_public_buckets = false
}

resource "aws_s3_object" "datacontract_files" {
  bucket = aws_s3_bucket.project_bucket.id
  key    = "datacontract_files/"
}
data "aws_iam_policy_document" "allow_datacontract_files_policy" {
  statement {
    principals {
      type        = "AWS"
      identifiers = ["*"]
    }

    actions = [
      "s3:GetObject",
      "s3:ListBucket",
    ]

    resources = [
      aws_s3_bucket.project_bucket.arn,
      "${aws_s3_bucket.project_bucket.arn}/datacontract_files/*",
    ]
  }
}
resource "aws_s3_bucket_policy" "allow_datacontract_files" {
  bucket = aws_s3_bucket.project_bucket.id
  policy = data.aws_iam_policy_document.allow_datacontract_files_policy.json
}
output "s3_bucket" {
  value = aws_s3_bucket.project_bucket.arn

}