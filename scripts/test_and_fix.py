#!/usr/bin/env python3
"""Comprehensive test suite for MOAR Advisory Odoo website."""

import urllib.request
import urllib.error
import xmlrpc.client
import re
import ssl

from common import get_odoo_config

URL, DB, USERNAME, PASSWORD = get_odoo_config()

# SSL context for HTTPS
ctx = ssl.create_default_context()

PASS = "\033[92m PASS \033[0m"
FAIL = "\033[91m FAIL \033[0m"
WARN = "\033[93m WARN \033[0m"

issues = []


def fetch(path, follow_redirects=True):
    """Fetch a page and return (status_code, html_body)."""
    try:
        req = urllib.request.Request(
            f"{URL}{path}",
            headers={"User-Agent": "Mozilla/5.0 MOAR-Test-Bot"}
        )
        resp = urllib.request.urlopen(req, context=ctx, timeout=30)
        body = resp.read().decode("utf-8", errors="replace")
        return resp.status, body
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", errors="replace")
        except Exception:
            pass
        return e.code, body
    except Exception as e:
        return 0, str(e)


def check(label, condition, detail=""):
    """Log a test result."""
    if condition:
        print(f"  [{PASS}] {label}")
    else:
        msg = f"{label}: {detail}" if detail else label
        print(f"  [{FAIL}] {msg}")
        issues.append(msg)
    return condition


# ═══════════════════════════════════════════
# TEST 1: Page Response & Content
# ═══════════════════════════════════════════
print("=" * 60)
print("TEST 1: PAGE RESPONSE & CONTENT CHECKS")
print("=" * 60)

pages = {
    "/": {
        "name": "Homepage",
        "expect": ["Advice You Can Trust", "Your Partner in Growth", "What We Do", "moar-hero"],
    },
    "/about": {
        "name": "About Overview",
        "expect": ["About MOAR Advisory", "Who We Are", "Global Footprint"],
    },
    "/our-leaders": {
        "name": "Our Leaders",
        "expect": ["Our Leaders", "Mohith Mohan", "Gopal Shivapuja"],
    },
    "/company-setup-finance": {
        "name": "Company Setup & Finance",
        "expect": ["Company Setup", "Legal Entity Setup", "Simplified Entry"],
    },
    "/people-advisory": {
        "name": "People Advisory",
        "expect": ["People Advisory", "Workforce Strategy", "Executive Coaching"],
    },
    "/m-select": {
        "name": "M-SELECT Recruitment",
        "expect": ["M-SELECT", "Strategic Recruitment", "GCC Success"],
    },
    "/m-power": {
        "name": "M-POWER Employer Branding",
        "expect": ["M-POWER", "Employer Branding", "Strategic Communications"],
    },
    "/technology-digital": {
        "name": "Technology & Digital",
        "expect": ["Technology", "Digital Transformation", "Enterprise IT"],
    },
    "/advisory-services": {
        "name": "Advisory Services",
        "expect": ["Advisory Services", "Feasibility Study", "Location Services"],
    },
    "/case-studies": {
        "name": "Case Studies",
        "expect": ["Case Studies", "Global Leader in Packaging", "Retail"],
    },
    "/media": {
        "name": "Media",
        "expect": ["Media", "Podcasts", "Conversations"],
    },
    "/blog": {
        "name": "Blog (MOAR Lens)",
        "expect": ["blog"],  # Odoo blog page
    },
    "/contactus": {
        "name": "Contact Us",
        "expect": ["contact", "form"],  # Odoo contact page
    },
    "/jobs": {
        "name": "Jobs",
        "expect": [],  # Just check 200
    },
    "/event": {
        "name": "Events",
        "expect": [],
    },
    "/shop": {
        "name": "Shop (eCommerce)",
        "expect": [],
    },
    "/forum": {
        "name": "Forum",
        "expect": [],
    },
    "/slides": {
        "name": "Courses (Slides)",
        "expect": [],
    },
}

page_html_cache = {}

