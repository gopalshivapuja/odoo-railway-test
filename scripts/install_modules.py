#!/usr/bin/env python3
"""Install all Odoo website modules via XML-RPC API."""

import time
from common import connect_odoo

# All website modules to install, in dependency order
MODULES = [
    # Batch 1: Core
    "website_crm",
    "website_blog",
    # Batch 2: Features
    "website_hr_recruitment",
    "website_livechat",
    "website_mass_mailing",
    "website_appointment",
    # Batch 3: Extended
    "website_slides",
    "website_event",
    "website_forum",
    "website_sale",
    "website_membership",
    # Backend branding
    "moar_backend_brand",
]


def main():
    _, db, uid, password, models = connect_odoo()
    print(f"Authenticated as uid={uid}")

    for module_name in MODULES:
        print(f"\n--- {module_name} ---")

        # Find the module
        module_ids = models.execute_kw(
            db, uid, password, "ir.module.module", "search",
            [[["name", "=", module_name]]]
        )
        if not module_ids:
            print("  NOT FOUND - skipping")
            continue

        # Check current state
        info = models.execute_kw(
            db, uid, password, "ir.module.module", "read",
            [module_ids, ["name", "state"]]
        )
        state = info[0]["state"]
        print(f"  Current state: {state}")

        if state == "installed":
            print("  Already installed - skipping")
            continue

        # Install the module
        print("  Installing... (this may take a minute)")
        try:
            models.execute_kw(
                db, uid, password, "ir.module.module",
                "button_immediate_install", [module_ids]
            )
            print("  INSTALLED successfully!")
        except Exception as e:
            error_msg = str(e)
            if "timeout" in error_msg.lower() or "deadline" in error_msg.lower():
                print("  Timeout during install - module may still be installing.")
                print("  Waiting 30s before continuing...")
                time.sleep(30)
            else:
                print(f"  ERROR: {error_msg}")
                print("  Continuing with next module...")

        # Brief pause between installs
        time.sleep(2)

    # Final status check
    print("\n\n=== FINAL STATUS ===")
    for module_name in MODULES:
        module_ids = models.execute_kw(
            db, uid, password, "ir.module.module", "search",
            [[["name", "=", module_name]]]
        )
        if module_ids:
            info = models.execute_kw(
                db, uid, password, "ir.module.module", "read",
                [module_ids, ["name", "state"]]
            )
            print(f"  {module_name}: {info[0]['state']}")
        else:
            print(f"  {module_name}: NOT FOUND")


if __name__ == "__main__":
    main()
