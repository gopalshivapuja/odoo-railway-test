#!/usr/bin/env bash
set -euo pipefail

# Uses Postgres 16 pg_dump via Docker to avoid local version mismatches.
: "${DATABASE_PUBLIC_URL:?DATABASE_PUBLIC_URL is required}"

mkdir -p backups
OUT="backups/railway-production-$(date +%Y%m%d-%H%M%S).dump"

echo "Creating DB backup at ${OUT}"
docker run --rm \
  -v "$PWD/backups:/backups" \
  postgres:16 \
  pg_dump "$DATABASE_PUBLIC_URL" -Fc -f "/backups/$(basename "$OUT")"

echo "Backup complete: $OUT"
