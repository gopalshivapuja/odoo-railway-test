# Odoo Railway Ownership Repo

This repository turns a Railway one-click Odoo deployment into a GitHub-owned, CI-guarded, auto-deployed workflow.

## Repository Layout
- `custom_addons/` custom Odoo modules
- `config/odoo.conf` Odoo runtime config
- `scripts/` XML-RPC automation, backups, smoke checks
- `assets/` static assets used by scripts
- `docs/operations.md` rollback and cutover runbook
- `.github/workflows/ci.yml` CI checks

## Security First
The scripts use environment variables; no credentials should be hardcoded.

Required env vars for XML-RPC scripts:
- `ODOO_URL`
- `ODOO_DB`
- `ODOO_USERNAME`
- `ODOO_PASSWORD`

Copy `.env.example` locally and set values.

## Local Run (Docker)
```bash
docker compose up --build
```

## Script Usage
```bash
python3 scripts/install_modules.py
python3 scripts/configure_branding.py
python3 scripts/setup_menus.py
python3 scripts/seed_content.py
python3 scripts/verify_install.py
python3 scripts/build_website.py
```

## Backup Commands
```bash
DATABASE_PUBLIC_URL='<postgres url>' scripts/backup_db.sh
scripts/backup_filestore.sh
```

## Suggested Git Flow
1. Work on `feature/*` branches.
2. Open PR to `main`.
3. CI must pass.
4. Merge to `main` triggers Railway auto-deploy.

## Railway CD Setup
1. Link this repo to the Railway Odoo service.
2. Set deploy branch to `main`.
3. Keep required environment variables in Railway.
4. Confirm volume remains mounted at `/var/lib/odoo`.
