#!/usr/bin/env bash
set -euo pipefail

# Ephemeral local database; no production credentials, Copilot token or GitHub token.
project="neighborcare-ci-${GITHUB_RUN_ID:-$$}-${GITHUB_RUN_ATTEMPT:-1}"
compose=(docker compose -p "$project" -f backend/compose.yaml)
db=false
failed=0
cleanup() {
  if [[ "$db" == true ]]; then
    "${compose[@]}" down -v || true
  fi
}
trap cleanup EXIT
record() {
  printf '%s: %s\n' "$1" "$2"
  if [[ -n "${GITHUB_OUTPUT:-}" ]]; then
    printf '%s=%s\n' "$1" "$2" >> "$GITHUB_OUTPUT"
  fi
}
check() {
  local name="$1"
  shift
  if "$@"; then
    record "$name" success
  else
    record "$name" failure
    failed=1
  fi
}
for file in backend/pom.xml backend/.java-version frontend/package.json frontend/package-lock.json frontend/.nvmrc; do
  test -s "$file" || { echo "Manifest o file versione mancante: $file"; exit 1; }
done
# Do not silently skip PostgreSQL when the service fails to start.
if services="$("${compose[@]}" config --services)" && grep -qx database <<< "$services"; then
  db=true
  check database "${compose[@]}" up -d --wait --wait-timeout 120 database
else
  record database failure
  failed=1
fi
export NEIGHBORCARE_DB_TESTS="$db"
rm -rf backend/target/surefire-reports backend/target/failsafe-reports
rm -f frontend/test-results/junit.xml
check backend mvn -B -f backend/pom.xml clean verify -Dneighborcare.integration.database=true
if npm --prefix frontend ci; then
  record install success
  check frontend_build npm --prefix frontend run build
  mkdir -p frontend/test-results
  check frontend_tests npm --prefix frontend run test:ci
  check audit npm --prefix frontend audit --audit-level=high
else
  record install failure
  record frontend_build skipped
  record frontend_tests skipped
  record audit skipped
  failed=1
fi
check reports python3 "$(dirname "$0")/verify_reports.py"
exit "$failed"
