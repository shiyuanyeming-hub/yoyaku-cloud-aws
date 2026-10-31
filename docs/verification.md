# 検証記録 / Verification record

## 2026-10-31 — Local

- Python API: `pytest -q` with a disposable PostgreSQL database — 4 tests passed. Covers creation, lookup, timezone normalization, invalid input, and eight concurrent requests competing for one slot (one 201 and seven 409s).
- Browser: submitted the Japanese demo form and repeated the same request; observed success and then a duplicate-slot message.
- Docker: built the image and ran it as the non-root user. Verified `/health`, creation and duplicate 409. An initial startup failed because SQLite could not write to `/app`; the database path was moved to the non-root user's home and the container was rebuilt and retested.
- PostgreSQL integration: ran an isolated PostgreSQL 16 container and API container, created a reservation and confirmed a duplicate expressed in UTC returned 409. Temporary containers were removed.
- Terraform: `terraform init -backend=false` and `terraform validate` passed with AWS provider 5.100.0. This checks configuration validity, not provisioning or runtime behavior.
- AWS deployment: not performed; no AWS account available for testing. RDS, IAM, networking, and Fargate behavior have not been verified in AWS.

The HTTP-only sample is for isolated demonstrations. It has no authentication and must not contain real customer information.
