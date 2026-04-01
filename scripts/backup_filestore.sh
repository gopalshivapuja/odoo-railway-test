#!/usr/bin/env bash
set -euo pipefail

# Requires Railway CLI auth and a running Odoo service.
# Creates a compressed filestore archive inside the running container.
# You can then move it to persistent storage (S3/GDrive) from Railway shell.

ARCHIVE_PATH="/tmp/odoo-filestore-$(date +%Y%m%d-%H%M%S).tar.gz"

echo "Creating filestore archive inside Odoo service: ${ARCHIVE_PATH}"
railway ssh --service Odoo "tar -czf ${ARCHIVE_PATH} /var/lib/odoo/filestore && ls -lh ${ARCHIVE_PATH}"

echo "Archive created inside service. Copy/upload it before deleting container."
