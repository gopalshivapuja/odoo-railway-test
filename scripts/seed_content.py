#!/usr/bin/env python3
"""Seed sample content for MOAR Advisory Odoo website via XML-RPC."""

from common import connect_odoo


def main():
    _, db, uid, password, models = connect_odoo()

    # ── 1. Blog: MOAR Lens ──
    print("\n=== Setting up Blog (MOAR Lens) ===")

    # Check if a blog already exists
    existing_blogs = models.execute_kw(
        db, uid, password, "blog.blog", "search_read",
        [[]], {"fields": ["id", "name"]}
    )
    print(f"Existing blogs: {existing_blogs}")

    blog_id = None
    for b in existing_blogs:
        if "MOAR" in b["name"]:
            blog_id = b["id"]
            break

    if not blog_id:
        # Rename first blog or create new one
        if existing_blogs:
            blog_id = existing_blogs[0]["id"]
            models.execute_kw(
                db, uid, password, "blog.blog", "write",
                [[blog_id], {"name": "MOAR Lens"}]
            )
            print(f"  Renamed blog ID {blog_id} to 'MOAR Lens'")
        else:
            blog_id = models.execute_kw(
                db, uid, password, "blog.blog", "create",
                [{"name": "MOAR Lens", "website_id": 1}]
            )
            print(f"  Created blog 'MOAR Lens' (ID: {blog_id})")

    # Create sample blog posts
    posts = [
        {
            "name": "Business Setup Services: The Hidden Risks of Getting First Decisions Wrong",
            "subtitle": "Why choosing the right advisory partner matters from day one",
            "blog_id": blog_id,
            "content": """<section class="s_text_block pt32 pb32">
<div class="container">
<h2>The Foundation Matters</h2>
<p>When setting up a business in India, the decisions you make in the first 90 days can define your trajectory for years. From entity structure to compliance frameworks, from banking relationships to tax planning — each choice creates ripple effects that are costly to reverse.</p>
<p>At MOAR Advisory, we've seen companies lose months of progress and significant capital simply because their initial setup wasn't aligned with their long-term strategy. Our Company Setup & Finance practice exists precisely to prevent these costly missteps.</p>
<h3>Key Areas to Get Right</h3>
<ul>
<li>Entity structure selection (Private Limited, LLP, Branch Office, Liaison Office)</li>
<li>Regulatory compliance framework</li>
<li>Banking and treasury setup</li>
<li>Tax planning and transfer pricing</li>
<li>Accounting system implementation</li>
</ul>
<p>The right advisory partner doesn't just fill forms — they architect your business foundation for scale.</p>
</div>
</section>""",
            "is_published": True,
            "website_id": 1,
        },
        {
            "name": "The Rise of GCCs in India: Why Global Companies Are Building Capability Centers",
            "subtitle": "Understanding the GCC boom and what it means for your organization",
            "blog_id": blog_id,
            "content": """<section class="s_text_block pt32 pb32">
<div class="container">
<h2>India's GCC Revolution</h2>
<p>India is home to over 1,600 Global Capability Centers (GCCs), and this number is growing rapidly. What started as cost arbitrage has evolved into a strategic capability play — companies are building centers of excellence that drive innovation, not just efficiency.</p>
<p>MOAR Advisory's GCC practice helps enterprises navigate the three key models:</p>
<h3>BOT (Build, Operate & Transfer)</h3>
<p>We build and operate your GCC, then transfer full ownership once it's mature and self-sustaining.</p>
<h3>GCC as a Service</h3>
<p>A fully managed model where we handle everything from infrastructure to talent, letting you focus on outcomes.</p>
<h3>Assisted GCC</h3>
<p>For organizations that want to own the journey but need expert guidance at every step.</p>
<p>The right model depends on your organization's maturity, risk appetite, and strategic goals.</p>
</div>
</section>""",
            "is_published": True,
            "website_id": 1,
        },
        {
            "name": "Employer Branding: Why Your EVP Is Your Most Important Recruitment Tool",
            "subtitle": "How M-POWER helps companies build magnetic employer brands",
            "blog_id": blog_id,
            "content": """<section class="s_text_block pt32 pb32">
<div class="container">
<h2>Beyond Job Postings</h2>
<p>In today's competitive talent market, a strong employer brand isn't a nice-to-have — it's a strategic imperative. Companies with strong employer brands see 50% more qualified applicants and significantly lower cost-per-hire.</p>
<p>MOAR Advisory's M-POWER practice focuses on building authentic employer brands that resonate with the talent you want to attract. This goes far beyond logos and career pages.</p>
<h3>The M-POWER Framework</h3>
<ul>
<li><strong>Employee Value Proposition (EVP)</strong> — Defining what makes you unique as an employer</li>
<li><strong>Employer Brand Communications</strong> — Telling your story across channels</li>
<li><strong>Candidate Experience Design</strong> — Every touchpoint matters</li>
<li><strong>Internal Communications</strong> — Your employees are your best brand ambassadors</li>
</ul>
<p>A great employer brand doesn't just attract talent — it retains it.</p>
</div>
</section>""",
            "is_published": True,
            "website_id": 1,
        },
    ]

    for post in posts:
        # Check if post already exists
        existing = models.execute_kw(
            db, uid, password, "blog.post", "search",
            [[["name", "=", post["name"]]]]
        )
        if existing:
            print(f"  Post already exists: {post['name'][:50]}...")
            continue
        post_id = models.execute_kw(
            db, uid, password, "blog.post", "create", [post]
        )
        print(f"  Created post: {post['name'][:50]}... (ID: {post_id})")

    # ── 2. CRM Sales Team ──
    print("\n=== Setting up CRM Sales Team ===")
    existing_teams = models.execute_kw(
        db, uid, password, "crm.team", "search_read",
        [[["name", "ilike", "MOAR"]]], {"fields": ["id", "name"]}
    )
    if not existing_teams:
        team_id = models.execute_kw(
            db, uid, password, "crm.team", "create",
            [{"name": "MOAR Website Leads", "use_leads": True}]
        )
        print(f"  Created CRM team (ID: {team_id})")
    else:
        print(f"  CRM team already exists: {existing_teams[0]['name']}")

    # ── 3. Live Chat Channel ──
    print("\n=== Setting up Live Chat ===")
    existing_channels = models.execute_kw(
        db, uid, password, "im_livechat.channel", "search_read",
        [[]], {"fields": ["id", "name"]}
    )
    if not existing_channels:
        channel_id = models.execute_kw(
            db, uid, password, "im_livechat.channel", "create",
            [{
                "name": "MOAR Advisory Support",
                "button_text": "Chat with us",
                "default_message": "Hello! Welcome to MOAR Advisory. How can we help you today?",
            }]
        )
        print(f"  Created live chat channel (ID: {channel_id})")
    else:
        print(f"  Live chat channel already exists: {existing_channels[0]['name']}")

    # ── 4. Sample Job Posting ──
    print("\n=== Setting up Job Postings ===")
    existing_jobs = models.execute_kw(
        db, uid, password, "hr.job", "search_read",
        [[]], {"fields": ["id", "name"]}
    )
    if not existing_jobs:
        job_id = models.execute_kw(
            db, uid, password, "hr.job", "create",
            [{
                "name": "Senior GCC Consultant",
                "description": """<p>We're looking for an experienced GCC consultant to join our growing advisory team.</p>
<h3>Responsibilities</h3>
<ul>
<li>Lead GCC setup and transformation engagements</li>
<li>Advise clients on operating model design</li>
<li>Drive talent strategy for new capability centers</li>
<li>Manage stakeholder relationships across geographies</li>
</ul>
<h3>Requirements</h3>
<ul>
<li>8+ years in management consulting or GCC operations</li>
<li>Experience with India market entry and setup</li>
<li>Strong stakeholder management skills</li>
<li>MBA or equivalent preferred</li>
</ul>""",
                "website_published": True,
                "no_of_recruitment": 2,
            }]
        )
        print(f"  Created job posting (ID: {job_id})")
    else:
        print(f"  Jobs already exist: {[j['name'] for j in existing_jobs]}")

    # ── 5. Sample Event ──
    print("\n=== Setting up Events ===")
    existing_events = models.execute_kw(
        db, uid, password, "event.event", "search_read",
        [[]], {"fields": ["id", "name"]}
    )
    if not existing_events:
        event_id = models.execute_kw(
            db, uid, password, "event.event", "create",
            [{
                "name": "Conversations that Shape Decisions - GCC Strategy Webinar",
                "date_begin": "2026-04-15 10:00:00",
                "date_end": "2026-04-15 11:30:00",
                "website_published": True,
                "description": """<p>Join MOAR Advisory's leadership team for an insightful webinar on GCC strategy in 2026.</p>
<p>Topics covered:</p>
<ul>
<li>The evolving GCC landscape in India</li>
<li>Choosing the right GCC model for your organization</li>
<li>Talent acquisition and retention strategies</li>
<li>Technology infrastructure decisions</li>
</ul>
<p>This session is ideal for CXOs, HR leaders, and strategy teams evaluating India as a GCC destination.</p>""",
            }]
        )
        print(f"  Created event (ID: {event_id})")
    else:
        print(f"  Events already exist: {[e['name'] for e in existing_events]}")

    print("\nContent seeding complete!")


if __name__ == "__main__":
    main()
