#!/usr/bin/env python3
"""Update hero sections on 9 pages to use background images."""

import socket
_orig = socket.getaddrinfo
def _patched(host, port, family=0, type=0, proto=0, flags=0):
    if 'railway.app' in str(host):
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', ('151.101.2.15', port if isinstance(port, int) else 443))]
    return _orig(host, port, family, type, proto, flags)
socket.getaddrinfo = _patched

import xmlrpc.client
import re
import ssl
import urllib.request

URL = 'https://odoo-production-26e2.up.railway.app'
DB = 'railway'
USERNAME = 'gopal.shivapuja@moaradvisory.com'
PASSWORD = 'yamaha7222'

# Connect
common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common', context=ssl._create_unverified_context())
uid = common.authenticate(DB, USERNAME, PASSWORD, {})
print(f"Authenticated as uid={uid}")
models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object', context=ssl._create_unverified_context())

PAGES = {
    '/about': 'https://moaradvisory.com/wp-content/uploads/2025/10/MOAR-Advisory-partner-in-growth-Gcc-homepage-banner.webp',
    '/company-setup-finance': 'https://moaradvisory.com/wp-content/uploads/2025/10/MOAR-Advisory-company-setup-and-finances.webp',
    '/people-advisory': 'https://moaradvisory.com/wp-content/uploads/2025/09/HR-Talent-.webp',
    '/m-select': 'https://moaradvisory.com/wp-content/uploads/2026/01/m-select-gcc-recruitment-services-moar-advisory-1.webp',
    '/m-power': 'https://moaradvisory.com/wp-content/uploads/2025/09/Employer-Branding-Communications.webp',
    '/technology-digital': 'https://moaradvisory.com/wp-content/uploads/2025/09/Technology-Digital-Transformation.webp',
    '/advisory-services': 'https://moaradvisory.com/wp-content/uploads/2025/10/MOAR-Advisory-People-Advisory-1.webp',
    '/our-leaders': 'https://moaradvisory.com/wp-content/uploads/2025/10/MOAR-Advisory-partner-in-growth-Gcc-homepage-banner.webp',
    '/case-studies': 'https://moaradvisory.com/wp-content/uploads/2025/10/MOAR-Advisory-partner-in-growth-Gcc-homepage-banner.webp',
}

def update_page(url, image_url):
    print(f"\n{'='*60}")
    print(f"Processing: {url}")

    # Find the page
    pages = models.execute_kw(DB, uid, PASSWORD, 'website.page', 'search_read',
        [[['url', '=', url]]],
        {'fields': ['id', 'name', 'url', 'view_id']})

    if not pages:
        print(f"  WARNING: No page found for {url}")
        return False

    page = pages[0]
    view_id = page['view_id'][0]
    print(f"  Page: {page['name']} (id={page['id']}, view_id={view_id})")

    # Read the view
    views = models.execute_kw(DB, uid, PASSWORD, 'ir.ui.view', 'read',
        [[view_id]], {'fields': ['arch_db']})
    arch = views[0]['arch_db']

    # Find the hero section - look for moar-hero-gradient or moar-hero-img or moar-hero
    # Pattern: <section with class containing moar-hero
    hero_pattern = r'(<section[^>]*class="[^"]*moar-hero[^"]*"[^>]*>)(.*?)(</section>)'
    match = re.search(hero_pattern, arch, re.DOTALL)

    if not match:
        # Try alternate: section that contains an h1
        print("  No moar-hero section found, looking for first section with h1...")
        hero_pattern = r'(<section[^>]*>)(.*?<h1>.*?</h1>.*?)(</section>)'
        match = re.search(hero_pattern, arch, re.DOTALL)

    if not match:
        print(f"  ERROR: Could not find hero section for {url}")
        # Print first 500 chars for debugging
        print(f"  First 500 chars: {arch[:500]}")
        return False

    opening_tag = match.group(1)
    inner_content = match.group(2)
    closing_tag = match.group(3)
    full_match = match.group(0)

    print(f"  Found hero section: {opening_tag[:80]}...")

    # Extract h1 and p content
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', inner_content, re.DOTALL)
    p_match = re.search(r'<p[^>]*>(.*?)</p>', inner_content, re.DOTALL)

    if not h1_match:
        print(f"  ERROR: No h1 found in hero section")
        return False

    h1_text = h1_match.group(1).strip()
    p_text = p_match.group(1).strip() if p_match else ''

    print(f"  H1: {h1_text[:60]}")
    print(f"  P: {p_text[:60]}")

    # Build new hero section
    p_html = f'\n        <p>{p_text}</p>' if p_text else ''
    new_hero = f'''<section class="moar-hero-img" style="background-image: url('{image_url}');">
    <div class="hero-content">
        <h1>{h1_text}</h1>{p_html}
    </div>
</section>'''

    # Replace in arch
    new_arch = arch.replace(full_match, new_hero)

    if new_arch == arch:
        print(f"  WARNING: No change made (replacement didn't work)")
        return False

    # Write back
    result = models.execute_kw(DB, uid, PASSWORD, 'ir.ui.view', 'write',
        [[view_id], {'arch_db': new_arch}])
    print(f"  Updated successfully: {result}")
    return True

# Process all pages
results = {}
for url, image_url in PAGES.items():
    try:
        results[url] = update_page(url, image_url)
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        results[url] = False

# Verify all pages return 200
print(f"\n{'='*60}")
print("Verification - checking HTTP status codes:")
ctx = ssl._create_unverified_context()
for url in PAGES:
    full_url = f"{URL}{url}"
    try:
        req = urllib.request.Request(full_url, method='HEAD')
        resp = urllib.request.urlopen(req, context=ctx, timeout=10)
        status = resp.getcode()
        print(f"  {url}: {status}")
    except Exception as e:
        # Try GET if HEAD fails
        try:
            req = urllib.request.Request(full_url)
            resp = urllib.request.urlopen(req, context=ctx, timeout=15)
            status = resp.getcode()
            print(f"  {url}: {status}")
        except Exception as e2:
            print(f"  {url}: ERROR - {e2}")

print(f"\n{'='*60}")
print("Summary:")
for url, ok in results.items():
    print(f"  {url}: {'OK' if ok else 'FAILED'}")
