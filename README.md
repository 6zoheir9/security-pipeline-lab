A DevSecOps CI/CD pipeline that automatically scans code, dependencies, and container builds for security issues before they reach main.

Every push or pull request triggers four parallel security checks — no code merges without passing them. This repo demonstrates shift-left security: catching problems at commit time instead of after deployment.

What It Does
Job	Tool	Catches
secret-scan	TruffleHog	Leaked credentials (API keys, passwords) — verified-only mode to avoid false positives
sca-scan	Trivy	Known CVEs in dependencies (fails the build on HIGH/CRITICAL)
sast-scan	Semgrep	Vulnerable code patterns (injection flaws, insecure configs) via the p/ci ruleset
sbom-generate	Trivy	Generates a Software Bill of Materials (SPDX JSON) as a build artifact

All four run on every push and pull_request targeting main/master, defined in .github/workflows/ci.yml.

Architecture
Push / PR to main
        │
        ├──▶ secret-scan   (TruffleHog)
        ├──▶ sca-scan      (Trivy — dependency CVEs)
        ├──▶ sast-scan     (Semgrep — code patterns)
        └──▶ sbom-generate (Trivy — SBOM artifact)
        │
   All must pass ──▶ merge allowed

The target application (app/) is a minimal Flask app used purely as a scan target — not a production app.

Supply Chain Hardening
Docker base image is pinned by SHA digest, not a floating tag (python:3.11-slim@sha256:...)
Container runs as a non-root user
actions/checkout pinned by SHA where hardened (in progress across all jobs — see Known Issues)
Running Locally
bash
# Build and run the app
docker build -t security-pipeline-lab .
docker run -p 5000:5000 security-pipeline-lab

# Run the scanners locally (optional, mirrors CI)
pip install semgrep
semgrep scan --config p/ci

docker run --rm -v $(pwd):/app aquasec/trivy fs /app
Demo: Catching Real Issues

(In progress) The current app.py passes all checks cleanly. To prove the pipeline actually catches problems — not just runs — a demo branch introduces:

A genuine SSTI vulnerability (user input concatenated directly into a Jinja template string) → caught by sast-scan
A pinned, known-vulnerable dependency version → caught by sca-scan

Results and before/after screenshots go here once the demo branch is pushed.

Known Issues / Next Steps
 Pin actions/checkout to a SHA consistently across all four jobs (currently mixed)
 Pin trufflesecurity/trufflehog@main and aquasecurity/trivy-action@master to a release tag/SHA instead of a floating branch
 Confirm this workflow is set as a required status check in branch protection on main
 (Future) Route findings into an AI-based triage layer for automated prioritization
