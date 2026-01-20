#!/bin/bash

echo "--- RUNNING SECRET SCAN ---"
MSYS_NO_PATHCONV=1 docker run --rm -v "${PWD}:/src" trufflesecurity/trufflehog:latest filesystem /src --fail || exit 1

echo "--- RUNNING SCA SCAN ---"
MSYS_NO_PATHCONV=1 docker run --rm -v "${PWD}:/src" aquasec/trivy:latest fs /src --severity HIGH,CRITICAL --scanners vuln

echo "--- RUNNING SAST SCAN ---"
MSYS_NO_PATHCONV=1 docker run --rm -v "${PWD}:/src" returntocorp/semgrep semgrep scan --config auto /src --error || exit 1

echo "ALL SCANS PASSED!"