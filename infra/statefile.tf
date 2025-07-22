terraform {
  backend "s3" {
    bucket         = "455986485846-datacontract"
    key            = "ops/datacontract-state-file.tfstate"
    region         = "us-east-1"
    encrypt        = true
  }
}