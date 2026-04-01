#!/usr/bin/env python3
"""Verify all Odoo website modules and features are properly configured."""

from common import connect_odoo


def main():
    url, db, uid, password, models = connect_odoo()

    all_ok = True

    # ── 1. Module Status ──
    print("\n=== MODULE STATUS ===")
    modules = [
        "website", "website_crm", "website_blog", "website_hr_recruitment",
        "website_livechat", "website_mass_mailing", "website_slides",
        "website_event", "website_forum", "website_sale",
    ]
    for mod in modules:
        ids = models.execute_kw(
            db, uid, password, "ir.module.module", "search_read",
            [[["name", "=", mod]]], {"fields": ["name", "state"]}
        )
        if ids:
            status = ids[0]["state"]
            icon = "OK" if status == "installed" else "WARN"
            if status != "installed":
                all_ok = False
            print(f"  [{icon}] {mod}: {status}")
        else:
            print(f"  [MISS] {mod}: not found")
            all_ok = False

    # ── 2. Company Branding ──
    print("\n=== COMPANY BRANDING ===")
    company = models.execute_kw(
        db, uid, password, "res.company", "read",
        [[1], ["name", "email", "website", "city", "country_id"]]
    )
    c = company[0]
    print(f"  Name: {c['name']}")
    print(f"  Email: {c['email']}")
    print(f"  Website: {c['website']}")
    print(f"  City: {c['city']}")
    print(f"  Country: {c['country_id']}")

    # ── 3. Website Config ──
    print("\n=== WEBSITE CONFIG ===")
    websites = models.execute_kw(
        db, uid, password, "website", "search_read",
        [[]], {"fields": ["id", "name"]}
    )
    for w in websites:
        print(f"  Website ID {w['id']}: {w['name']}")

    # ── 4. Navigation Menus ──
    print("\n=== NAVIGATION MENUS ===")
    menus = models.execute_kw(
        db, uid, password, "website.menu", "search_read",
        [[["website_id", "=", 1]]],
        {"fields": ["id", "name", "url", "parent_id", "sequence"],
         "order": "sequence"}
    )
    for m in menus:
        parent = f" (child of {m['parent_id'][1]})" if m["parent_id"] else " [ROOT]"
        print(f"  {m['name']} -> {m['url']}{parent}")

    # ── 5. Blog ──
    print("\n=== BLOG ===")
    blogs = models.execute_kw(
        db, uid, password, "blog.blog", "search_read",
        [[]], {"fields": ["id", "name"]}
    )
    for b in blogs:
        print(f"  Blog: {b['name']} (ID: {b['id']})")
        posts = models.execute_kw(
            db, uid, password, "blog.post", "search_read",
            [[["blog_id", "=", b["id"]]]],
            {"fields": ["id", "name", "is_published"]}
        )
        for p in posts:
            pub = "published" if p["is_published"] else "draft"
            print(f"    - {p['name'][:60]}... [{pub}]")

    # ── 6. CRM Team ──
    print("\n=== CRM TEAMS ===")
    teams = models.execute_kw(
        db, uid, password, "crm.team", "search_read",
        [[]], {"fields": ["id", "name"]}
    )
    for t in teams:
        print(f"  {t['name']} (ID: {t['id']})")

    # ── 7. Jobs ──
    print("\n=== JOB POSTINGS ===")
    jobs = models.execute_kw(
        db, uid, password, "hr.job", "search_read",
        [[]], {"fields": ["id", "name", "website_published"]}
    )
    for j in jobs:
        pub = "published" if j.get("website_published") else "draft"
        print(f"  {j['name']} [{pub}]")

    # ── 8. Events ──
    print("\n=== EVENTS ===")
    events = models.execute_kw(
        db, uid, password, "event.event", "search_read",
        [[]], {"fields": ["id", "name", "date_begin", "website_published"]}
    )
    for e in events:
        pub = "published" if e.get("website_published") else "draft"
        print(f"  {e['name']} ({e['date_begin']}) [{pub}]")

    # ── 9. Live Chat ──
    print("\n=== LIVE CHAT ===")
    channels = models.execute_kw(
        db, uid, password, "im_livechat.channel", "search_read",
        [[]], {"fields": ["id", "name"]}
    )
    for ch in channels:
        print(f"  Channel: {ch['name']} (ID: {ch['id']})")

    # ── Summary ──
    print("\n" + "=" * 50)
    if all_ok:
        print("ALL MODULES INSTALLED SUCCESSFULLY!")
    else:
        print("Some modules are missing - check warnings above.")
    print(f"\nSite URL: {url}")
    print("=" * 50)


if __name__ == "__main__":
    main()
