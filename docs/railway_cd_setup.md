# Railway CD Setup

## Connect GitHub Repo
1. Open Railway project `Odoo Deployment`.
2. Select Odoo service.
3. Set source to GitHub repo `gopalshivapuja/odoo-railway-test`.
4. Set auto-deploy branch to `main`.

## Runtime Config
- Keep healthcheck path: `/web/health`
- Keep persistent volume mount: `/var/lib/odoo`
- Keep Postgres service attached and env vars available

## Required Environment Variables
- `ODOO_DATABASE_HOST`
- `ODOO_DATABASE_PORT`
- `ODOO_DATABASE_USER`
- `ODOO_DATABASE_PASSWORD`
- `ODOO_DATABASE_NAME`
- `ODOO_SMTP_HOST`
- `ODOO_SMTP_PORT_NUMBER`
- `ODOO_SMTP_USER`
- `ODOO_SMTP_PASSWORD`
- `ODOO_EMAIL_FROM`

## Post-Connection Verification
1. Trigger deploy from latest `main` commit.
2. Confirm build logs complete successfully.
3. Validate `/web/health` and login.
4. Run `scripts/smoke_check.sh` against public URL.
