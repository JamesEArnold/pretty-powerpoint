# Terraform configuration for serverless presentation generator.

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    # Backend configuration will be provided via -backend-config
    # during terraform init
  }
}

variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "presentation-generator"
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}
