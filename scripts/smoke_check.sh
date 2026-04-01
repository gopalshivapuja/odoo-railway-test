#!/usr/bin/env bash
set -euo pipefail

: "${ODOO_URL:?ODOO_URL is required}"

for path in /web/health / /web/login; do
  echo "Checking ${ODOO_URL}${path}"
  curl -fsSL "${ODOO_URL}${path}" >/dev/null
  echo "OK: ${path}"
done
