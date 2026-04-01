# Operations Runbook

## Baseline Inventory
- Odoo image: `odoo:19.0`
- Postgres image: `ghcr.io/railwayapp-templates/postgres-ssl:16`
- Odoo service healthcheck: `/web/health`
- Odoo persistent volume mount: `/var/lib/odoo`
- Postgres persistent volume mount: `/var/lib/postgresql/data`

## Pre-Deployment Backup Steps
1. `railway status --json` and save output to your release notes.
2. Export variables safely: `railway variables --service Odoo --json` and `railway variables --service Postgres --json` to a secure password manager (never commit).
3. DB backup: use `scripts/backup_db.sh` with `DATABASE_PUBLIC_URL`.
4. Filestore backup: use `scripts/backup_filestore.sh`.
5. Verify backup artifacts exist and note timestamps/checksums.

## Rollback Procedure
1. Redeploy previous known-good Git tag from Railway deploy history.
2. Restore DB from the matching dump:
   - drop/recreate target DB
   - `pg_restore --clean --if-exists --no-owner --no-privileges -d <db> <dump_file>`
3. Restore filestore archive back into `/var/lib/odoo/filestore`.
4. Restart Odoo service.
5. Run `scripts/smoke_check.sh`.

## Production Verification Checklist
- `/web/health` returns 200.
- Login works for admin users.
- Homepage + key pages load.
- Contact form submission path works.
- Custom modules appear in Apps and remain installed.
