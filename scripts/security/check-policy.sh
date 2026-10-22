#!/usr/bin/env bash
# Compare against an actual immutable base; never let a PR weaken its own scanner policy.
set -euo pipefail
base=${1:?An immutable PR base is required}
if ! [[ "$base" =~ ^[0-9a-f]{40}$ ]]; then
  printf '%s\n' 'An immutable PR base is required.' >&2
  exit 2
fi
git cat-file -e "$base^{commit}"
changed=$(git diff --name-only "$base" HEAD -- .gitleaks.toml .gitleaksignore .trivyignore .trivyignore.yaml trivy.yaml trivy-secret.yaml)
if [[ -n "$changed" ]]; then
  printf '%s\n' 'Scanner policy changed in this PR; a separate reviewed policy transition is required.' >&2
  exit 1
fi