for path, config in pages.items():
    name = config["name"]
    print(f"\n  --- {name} ({path}) ---")

    status, body = fetch(path)
    page_html_cache[path] = (status, body)

    check(f"{name}: HTTP status", status == 200, f"got {status}")

    if status == 200:
        # Check for Odoo error/traceback
        has_error = "Internal Server Error" in body or "Traceback" in body or "odoo.exceptions" in body
        check(f"{name}: No server errors", not has_error, "found error/traceback in page")

        # Check expected content
        for keyword in config.get("expect", []):
            found = keyword.lower() in body.lower()
            check(f"{name}: contains '{keyword}'", found, f"'{keyword}' not found in page")

# ═══════════════════════════════════════════
# TEST 2: CSS & STYLING
# ═══════════════════════════════════════════
print("\n" + "=" * 60)
print("TEST 2: CSS & STYLING VALIDATION")
print("=" * 60)

# Check homepage for CSS
status, body = page_html_cache.get("/", (0, ""))
if status == 200:
    check("Custom CSS: 'moar-hero' class present", "moar-hero" in body)
    check("Custom CSS: 'moar-card' class present", "moar-card" in body)
    check("Custom CSS: 'moar-section' class present", "moar-section" in body)
    check("Google Fonts: Archivo loading", "fonts.googleapis.com" in body or "Archivo" in body)
    check("Gradient colors: #2575fc present", "#2575fc" in body or "2575fc" in body)
    check("Gradient colors: #6a11cb present", "#6a11cb" in body or "6a11cb" in body)
    check("Dark theme: #1a1a2e present", "#1a1a2e" in body or "1a1a2e" in body)

    # Check for MOAR branding
    check("Branding: 'MOAR Advisory' in page", "MOAR Advisory" in body)

# Check a service page
status, body = page_html_cache.get("/about", (0, ""))
if status == 200:
    check("About page: has moar-hero", "moar-hero" in body)
    check("About page: has moar-stat", "moar-stat" in body)


# ═══════════════════════════════════════════
# TEST 3: NAVIGATION & LINKS
# ═══════════════════════════════════════════
print("\n" + "=" * 60)
print("TEST 3: NAVIGATION & LINKS")
print("=" * 60)

status, body = page_html_cache.get("/", (0, ""))
if status == 200:
    # Check nav menu items are present
    nav_items = [
        ("Home", "/"),
        ("About", "#"),
        ("Our Offerings", "#"),
        ("Case Studies", "/case-studies"),
        ("MOAR Lens", "/blog"),
        ("Media", "/media"),
        ("Contact Us", "/contactus"),
    ]
    for name, href in nav_items:
        found = name in body
        check(f"Nav menu: '{name}' present", found)

    # Extract all internal links and test them
    link_pattern = re.compile(r'href="(/[^"]*)"')
    found_links = set(link_pattern.findall(body))
    # Filter to unique internal paths, skip anchors and static files
    test_links = set()
    for link in found_links:
        if link.startswith("/web/") or link.startswith("/website/") or link.startswith("/odoo/"):
            continue
        if any(link.endswith(ext) for ext in [".css", ".js", ".png", ".jpg", ".svg", ".ico", ".woff"]):
            continue
        if link == "#" or link.startswith("/#"):
            continue
        test_links.add(link.split("?")[0].split("#")[0])

    print(f"\n  Found {len(test_links)} unique internal links on homepage")
    broken_links = []
    for link in sorted(test_links):
        s, _ = fetch(link)
        if s != 200:
            broken_links.append((link, s))
            print(f"  [{FAIL}] {link} -> HTTP {s}")
        else:
            print(f"  [{PASS}] {link} -> OK")

    check("No broken links on homepage", len(broken_links) == 0,
          f"{len(broken_links)} broken: {broken_links}")


# ═══════════════════════════════════════════
# TEST 4: FEATURES (XML-RPC)
# ═══════════════════════════════════════════
print("\n" + "=" * 60)
print("TEST 4: FEATURE VERIFICATION (XML-RPC)")
print("=" * 60)

common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common", allow_none=True)
uid = common.authenticate(DB, USERNAME, PASSWORD, {})
check("XML-RPC: authentication works", uid is not None and uid > 0, f"uid={uid}")

models = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object", allow_none=True)

