#!/bin/zsh
set -euo pipefail

NODE_BIN="/usr/local/opt/node@22/bin/node"
OPENCLAW_ENTRY="/usr/local/lib/node_modules/openclaw/dist/index.js"
GUARD_SCRIPT="/Users/krazeerastagroup/.openclaw/workspace/scripts/openclaw-config-guard.mjs"
ENV_FILE="$HOME/.openclaw/.env"
LOG_DIR="$HOME/.openclaw/logs"
mkdir -p "$LOG_DIR"

if ! "$NODE_BIN" "$GUARD_SCRIPT" >> "$LOG_DIR/config-guard.log" 2>> "$LOG_DIR/config-guard.err.log"; then
  echo "[openclaw-gateway-wrapper] Config guard blocked startup. See ~/.openclaw/state/config-guard/last-failure.txt" >> "$LOG_DIR/config-guard.err.log"
  exit 1
fi

if [[ -f "$ENV_FILE" ]]; then
  set -a
  source "$ENV_FILE"
  set +a
fi

exec "$NODE_BIN" "$OPENCLAW_ENTRY" gateway --port 18789
