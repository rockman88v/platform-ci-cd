#!/usr/bin/env bash
set -euo pipefail
: "${BASE_URL:?BASE_URL is required}"
: "${TEST_PATH:?TEST_PATH is required}"
: "${TEST_TIMEOUT:?TEST_TIMEOUT is required}"
script="$GITHUB_WORKSPACE/$TEST_PATH/run.sh"
if [[ ! -f "$script" ]]; then
  echo "Smoke test script not found: $TEST_PATH/run.sh" >&2
  exit 1
fi
timeout --foreground "$TEST_TIMEOUT" bash "$script"
