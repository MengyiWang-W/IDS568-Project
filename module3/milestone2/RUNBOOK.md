## 1. Dependency Pinning Strategy
All Python dependencies are pinned to exact versions in:
app/requirements.txt
Example:
fastapi==0.110.0
uvicorn==0.29.0
pytest==8.0.0
httpx==0.27.0

Pinning ensures:
Reproducible builds
CI consistency
Protection against upstream breaking changes
Environment parity between local development and CI/CD
Stable Docker layer caching

In CI, dependencies are installed using:
```bash
pip install -r module3/milestone2/app/requirements.txt
```
This guarantees deterministic behavior across environments.

## 2. Docker Image Optimization
The Dockerfile applies multiple optimization strategies.
a) Slim Base Image
```bash
FROM python:3.11-slim
```
Using a slim image reduces base OS footprint and minimizes attack surface.

b) Multi-Stage Build
The Dockerfile separates:
Builder stage
Runtime stage
Only necessary runtime artifacts are copied into the final image.
This prevents development dependencies and build tools from being included in production.

c) No Cache Installation
```bash
pip install --no-cache-dir -r requirements.txt
```
Prevents pip cache files from being stored in the image, reducing layer size.

d) .dockerignore Usage
The .dockerignore file excludes unnecessary files such as:
.git
__pycache__
tests
local artifacts
This reduces Docker build context size and improves build performance.

## Image Size Optimization Results
Measured using:docker images
Results:
Single-stage image size: 232MB
Multi-stage image size: 213MB
Size reduction: 8%
Although the reduction is moderate, this is expected because:
Both builds use python:3.11-slim
No heavy build tools were installed in the single-stage version
The application footprint is minimal
The optimization confirms that multi-stage builds reduce unnecessary layers and runtime size.

## 3. Security Considerations
The container design follows basic container security best practices:
Minimal base image (python:3.11-slim)
No unnecessary OS packages installed
No hard-coded secrets in source code
Dependencies pinned to reduce supply-chain risks
Reduced runtime surface area
Additional production-level enhancements (future improvements):
Run container as non-root user
Add vulnerability scanning (e.g., Trivy)
Implement runtime resource limits

## 4. CI/CD Workflow Explanation
The GitHub Actions workflow performs:
Checkout repository
Set up Python 3.11
Install pinned dependencies
Run pytest
Log in to Docker Hub
Build Docker image
Push image to Docker registry
Trigger Condition
on:
  push:
    tags:
      - "v*"

This ensures only semantic version tags trigger container builds.
Example:
git tag v1.0.36
git push origin v1.0.36

CI Guarantees
Tests must pass before image build
Broken code cannot be deployed
Every tagged release produces a traceable container version
Automated publishing to registry

## 5. Versioning Strategy
Semantic Versioning is used:
MAJOR.MINOR.PATCH

Examples:
v1.0.0 → Initial stable release
v1.1.0 → Feature addition
v1.1.1 → Bug fix
Each semantic version tag triggers:
CI validation
Docker image build
Registry publishing
Final submission tag:m2-submission

Created using:
git tag m2-submission
git push --tags
This ensures reproducibility and traceable grading state.

## 6. Troubleshooting Guide
Issue 1: CI fails but works locally
Possible causes:
Missing dependency
Incorrect PYTHONPATH
Python version mismatch

Solutions:
Ensure dependencies are pinned
Confirm __init__.py exists in app/
Match local Python version with CI (3.11)
Run pytest -v locally before pushing
Issue 2: Docker image fails to build

Possible causes:
Incorrect COPY paths
Missing requirements.txt
Incorrect build context

Solutions:
Verify Dockerfile paths
Ensure build is run from correct directory
Confirm final . is included in docker build command

Issue 3: Docker push fails
Possible causes:
Invalid Docker tag format
Incorrect Docker Hub credentials
Secrets misconfigured in GitHub

Solutions:
Recreate DOCKERHUB_USERNAME secret
Regenerate Docker Hub access token
Verify semantic version tag format

## CI Pipeline Summary
Triggered on semantic version tag push
Executes automated tests
Fails fast on errors
Builds multi-stage Docker image
Publishes versioned container to Docker Hub
Ensures reproducible ML inference deployment