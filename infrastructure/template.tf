# Define AWS provider
provider "aws" {
  region = "us-east-1"
}

# Create Kinesis stream
resource "aws_kinesis_stream" "stream" {
  name             = "stream-name"
  shard_count      = 1
  retention_period = 24
}

# Create IAM role for Lambda function
resource "aws_iam_role" "lambda_role" {
  name = "lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

# Attach policy to IAM role
resource "aws_iam_role_policy_attachment" "lambda_policy" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.lambda_role.name
}

# Create ECR repository
resource "aws_ecr_repository" "repository" {
  name = "repository-name"
}

# Create S3 bucket for model artifacts
resource "aws_s3_bucket" "bucket" {
  bucket = "bucket-name"
}

# Create Lambda function
resource "aws_lambda_function" "function" {
  function_name = "function-name"
  role          = aws_iam_role.lambda_role.arn
  handler       = "index.handler"
  runtime       = "python3.8"
  timeout       = 60

  # Upload function code to ECR repository
  container_image = aws_ecr_repository.repository.repository_url

  # Set environment variables
  environment {
    variables = {
      KINESIS_STREAM_NAME = aws_kinesis_stream.stream.name
      S3_BUCKET_NAME      = aws_s3_bucket.bucket.bucket
    }
  }
}

# Create Kinesis stream event source for Lambda function
resource "aws_lambda_event_source_mapping" "event_source_mapping" {
  event_source_arn = aws_kinesis_stream.stream.arn
  function_name    = aws_lambda_function.function.arn
}
