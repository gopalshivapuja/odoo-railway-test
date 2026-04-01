#!/usr/bin/env python3
"""Set up MOAR Advisory navigation menus in Odoo via XML-RPC."""

import sys

from common import connect_odoo


def main():
    _, db, uid, password, models = connect_odoo()

    # Find the top-level menu (root menu for website 1)
    top_menus = models.execute_kw(
        db, uid, password, "website.menu", "search_read",
        [[["website_id", "=", 1], ["parent_id", "=", False]]],
        {"fields": ["id", "name"]}
    )
    if not top_menus:
        print("ERROR: No root menu found!")
        sys.exit(1)

    root_id = top_menus[0]["id"]
    print(f"Root menu: {top_menus[0]['name']} (ID: {root_id})")

    # List existing child menus
    existing = models.execute_kw(
        db, uid, password, "website.menu", "search_read",
        [[["website_id", "=", 1], ["parent_id", "=", root_id]]],
        {"fields": ["id", "name", "url"]}
    )
    print(f"\nExisting menus ({len(existing)}):")
    for m in existing:
        print(f"  ID {m['id']}: {m['name']} -> {m['url']}")

    # Delete existing child menus (and their children)
    if existing:
        all_child_ids = models.execute_kw(
            db, uid, password, "website.menu", "search",
            [[["website_id", "=", 1], ["id", "!=", root_id]]]
        )
        if all_child_ids:
            models.execute_kw(
                db, uid, password, "website.menu", "unlink", [all_child_ids]
            )
            print(f"\nDeleted {len(all_child_ids)} existing menu items.")

    # Helper to create menu
    def create_menu(name, url, parent_id, sequence):
        mid = models.execute_kw(
            db, uid, password, "website.menu", "create",
            [{"name": name, "url": url, "parent_id": parent_id,
              "sequence": sequence, "website_id": 1}]
        )
        print(f"  Created: {name} -> {url} (ID: {mid})")
        return mid

    print("\nCreating MOAR Advisory menus...")

    # Home
    create_menu("Home", "/", root_id, 10)

    # About (dropdown)
    about_id = create_menu("About", "#", root_id, 20)
    create_menu("Overview", "/about", about_id, 21)
    create_menu("Our Leaders", "/our-leaders", about_id, 22)

    # Our Offerings (dropdown)
    offerings_id = create_menu("Our Offerings", "#", root_id, 30)
    create_menu("Company Setup & Finance", "/company-setup-finance", offerings_id, 31)
    create_menu("People Advisory", "/people-advisory", offerings_id, 32)
    create_menu("M-SELECT Recruitment", "/m-select", offerings_id, 33)
    create_menu("M-POWER Employer Branding", "/m-power", offerings_id, 34)
    create_menu("Technology & Digital Transformation", "/technology-digital", offerings_id, 35)
    create_menu("Advisory Services", "/advisory-services", offerings_id, 36)

    # Case Studies
    create_menu("Case Studies", "/case-studies", root_id, 40)

    # MOAR Lens (Blog)
    create_menu("MOAR Lens", "/blog", root_id, 50)

    # Media
    create_menu("Media", "/media", root_id, 60)

    # Contact Us
    create_menu("Contact Us", "/contactus", root_id, 70)

    print("\nMenu setup complete!")


if __name__ == "__main__":
    main()
