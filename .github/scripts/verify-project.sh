#!/usr/bin/env bash
set -euo pipefail

# Ephemeral local database; no production credentials, Copilot token or GitHub token.
test -s backend/pom.xml && test -s backend/.java-version
test -s frontend/package.json && test -s frontend/package-lock.json && test -s frontend/.nvmrc

db=false
cleanup() {
  if [[ "$db" == true ]]; then
    docker compose -f backend/compose.yaml down -v || true
  fi
}
trap cleanup EXIT
if [[ -f backend/compose.yaml ]]; then
  services="$(docker compose -f backend/compose.yaml config --services)"
  if grep -qx database <<< "$services"; then
    db=true
    docker compose -f backend/compose.yaml up -d --wait --wait-timeout 120 database
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