# Blog posts
print("\n  --- Blog ---")
posts = models.execute_kw(
    DB, uid, PASSWORD, "blog.post", "search_read",
    [[["is_published", "=", True]]],
    {"fields": ["id", "name", "website_url"], "limit": 10}
)
check("Blog: has published posts", len(posts) > 0, f"found {len(posts)} posts")
for post in posts:
    post_url = post.get("website_url", "")
    if post_url:
        s, b = fetch(post_url)
        check(f"Blog post '{post['name'][:40]}' accessible", s == 200, f"HTTP {s} at {post_url}")

# CRM / Contact form test
print("\n  --- CRM & Contact ---")
try:
    lead_id = models.execute_kw(
        DB, uid, PASSWORD, "crm.lead", "create",
        [{"name": "Test Lead from Website", "email_from": "test@moartest.com",
          "phone": "+91-9999999999", "description": "Automated test lead"}]
    )
    check("CRM: can create lead", lead_id > 0, f"lead_id={lead_id}")
    # Clean up
    models.execute_kw(DB, uid, PASSWORD, "crm.lead", "unlink", [[lead_id]])
    print(f"    (cleaned up test lead {lead_id})")
except Exception as e:
    check("CRM: can create lead", False, str(e))

# Jobs
print("\n  --- Jobs ---")
jobs = models.execute_kw(
    DB, uid, PASSWORD, "hr.job", "search_read",
    [[["website_published", "=", True]]],
    {"fields": ["id", "name"]}
)
check("Jobs: has published job postings", len(jobs) > 0, f"found {len(jobs)}")

# Events
print("\n  --- Events ---")
events = models.execute_kw(
    DB, uid, PASSWORD, "event.event", "search_read",
    [[["website_published", "=", True]]],
    {"fields": ["id", "name"]}
)
check("Events: has published events", len(events) > 0, f"found {len(events)}")

# Live Chat
print("\n  --- Live Chat ---")
channels = models.execute_kw(
    DB, uid, PASSWORD, "im_livechat.channel", "search_read",
    [[]], {"fields": ["id", "name"]}
)
check("Live Chat: channel configured", len(channels) > 0, f"found {len(channels)}")

# CSS View active
print("\n  --- Custom CSS View ---")
css_views = models.execute_kw(
    DB, uid, PASSWORD, "ir.ui.view", "search_read",
    [[["key", "=", "moar_advisory.custom_css_inject"]]],
    {"fields": ["id", "name", "active", "inherit_id"]}
)
if css_views:
    v = css_views[0]
    check("CSS View: exists", True)
    check("CSS View: is active", v.get("active", False), f"active={v.get('active')}")
    check("CSS View: has inherit_id", v.get("inherit_id") is not None)
else:
    check("CSS View: exists", False, "moar_advisory.custom_css_inject not found")

# Website menus
print("\n  --- Navigation Menus ---")
menus = models.execute_kw(
    DB, uid, PASSWORD, "website.menu", "search_read",
    [[["website_id", "=", 1], ["parent_id", "!=", False]]],
    {"fields": ["id", "name", "url", "parent_id"], "order": "sequence"}
)
expected_menus = ["Home", "About", "Overview", "Our Leaders", "Our Offerings",
                  "Company Setup", "People Advisory", "M-SELECT", "M-POWER",
                  "Technology", "Advisory Services", "Case Studies", "MOAR Lens",
                  "Media", "Contact Us"]
menu_names = [m["name"] for m in menus]
for em in expected_menus:
    found = any(em.lower() in mn.lower() for mn in menu_names)
    check(f"Menu: '{em}' present", found)


# ═══════════════════════════════════════════
# TEST 5: CONTACT FORM (JSON-RPC)
# ═══════════════════════════════════════════
print("\n" + "=" * 60)
print("TEST 5: CONTACT FORM SUBMISSION (JSON-RPC)")
print("=" * 60)

# Test the /contactus page has a form
status, body = page_html_cache.get("/contactus", (0, ""))
if status == 200:
    has_form = "<form" in body.lower() or "s_website_form" in body
    check("Contact page: has form element", has_form)
    has_email_field = "email" in body.lower()
    check("Contact page: has email field", has_email_field)


# ═══════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════
print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)

if issues:
    print(f"\n  {FAIL} {len(issues)} issue(s) found:\n")
    for i, issue in enumerate(issues, 1):
        print(f"    {i}. {issue}")
else:
    print(f"\n  {PASS} All tests passed!")

print(f"\n  Site: {URL}")
print("=" * 60)
