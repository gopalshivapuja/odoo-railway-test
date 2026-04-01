# GitHub and Branch Protection Setup

## Repository
- Remote created: `https://github.com/gopalshivapuja/odoo-railway-test`

## Push Initial State
```bash
git add .
git commit -m "Bootstrap owned Odoo Railway repo with CI/CD scaffolding"
git push -u origin main
```

## Protect `main`
Enable these in GitHub branch protection:
- Require pull request before merge
- Require status checks to pass (`lint-and-sanity`, `docker-build`)
- Restrict force pushes
- Require linear history (optional but recommended)

## Recommended Branch Model
- `main` = production
- `develop` = staging integration (optional)
- `feature/*` = active dev work

## Release Tagging
```bash
git tag -a vYYYY.MM.DD.N -m "Production release"
git push origin --tags
```
