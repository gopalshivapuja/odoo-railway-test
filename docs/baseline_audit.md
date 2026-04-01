# Baseline Audit (Pre-Migration)

## Local Workspace
- Initial state: loose scripts with no git repository.
- Current state: structured repository with `scripts/`, `config/`, `custom_addons/`, `docs/`, `assets/`.

## Railway Runtime Snapshot
- Project: `Odoo Deployment`
- Environment: `production`
- Odoo service: `Odoo`
- Postgres service: `Postgres`
- Odoo image: `odoo:19.0`
- Postgres image: `postgres-ssl:16`
- Odoo healthcheck: `/web/health`
- Odoo volume mount: `/var/lib/odoo`

## Odoo App Baseline
- Authenticated XML-RPC user ID: `2`
- Base module latest version: `19.0.1.3`
- Installed module count: `166`
- Sample installed modules: `sale_management`, `account`, `crm`, `website`, `purchase`, `project`, `website_sale`, `mass_mailing`

## Security Findings
- Original scripts had hardcoded secrets (URL, DB, username, password).
- Scripts now require environment variables (`ODOO_URL`, `ODOO_DB`, `ODOO_USERNAME`, `ODOO_PASSWORD`).
- Next required action: rotate previously exposed credentials in Railway.

## Known Constraints During Automation
- Local `pg_dump` (v15) mismatched Railway Postgres (v16).
- Docker daemon was unavailable in this environment, so automated DB dump couldn't be executed here.
- Added `scripts/backup_db.sh` and `scripts/backup_filestore.sh` to execute backups in your normal local environment.
