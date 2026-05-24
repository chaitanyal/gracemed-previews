#!/usr/bin/env bash
set -euo pipefail

rm -rf dist
mkdir -p dist

for item in ./*; do
  name="$(basename "$item")"
  case "$name" in
    AGENTS.md|README.md|wrangler.toml|scripts|dist|node_modules)
      continue
      ;;
  esac

  cp -R "$item" dist/
done

find dist -name '.DS_Store' -type f -delete
