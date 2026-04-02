# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

An Odoo 19.0 deployment for the MOAR Advisory website (moaradvisory.com), hosted on Railway. The repo contains a custom Odoo theme module (`theme_moar_advisory`) and Python XML-RPC automation scripts that configure the site content programmatically.

## Local Development

```bash
# Start Odoo + Postgres locally (http://localhost:8069)
docker compose up --build

# Rebuild just the Odoo container after theme changes
docker compose up --build odoo
```

Default local credentials: `odoo`/`odoo` for both DB user and database name.

After container is running, install the theme module via Odoo Apps or:
```bash
python3 scripts/install_theme.py
```

## CI

```bash
ruff check scripts          # Lint Python scripts
python -m compileall scripts  # Compile check
docker build -t odoo-custom:ci .  # Docker build check
```

CI runs on all PRs and pushes to `main` (`.github/workflows/ci.yml`).

## Architecture

### Theme Module (`custom_addons/theme_moar_advisory/`)

A standard Odoo theme module that overrides website templates:
- `views/website_templates.xml` — header/nav overrides (inherits `website.layout`)
- `views/snippets.xml` — custom homepage snippet blocks
- `views/pages.xml` — full page definitions (About, Services, etc.)
- `static/src/scss/theme.scss` — site-wide styling (colors, fonts, layout)
- `static/src/js/header_social.js` — JS for social icons and font loading
- `__manifest__.py` — declares dependencies, data files, and frontend assets

The module depends only on `website`. Version scheme: `19.0.x.y.z`.

### XML-RPC Scripts (`scripts/`)

Python scripts that automate Odoo configuration via XML-RPC. All use `scripts/common.py` for connection setup. Required env vars: `ODOO_URL`, `ODOO_DB`, `ODOO_USERNAME`, `ODOO_PASSWORD`.

Key scripts:
- `rebuild_site.py` (root) — master script that rebuilds the full site content
- `install_modules.py` / `install_theme.py` — module installation
- `configure_branding.py` — company name, logo, colors
- `setup_menus.py` — website navigation menus
- `seed_content.py` / `build_website.py` — page content creation

### Deployment

Merging to `main` triggers Railway auto-deploy. Railway uses the `Dockerfile` (based on `odoo:19.0`) and `config/odoo.conf` for runtime configuration. The config uses env var interpolation for all secrets.

## Key Conventions

- Theme changes go through Odoo's QWeb template inheritance (`t-inherit`, `t-inherit-mode="extension"`), not raw HTML injection.
- Test changes locally with Docker before pushing to Railway.
- Scripts use `xmlrpc.client` exclusively — no direct DB access from scripts.
- Images reference moaradvisory.com URLs rather than being stored locally.
