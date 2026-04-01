#!/usr/bin/env python3
"""Configure MOAR Advisory branding in Odoo via XML-RPC."""

import base64
import os

from common import connect_odoo


def main():
    _, db, uid, password, models = connect_odoo()

    # Load logo
    print("Loading logo...")
    logo_path = os.getenv("MOAR_LOGO_PATH", "assets/moar_logo.png")
    with open(logo_path, "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode()

    # Find India country ID
    india_ids = models.execute_kw(
        db, uid, password, "res.country", "search",
        [[["name", "=", "India"]]]
    )
    india_id = india_ids[0] if india_ids else False

    # Find Karnataka state ID
    karnataka_ids = models.execute_kw(
        db, uid, password, "res.country.state", "search",
        [[["name", "ilike", "Karnataka"]]]
    )
    karnataka_id = karnataka_ids[0] if karnataka_ids else False

    # Update company record
    print("Updating company info...")
    models.execute_kw(
        db, uid, password, "res.company", "write",
        [[1], {
            "name": "MOAR Advisory",
            "email": "contact@moaradvisory.com",
            "website": "https://moaradvisory.com",
            "street": "1st Floor, 611, 2nd Cross Rd, 3rd Block",
            "street2": "Koramangala",
            "city": "Bengaluru",
            "zip": "560034",
            "country_id": india_id,
            "state_id": karnataka_id,
            "logo": logo_b64,
        }]
    )
    print("  Company info updated!")

    # Update website record
    print("Updating website settings...")
    website_ids = models.execute_kw(
        db, uid, password, "website", "search", [[]]
    )
    if website_ids:
        models.execute_kw(
            db, uid, password, "website", "write",
            [website_ids, {
                "name": "MOAR Advisory",
                "logo": logo_b64,
            }]
        )
        print(f"  Website name and logo updated (IDs: {website_ids})")

    # Update admin user name
    print("Updating admin user...")
    models.execute_kw(
        db, uid, password, "res.users", "write",
        [[uid], {
            "name": "Gopal Shivapuja",
            "company_name": "MOAR Advisory",
        }]
    )
    print("  Admin user updated!")

    # Update partner (linked to company)
    print("Updating company partner...")
    company_info = models.execute_kw(
        db, uid, password, "res.company", "read",
        [[1], ["partner_id"]]
    )
    partner_id = company_info[0]["partner_id"][0]
    models.execute_kw(
        db, uid, password, "res.partner", "write",
        [[partner_id], {
            "name": "MOAR Advisory",
            "image_1920": logo_b64,
            "website": "https://moaradvisory.com",
        }]
    )
    print("  Company partner updated!")

    print("\nBranding configuration complete!")


if __name__ == "__main__":
    main()
