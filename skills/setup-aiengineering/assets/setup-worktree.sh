#!/usr/bin/env bash
# Idempotent worktree bootstrap — makes a fresh git worktree / clone buildable.
# Runs on the first session (SessionStart hook in .claude/settings.json) and on demand.
#
# Plain shell on purpose: it installs the toolchain other scripts need, so it must not
# depend on that toolchain itself. Detects the ecosystem from its lockfile/manifest and
# runs the matching install only when dependencies look stale. Never hard-fails — a missing
# tool or failed install prints a WARN and exits 0 so the session can still start.

cd "$(dirname "$0")/.." || exit 0
did_work=0

have() { command -v "$1" >/dev/null 2>&1; }
warn() { echo "WARN: $*" >&2; }

# --- Node ecosystem (pnpm / yarn / npm), picked by lockfile ---------------------------------
if [ -f pnpm-lock.yaml ]; then
  # Compare against pnpm's .modules.yaml marker (rewritten every install), not the dir mtime.
  if [ ! -f node_modules/.modules.yaml ] || [ pnpm-lock.yaml -nt node_modules/.modules.yaml ]; then
    if have pnpm; then pnpm install --frozen-lockfile && did_work=1 || warn "pnpm install failed — run it manually."
    else warn "pnpm not found — install it, then run 'pnpm install'."; fi
  fi
elif [ -f yarn.lock ]; then
  if [ ! -d node_modules ] || [ yarn.lock -nt node_modules ]; then
    if have yarn; then yarn install --frozen-lockfile && did_work=1 || warn "yarn install failed — run it manually."
    else warn "yarn not found — install it, then run 'yarn install'."; fi
  fi
elif [ -f package-lock.json ]; then
  if [ ! -d node_modules ] || [ package-lock.json -nt node_modules ]; then
    if have npm; then npm ci && did_work=1 || warn "npm ci failed — run it manually."
    else warn "npm not found."; fi
  fi
elif [ -f package.json ]; then
  if [ ! -d node_modules ]; then
    if have npm; then npm install && did_work=1 || warn "npm install failed — run it manually."
    else warn "npm not found."; fi
  fi
fi

# --- Python ---------------------------------------------------------------------------------
if [ -f requirements.txt ] && [ ! -d .venv ] && [ ! -d venv ]; then
  if have python3; then
    python3 -m venv .venv && . .venv/bin/activate && python3 -m pip install -r requirements.txt && did_work=1 \
      || warn "python venv/install failed — set it up manually."
  else warn "python3 not found."; fi
elif [ -f pyproject.toml ] && have poetry && [ ! -d .venv ]; then
  poetry install && did_work=1 || warn "poetry install failed — run it manually."
fi

# --- Go / Rust ------------------------------------------------------------------------------
if [ -f go.mod ] && have go; then
  go mod download && did_work=1 || warn "go mod download failed — run it manually."
fi
if [ -f Cargo.toml ] && have cargo; then
  cargo fetch && did_work=1 || warn "cargo fetch failed — run it manually."
fi

# --- Belt-and-suspenders warnings (never fail) ----------------------------------------------
[ -f .env ] || [ -f .env.local ] || [ ! -f .env.example ] || warn "no .env/.env.local — copy .env.example."

[ "$did_work" -eq 1 ] && echo "Workspace ready (installed dependencies)."
exit 0
