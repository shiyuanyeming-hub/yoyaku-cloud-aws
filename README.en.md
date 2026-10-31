# Yoyaku Cloud — AWS Reservation API

[日本語](README.md)

A personal portfolio project using a Japanese shop reservation scenario to demonstrate AWS infrastructure and backend engineering. It shows daily availability, creates and lists reservations, cancels them, normalizes timestamps to UTC, and prevents duplicate slots using a database unique constraint. This is a demonstration, not a claim of professional or production experience.

## Architecture

An internet-facing ALB accepts traffic only from an explicitly allowed CIDR. ECS Fargate runs a FastAPI container in private subnets; RDS PostgreSQL is private and accepts connections only from the task security group. Terraform also defines a NAT gateway, IAM execution role, Secrets Manager secret and CloudWatch logs. See the diagram in the [Japanese README](README.md).

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000/` for the Japanese demo UI or `/docs` for the API documentation. Local storage uses SQLite. The UI offers hourly slots from 09:00 to 18:00 Japan time; direct API requests accept any timezone-aware timestamp. The demo has no authentication, so anyone with access can see and cancel reservations. Submit `resource`, `customer`, and a timezone-aware `starts_at`; a conflicting slot returns HTTP 409. Equivalent timestamps in different time zones refer to the same slot.

## AWS deployment

Build and push a Linux x86-64 image to an ECR repository separately (on Apple Silicon use `docker build --platform linux/amd64 -t IMAGE_URI .`), then set `TF_VAR_image_uri`, `TF_VAR_allowed_cidr` to your own public IP in CIDR form, and `TF_VAR_db_password`. Run `terraform -chdir=infra init`, `plan`, and `apply`. Use `terraform -chdir=infra output url` to obtain the endpoint. Destroy the stack after use and check remaining ECR images, logs and Secrets Manager deletion status.

This is an HTTP-only unauthenticated demo. Do not submit real personal data. NAT, ALB, Fargate and RDS incur charges; the single NAT, task and database do not provide high availability. Terraform state contains the database password and connection string: keep it out of Git, encrypt it, and restrict access. Destroy deletes the database without a final snapshot. TLS, authentication, backup and production hardening are outside this demo.

CI is configured to run tests, build the container, and validate Terraform. A configuration is not proof of a successful cloud deployment: report only checks actually performed. See [the runbook](docs/runbook.md).

See the [verification record](docs/verification.md) for completed checks and unverified cloud behavior.
