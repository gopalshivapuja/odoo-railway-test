#!/usr/bin/env python3
"""Install the theme_moar_advisory module on Odoo."""

import sys
import time

sys.path.insert(0, "scripts")
from common import connect_odoo

URL, DB, uid, password, models = connect_odoo()

print("Updating module list...")
models.execute_kw(DB, uid, password, "ir.module.module", "update_list", [])
time.sleep(2)

# Find the module
modules = models.execute_kw(
    DB, uid, password, "ir.module.module", "search_read",
    [[["name", "=", "theme_moar_advisory"]]],
    {"fields": ["id", "state", "name"]}
)

if not modules:
    print("ERROR: theme_moar_advisory not found. Check that the module is in /mnt/extra-addons/")
    sys.exit(1)

mod = modules[0]
print(f"Found module: {mod['name']} (ID: {mod['id']}, state: {mod['state']})")

if mod["state"] == "installed":
    print("Module already installed. Upgrading...")
    models.execute_kw(DB, uid, password, "ir.module.module", "button_immediate_upgrade", [[mod["id"]]])
else:
    print("Installing module...")
    models.execute_kw(DB, uid, password, "ir.module.module", "button_immediate_install", [[mod["id"]]])

time.sleep(3)

# Verify
modules = models.execute_kw(
    DB, uid, password, "ir.module.module", "search_read",
    [[["name", "=", "theme_moar_advisory"]]],
    {"fields": ["state"]}
)
print(f"Module state: {modules[0]['state']}")
print(f"\nDone! Visit {URL} to see the theme.")
