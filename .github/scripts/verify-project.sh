#!/usr/bin/env bash
set -euo pipefail

# Ephemeral local database; no production credentials, Copilot token or GitHub token.
for file in backend/pom.xml backend/.java-version frontend/package.json frontend/package-lock.json frontend/.nvmrc; do
  test -s "$file" || { echo "Manifest o file versione mancante: $file"; exit 1; }
done
project="neighborcare-ci-${GITHUB_RUN_ID:-$$}-${GITHUB_RUN_ATTEMPT:-1}"
compose=(docker compose -p "$project" -f backend/compose.yaml)

db=false
cleanup() {
  if [[ "$db" == true ]]; then
    "${compose[@]}" down -v || true
  fi
}
trap cleanup EXIT
if [[ -f backend/compose.yaml ]]; then
  services="$("${compose[@]}" config --services)"
  if grep -qx database <<< "$services"; then
    db=true
    "${compose[@]}" up -d --wait --wait-timeout 120 database
  fi
fi
export NEIGHBORCARE_DB_TESTS="$db"
mvn -B -f backend/pom.xml clean verify -Dneighborcare.integration.database="$db"
npm --prefix frontend ci
npm --prefix frontend run build
mkdir -p frontend/test-results
rm -f frontend/test-results/junit.xml
npm --prefix frontend run test:ci
npm --prefix frontend audit --audit-level=high
python3 "$(dirname "$0")/verify_reports.py"
