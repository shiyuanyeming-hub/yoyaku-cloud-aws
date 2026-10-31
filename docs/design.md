# AWS Japan Cloud Portfolio — Design

## Goal
A personal portfolio for Japanese cloud infrastructure and AWS application roles. Demonstrate a small business API and the infrastructure lifecycle; do not claim production or employment experience.

## Scope
A simple reservation API supports creation and lookup, detects duplicate time slots, and exposes a health endpoint. Japanese and English documentation explains its usage and trade-offs. Local tests run without an AWS account.

## Architecture
Containerized Python API, deployed on ECS Fargate behind an ALB, with PostgreSQL on RDS. Terraform describes VPC, subnets, security groups, ECS, ALB, logging, and database. Public access is limited to the load balancer; application and database network rules are scoped. Use Tokyo region by default. Choose the simplest network topology that actually enables Fargate image pulls; explain costs and availability trade-offs.

## Delivery and operations
GitHub Actions runs tests and infrastructure checks; deployment requires explicit AWS credentials and is documented separately. Include CloudWatch logging and health checks, a Japanese incident runbook, cost considerations and teardown instructions. Do not commit secrets. Clearly distinguish local checks from actual AWS deployment verification.

## Validation
Test API validation, slot conflicts, and health checks. Validate Terraform when tooling is available. Verify deployment only when an AWS account and permission are available; document any unverified steps.

## Out of scope
Real customer data, payments, production-grade identity, guaranteed availability, multi-region disaster recovery, and simulated performance claims.
