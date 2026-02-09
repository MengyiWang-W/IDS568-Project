## 1. Dependency Pinning Strategy
All Python dependencies are pinned to exact versions in requirements.txt.
Example:
fastapi==0.110.0
uvicorn==0.29.0
pytest==8.0.0
httpx==0.27.0

Pinning ensures:
Reproducible builds
CI consistency
Protection against breaking changes from upstream packages
Environment parity between local and CI/CD

In CI, dependencies are installed using:
pip install -r module3/milestone2/app/requirements.txt

This guarantees consistent behavior across environments.

## 2. Docker Image Optimization
The Dockerfile applies the following optimizations:
a) Slim base image
FROM python:3.11-slim
Using a slim image reduces attack surface and image size.

b) --no-cache-dir flag
pip install --no-cache-dir -r requirements.txt
Prevents pip from storing cache files in the image.

c) .dockerignore usage
The .dockerignore file excludes:
.git
pycache
tests
local files
This reduces build context size.

Image Size
Before optimization: ~1GB (standard Python image)
After optimization: ~200–300MB (slim + cleaned layers)

## 3. Security Considerations
The container is hardened with:
Minimal base image (python:3.11-slim)
No unnecessary OS packages installed
No secret keys stored in code
Dependencies pinned to avoid supply chain attacks

Best practices applied:
Avoid running as root in production (future enhancement)
Do not expose unnecessary ports
Limit attack surface

## 4. CI/CD Workflow Explanation
The GitHub Actions workflow performs the following steps:
Checkout repository
Set up Python environment
Install dependencies
Run pytest
Build Docker image
Push image to container registry

Trigger:
on:
  push:
    tags:
      - "v*.*.*"

This ensures versioned releases trigger image builds.

CI ensures:
Tests must pass before image is built
No broken code is deployed
Reproducible builds

## 5. Versioning Strategy
Semantic Versioning is used:
MAJOR.MINOR.PATCH

Examples:
v1.0.0 → first stable release
v1.1.0 → new feature added
v1.1.1 → bug fix

Final submission tag:
m2-submission

Tags are created using:
git tag m2-submission
git push --tags
This ensures traceable releases.

## 6. Troubleshooting Guide
Issue 1: CI fails but works locally
Cause:
Missing dependency
Incorrect import path
Environment differences

Solution:
Ensure dependencies are pinned
Add __init__.py in app directory
Run pytest locally before pushing

Issue 2: Docker image fails to build
Cause:
Incorrect COPY paths
Missing requirements.txt

Solution:
Verify Dockerfile paths
Ensure context is correct during docker build

Issue 3: Tests fail in GitHub but not locally
Cause:
Python version mismatch
Missing test dependencies

Solution:
Ensure CI Python version matches local version
Install test requirements
End of Runbook.

CI Pipeline Summary
Triggered on semantic tag push
Runs tests before build
Fails fast if tests break
Builds container only after successful validation