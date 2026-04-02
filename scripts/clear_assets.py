#!/usr/bin/env python3
"""Clear Odoo asset cache and force regeneration."""

import sys
sys.path.insert(0, "scripts")
from common import connect_odoo

URL, DB, uid, password, models = connect_odoo()

# Find and delete cached asset bundles
print("Clearing cached asset bundles...")
attachments = models.execute_kw(
    DB, uid, password, "ir.attachment", "search",
    [[["url", "like", "/web/assets/"]]]
)
if attachments:
    models.execute_kw(DB, uid, password, "ir.attachment", "unlink", [attachments])
    print(f"  Deleted {len(attachments)} cached asset attachments")
else:
    print("  No cached assets found")

# Also clear any SCSS compilation cache via qweb
print("Clearing QWeb/SCSS cache...")
try:
    models.execute_kw(DB, uid, password, "ir.qweb", "clear_caches", [])
except Exception:
    pass

print("Done! Reload the site to regenerate assets.")
