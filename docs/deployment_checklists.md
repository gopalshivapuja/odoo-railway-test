# Staging and Production Checklists

## Staging Validation (Phase 6)
1. Create a new Railway environment/service for staging.
2. Link staging service to this GitHub repository branch (suggest `develop`).
3. Configure same env vars as production (with staging-safe values).
4. Restore latest DB dump to staging Postgres.
5. Restore latest filestore backup into staging Odoo volume.
6. Run module updates if needed (`-u <custom_modules>`).
7. Run smoke checks:
   - `/web/health`
   - login
   - homepage + service pages
   - forms/leads/blog paths
8. Record pass/fail in release notes.

## Production Cutover (Phase 7)
1. Announce deployment window.
2. Take fresh DB + filestore backups.
3. Confirm rollback tag exists for previous release.
4. Merge validated PR to `main`.
5. Verify Railway auto-deploy completion.
6. Execute post-deploy smoke checks.
7. Monitor logs + response times for stabilization window.

## Rollback Trigger Conditions
- `/web/health` failing for >5 minutes
- login failures or critical 500s on main pages
- failed DB migrations or broken custom modules

## Rollback Steps
1. Deploy previous Git tag.
2. Restore matching DB dump + filestore.
3. Restart Odoo service.
4. Re-run smoke checks and confirm business-critical flows.
