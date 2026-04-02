#!/usr/bin/env python3
"""Rebuild MOAR Advisory Odoo website with real images and exact styling."""

import sys
import time

sys.path.insert(0, "scripts")
from common import get_odoo_config, connect_odoo

URL, DB, _username, _password = get_odoo_config()

# Image base URL from moaradvisory.com
IMG = "https://moaradvisory.com/wp-content/uploads"

# ── Image URLs ──
IMAGES = {
    "logo": f"{IMG}/2025/08/MOAR-logo-TM-scaled.png",
    "hero_banner": f"{IMG}/2025/10/MOAR-Advisory-partner-in-growth-Gcc-homepage-banner.webp",
    "about_banner": f"{IMG}/2025/11/About-MOAR-advisory-scaled.webp",
    "map": f"{IMG}/2025/11/MOAR-Map-Image-BG.png",
    # Services
    "company_setup": f"{IMG}/2025/10/MOAR-Advisory-company-setup-and-finances.webp",
    "people_advisory": f"{IMG}/2025/09/HR-Talent-.webp",
    "m_select": f"{IMG}/2026/01/m-select-gcc-recruitment-services-moar-advisory-1.webp",
    "m_power": f"{IMG}/2025/09/Employer-Branding-Communications.webp",
    "tech_digital": f"{IMG}/2025/09/Technology-Digital-Transformation.webp",
    "advisory": f"{IMG}/2025/10/MOAR-Advisory-People-Advisory-1.webp",
    # GCC
    "bot": f"{IMG}/2025/09/BOT-–-Build-Operate-Transfer.webp",
    "gcc_service": f"{IMG}/2025/09/GCC-Global-Capability-Center-as-a-Service-e1774597756674.webp",
    "assisted_gcc": f"{IMG}/2025/09/Assisted-GCC.webp",
    # How we work
    "roadmap": f"{IMG}/2025/10/MOAR-Advisory-Build-the-roadmap-scaled.webp",
    "execution": f"{IMG}/2025/10/MOAR-Advisory-partner-in-execution-1.webp",
    "deliver": f"{IMG}/2025/10/MOAR-Advisory-deliver-and-execute.webp",
    # Team
    "mohith": f"{IMG}/2025/10/Mohith-Mohan-MOAR-Advisory-leadership-team-1024x1024.webp",
    "mukesh": f"{IMG}/2025/09/Moar-advisory-Mukesh-Kedia-1024x1024.webp",
    "gopal": "https://moaradvisory.com/wp-content/uploads/2026/03/santaoh-moar.avif",
    "santosh": f"{IMG}/2026/01/Santosh-Gnanaprakash-MOAR-Advisory-1024x1024.webp",
    "anneka": f"{IMG}/2025/10/Anneka-Darashah-MOAR-Advisory-1024x1024.webp",
    "sonia": f"{IMG}/2025/11/Sonia-Sharma-MOAR-Advisory-1024x1024.webp",
    "rahul": f"{IMG}/2025/11/Rahul-Virk-MOAR-Advisory-1-1024x1024.webp",
    "minoo": f"{IMG}/2025/09/Moar-advisory-Minoo-Verma-1024x1024.webp",
    "harsha": f"{IMG}/2025/11/Harsha-Nandakumar-MOAR-Advisory-1024x1024.webp",
    # Advisory committee
    "mahendra": f"{IMG}/2025/12/Mahendra-Dhillon-MOAR-Advisory-1024x1024.webp",
    "gagan": f"{IMG}/2025/09/Gagan-ganpathy-MOAR-Advisory-2-1024x1024.webp",
    "tom": f"{IMG}/2025/12/Tom-Ott-MOAR-Advisory-1024x1024.webp",
    # Service page banners
    "cs_banner": f"{IMG}/2025/10/company-setup-and-finance-Moar-advisory-banner.webp",
    "cs_gcc": f"{IMG}/2025/10/Company-setup-and-finance-gccs-entering-new-geographies.webp",
    "cs_startup": f"{IMG}/2025/10/Company-setup-and-finance-expert-guidance-from-a-trusted-business-advisory-firm.webp",
    "cs_sme": f"{IMG}/2025/10/Company-setup-and-finance-SMEs-who-need-comprehensive-business-advisory-and-global-business-services.webp",
    "cs_corp": f"{IMG}/2025/10/Company-setup-and-finance-Corporate-teams-who-need-business-advisory-services.webp",
    "ms_banner": f"{IMG}/2025/10/M-Select-recruitment-MOAR-advisory.webp",
    "ms_teams": f"{IMG}/2025/10/M-Select-recruitment-accelerating-high-impact-teams.webp",
    "ms_candidate": f"{IMG}/2025/10/M-Select-recruitment-personalized-candidate-journey-through-SMEs.webp",
    "ms_brand": f"{IMG}/2025/10/M-Select-recruitment-elevating-employer-branding-and-retaining-top-talent.webp",
    # Case studies
    "case_sonoco": f"{IMG}/2025/10/GCC-Setup-for-Sonoco-Performance-Hub-1024x659.webp",
    "case_packaging": f"{IMG}/2025/10/Global-Leader-in-Packaging-blog-banner-1024x659.webp",
    # Blog
    "blog_setup": f"{IMG}/2026/02/Business-Setup-Service-and-the-Hidden-Risks-of-Getting-the-First-Decisions-WrongBusiness-Setup-Servi-1.webp",
    "blog_formation": f"{IMG}/2026/02/Company-Formation-Services-for-Modern-Businesses-Entering-New-MarketsCompany-Formation-Services-for-1.webp",
    "blog_ai": f"{IMG}/2026/01/Digital-Transformation-Solutions-AI-First-blog-banner.webp",
    "blog_advisory": f"{IMG}/2026/01/Business-advisory-consulting-matters-for-modern-enterprises-blog-banner.webp",
    "blog_gcc_engine": f"{IMG}/2026/01/Why-the-Global-Capability-Center-is-Becoming-a-Strategic-Innovation-Engine-blog-banner-scaled.webp",
    "blog_gcc_setup": f"{IMG}/2025/12/Global-Capability-Center-Setup-what-every-leader-must-know-blog-banner-scaled.webp",
    "blog_gcc_kpi": f"{IMG}/2025/11/GCCs-why-value-continuity-is-the-new-KPI-blog-banner-scaled.webp",
    "blog_tier2": f"{IMG}/2025/10/Tier-2–3-Cities-Beyond-the-Metro-Why-the-Heart-of-the-Next-GCC-Strategy-1024x658-1.webp",
}

# ═══════════════════════════════════════════
# Updated CSS - exact match to moaradvisory.com
# ═══════════════════════════════════════════
CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;900&display=swap');

:root {
    --moar-blue: #2575fc;
    --moar-purple: #6a11cb;
    --moar-dark: #1a1a2e;
    --moar-gray: #32373c;
    --moar-light: #f7f8fa;
    --moar-text: #333333;
    --moar-text-light: #555555;
    --moar-gradient: linear-gradient(-35deg, #2575fc, #6a11cb);
    --moar-border: #e8e8e8;
}

/* ── Reset & Global ── */
body, .o_website_page {
    font-family: 'Archivo', sans-serif !important;
    color: var(--moar-text);
    font-size: 16px;
    line-height: 1.75;
    -webkit-font-smoothing: antialiased;
}
h1,h2,h3,h4,h5,h6,.h1,.h2,.h3,.h4,.h5,.h6 {
    font-family: 'Archivo', sans-serif !important;
    font-weight: 700;
    color: var(--moar-dark);
    line-height: 1.3;
}
h1,.h1 { font-size: 42px; }
h2,.h2 { font-size: 36px; margin-bottom: 20px; }
h3,.h3 { font-size: 22px; }
h4,.h4 { font-size: 18px; }
p { font-size: 16px; line-height: 1.8; color: var(--moar-text-light); margin-bottom: 16px; }
a { color: var(--moar-blue); transition: all 0.3s ease; }
a:hover { color: var(--moar-purple); }
img { max-width: 100%; height: auto; border-radius: 8px; }

/* ── Header ── */
header .navbar {
    background: #ffffff !important;
    box-shadow: 0 1px 8px rgba(0,0,0,0.06);
    padding: 10px 0;
    border-bottom: 1px solid var(--moar-border);
}
header .navbar-brand img { max-height: 42px; }
header .nav-link {
    font-family: 'Archivo', sans-serif !important;
    font-weight: 600;
    font-size: 14px;
    color: var(--moar-dark) !important;
    padding: 8px 14px !important;
    letter-spacing: 0.2px;
    transition: color 0.3s ease;
}
header .nav-link:hover { color: var(--moar-blue) !important; }
header .dropdown-menu {
    border: none;
    box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    border-radius: 8px;
    padding: 8px 0;
}
header .dropdown-item {
    font-size: 14px;
    padding: 8px 20px;
    font-weight: 500;
}
header .dropdown-item:hover { background: var(--moar-light); color: var(--moar-blue); }

/* ── Buttons ── */
.btn-primary, .btn-moar {
    background: var(--moar-gray) !important;
    border: none !important;
    color: #fff !important;
    padding: 12px 28px;
    border-radius: 5px;
    font-weight: 600;
    font-size: 15px;
    transition: all 0.3s ease;
    letter-spacing: 0.3px;
}
.btn-primary:hover, .btn-moar:hover {
    background: #555 !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 15px rgba(0,0,0,0.15);
}
.btn-gradient {
    background: var(--moar-gradient) !important;
    border: none !important;
    color: #fff !important;
    padding: 14px 36px;
    border-radius: 5px;
    font-weight: 700;
    font-size: 16px;
}
.btn-gradient:hover { opacity: 0.92; transform: translateY(-2px); box-shadow: 0 8px 25px rgba(37,117,252,0.3); }
.btn-white {
    background: #ffffff !important;
    color: var(--moar-gray) !important;
    border: 1px solid #ccc !important;
    padding: 10px 24px;
    border-radius: 5px;
    font-weight: 600;
    font-size: 15px;
}
.btn-white:hover { background: var(--moar-gray) !important; color: #fff !important; }
.btn-outline {
    background: transparent !important;
    border: 2px solid var(--moar-blue) !important;
    color: var(--moar-blue) !important;
    padding: 10px 28px;
    border-radius: 5px;
    font-weight: 600;
}
.btn-outline:hover { background: var(--moar-blue) !important; color: #fff !important; }

/* ── Hero Banner ── */
.moar-hero-img {
    position: relative;
    min-height: 520px;
    background-size: cover;
    background-position: center;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
}
.moar-hero-img::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(26,26,46,0.75), rgba(37,117,252,0.55));
    z-index: 1;
}
.moar-hero-img .hero-content {
    position: relative;
    z-index: 2;
    max-width: 800px;
    padding: 40px 20px;
}
.moar-hero-img h1 {
    color: #ffffff;
    font-size: 46px;
    font-weight: 900;
    margin-bottom: 18px;
    text-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
.moar-hero-img p {
    color: rgba(255,255,255,0.92);
    font-size: 20px;
    max-width: 650px;
    margin: 0 auto 28px;
    line-height: 1.6;
}

/* ── Gradient Hero (for inner pages) ── */
.moar-hero-gradient {
    background: var(--moar-gradient);
    padding: 80px 0 60px;
    text-align: center;
}
.moar-hero-gradient h1 { color: #fff; font-size: 42px; font-weight: 900; margin-bottom: 14px; }
.moar-hero-gradient p { color: rgba(255,255,255,0.9); font-size: 18px; max-width: 600px; margin: 0 auto; }

/* ── Sections ── */
.moar-section { padding: 80px 0; }
.moar-section-sm { padding: 50px 0; }
.moar-section-gray { background: var(--moar-light); }
.moar-section-dark { background: var(--moar-dark); }
.moar-section-dark h2,.moar-section-dark h3,.moar-section-dark h4 { color: #fff; }
.moar-section-dark p { color: rgba(255,255,255,0.78); }
.section-title { text-align: center; margin-bottom: 48px; }
.section-title h2 { font-size: 36px; font-weight: 700; margin-bottom: 12px; }
.section-title p { font-size: 17px; color: var(--moar-text-light); max-width: 580px; margin: 0 auto; }
.section-subtitle {
    display: inline-block;
    background: var(--moar-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 700;
    font-size: 14px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 10px;
}

/* ── Cards ── */
.moar-card {
    background: #ffffff;
    border-radius: 10px;
    padding: 0;
    box-shadow: 0 2px 16px rgba(0,0,0,0.05);
    transition: all 0.35s ease;
    height: 100%;
    border: 1px solid var(--moar-border);
    overflow: hidden;
}
.moar-card:hover { transform: translateY(-5px); box-shadow: 0 12px 35px rgba(0,0,0,0.1); }
.moar-card .card-img { width: 100%; height: 200px; object-fit: cover; border-radius: 0; }
.moar-card .card-body { padding: 28px; }
.moar-card h3 { font-size: 19px; font-weight: 700; margin-bottom: 12px; color: var(--moar-dark); }
.moar-card p { font-size: 15px; color: var(--moar-text-light); line-height: 1.7; margin-bottom: 12px; }
.moar-card .know-more {
    color: var(--moar-blue);
    font-weight: 600;
    font-size: 14px;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 5px;
}
.moar-card .know-more:hover { gap: 8px; }
.moar-card .know-more::after { content: '\\2192'; }

/* Text-only cards (no image) */
.moar-card-text {
    background: #ffffff;
    border-radius: 10px;
    padding: 32px 28px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.05);
    transition: all 0.35s ease;
    height: 100%;
    border: 1px solid var(--moar-border);
}
.moar-card-text:hover { transform: translateY(-4px); box-shadow: 0 10px 30px rgba(0,0,0,0.08); }
.moar-card-text h3 { font-size: 19px; margin-bottom: 12px; }
.moar-card-text p { font-size: 15px; color: var(--moar-text-light); }

/* Dark cards (GCC section) */
.moar-card-dark {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 10px;
    overflow: hidden;
    transition: all 0.35s ease;
    height: 100%;
}
.moar-card-dark:hover { transform: translateY(-4px); background: rgba(255,255,255,0.1); box-shadow: 0 8px 25px rgba(0,0,0,0.2); }
.moar-card-dark .card-img { width: 100%; height: 200px; object-fit: cover; border-radius: 0; }
.moar-card-dark .card-body { padding: 24px; }
.moar-card-dark h3 { color: #fff; font-size: 19px; margin-bottom: 10px; }
.moar-card-dark p { color: rgba(255,255,255,0.75); font-size: 15px; }

/* ── Stats ── */
.moar-stat { text-align: center; padding: 24px 16px; }
.moar-stat .stat-number {
    font-size: 52px;
    font-weight: 900;
    background: var(--moar-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
}
.moar-stat .stat-label { font-size: 15px; color: var(--moar-text-light); font-weight: 500; margin-top: 6px; }

/* ── Team Cards ── */
.moar-team-card {
    text-align: center;
    background: #ffffff;
    border-radius: 10px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.05);
    border: 1px solid var(--moar-border);
    overflow: hidden;
    transition: all 0.35s ease;
}
.moar-team-card:hover { transform: translateY(-4px); box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
.moar-team-card .team-photo {
    width: 100%;
    height: 280px;
    object-fit: cover;
    object-position: top;
}
.moar-team-card .team-info { padding: 20px 16px 24px; }
.moar-team-card h4 { font-size: 17px; font-weight: 700; color: var(--moar-dark); margin-bottom: 4px; }
.moar-team-card .team-role { font-size: 13px; color: var(--moar-blue); font-weight: 600; margin-bottom: 8px; }
.moar-team-card .team-bio { font-size: 13px; color: var(--moar-text-light); line-height: 1.6; padding: 0 8px; }

/* ── Values ── */
.moar-value { text-align: center; padding: 36px 20px; }
.moar-value .value-icon {
    width: 64px; height: 64px;
    background: var(--moar-gradient);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 18px;
    color: #fff; font-size: 26px;
}
.moar-value h4 { font-size: 18px; font-weight: 700; margin-bottom: 8px; }
.moar-value p { font-size: 14px; }

/* ── Industry Tags ── */
.moar-industry {
    background: #ffffff;
    border-radius: 10px;
    padding: 28px 16px;
    text-align: center;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
    border: 1px solid var(--moar-border);
    transition: all 0.3s ease;
}
.moar-industry:hover { transform: translateY(-3px); box-shadow: 0 6px 20px rgba(0,0,0,0.08); border-color: var(--moar-blue); }
.moar-industry .industry-icon { font-size: 36px; margin-bottom: 12px; }
.moar-industry h4 { font-size: 15px; font-weight: 700; color: var(--moar-dark); margin: 0; }

/* ── Steps ── */
.moar-step { text-align: center; position: relative; }
.moar-step .step-img { width: 100%; height: 220px; object-fit: cover; border-radius: 10px; margin-bottom: 20px; }
.moar-step .step-number {
    width: 44px; height: 44px;
    background: var(--moar-gradient);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 14px;
    color: #fff; font-size: 18px; font-weight: 700;
}
.moar-step h3 { font-size: 20px; margin-bottom: 10px; }
.moar-step p { font-size: 15px; }

/* ── CTA Banner ── */
.moar-cta {
    background: var(--moar-gradient);
    padding: 60px 0;
    text-align: center;
}
.moar-cta h2 { color: #fff; font-size: 32px; margin-bottom: 12px; }
.moar-cta p { color: rgba(255,255,255,0.9); font-size: 17px; margin-bottom: 28px; }
.moar-cta .btn { background: #fff !important; color: var(--moar-gray) !important; font-weight: 700; padding: 13px 36px; border-radius: 5px; }
.moar-cta .btn:hover { background: var(--moar-dark) !important; color: #fff !important; }

/* ── Badge / Tag ── */
.moar-badge {
    display: inline-block;
    background: var(--moar-gradient);
    color: #fff;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.5px;
    margin-bottom: 14px;
}

/* ── Contact Form ── */
.moar-form input,.moar-form textarea,.moar-form select {
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 10px 14px;
    font-size: 16px;
    font-family: 'Archivo', sans-serif;
    width: 100%;
    margin-bottom: 14px;
    transition: border-color 0.3s ease;
    background: #fff;
}
.moar-form input:focus,.moar-form textarea:focus,.moar-form select:focus {
    border-color: var(--moar-blue);
    outline: none;
    box-shadow: 0 0 0 3px rgba(37,117,252,0.1);
}

/* ── Footer ── */
footer, #footer, .o_footer {
    background: var(--moar-dark) !important;
    color: rgba(255,255,255,0.75);
    font-size: 14px;
}
footer h5, #footer h5 { color: #fff; font-weight: 700; font-size: 16px; margin-bottom: 16px; }
footer a, #footer a { color: rgba(255,255,255,0.65) !important; font-size: 14px; }
footer a:hover, #footer a:hover { color: var(--moar-blue) !important; }
.o_footer_copyright { background: var(--moar-dark) !important; border-top: 1px solid rgba(255,255,255,0.08); }

/* ── Responsive ── */
@media (max-width: 991px) {
    .moar-hero-img { min-height: 400px; }
    .moar-hero-img h1 { font-size: 32px; }
    h2,.h2 { font-size: 28px; }
    .moar-section { padding: 50px 0; }
}
@media (max-width: 767px) {
    .moar-hero-img { min-height: 350px; }
    .moar-hero-img h1 { font-size: 28px; }
    .moar-hero-img p { font-size: 16px; }
    .moar-stat .stat-number { font-size: 36px; }
    .moar-section { padding: 40px 0; }
    .section-title { margin-bottom: 30px; }
}

/* ── Override Odoo defaults ── */
#wrapwrap { background: #ffffff; }
.oe_structure.oe_empty > section:first-child { padding-top: 0 !important; margin-top: 0 !important; }
#wrap > section:first-child { margin-top: 0 !important; }
"""


# ═══════════════════════════════════════════
# Page HTML with real images
# ═══════════════════════════════════════════

HOMEPAGE_HTML = f"""
<!-- Hero Banner with real image -->
<section class="moar-hero-img" style="background-image: url('{IMAGES["hero_banner"]}');">
    <div class="hero-content">
        <h1>Advice You Can Trust.<br/>Experience You Can Use.</h1>
        <p>Expertise that helps organisations build stronger brands, cultures, and capabilities.</p>
        <a href="/blog" class="btn btn-gradient">Discover Now</a>
    </div>
</section>

<!-- About Section -->
<section class="moar-section">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-lg-6">
                <div class="section-subtitle">ABOUT US</div>
                <h2>Your Partner in Growth</h2>
                <p>We go beyond traditional consulting by working alongside you to set up, scale and optimize your business. With deep expertise in GCC consulting, people advisory, and digital transformation, MOAR Advisory delivers results that matter.</p>
                <p>Headquartered in Bengaluru with a 200+ delivery team through Yitro Global, we blend advisory expertise with hands-on execution to help enterprises establish, operate, and scale global capability centers with measurable outcomes.</p>
                <a href="/about" class="btn btn-primary mt-3">Learn MOAR</a>
            </div>
            <div class="col-lg-6">
                <div class="row">
                    <div class="col-4">
                        <div class="moar-stat">
                            <div class="stat-number">200+</div>
                            <div class="stat-label">Experienced Practitioners</div>
                        </div>
                    </div>
                    <div class="col-4">
                        <div class="moar-stat">
                            <div class="stat-number">10+</div>
                            <div class="stat-label">Industries Served</div>
                        </div>
                    </div>
                    <div class="col-4">
                        <div class="moar-stat">
                            <div class="stat-number">5</div>
                            <div class="stat-label">International Offices</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Services Section with real images -->
<section class="moar-section moar-section-gray">
    <div class="container">
        <div class="section-title">
            <div class="section-subtitle">OUR OFFERINGS</div>
            <h2>What We Do</h2>
            <p>End-to-end advisory services for your strategic growth</p>
        </div>
        <div class="row g-4">
            <div class="col-lg-4 col-md-6">
                <div class="moar-card">
                    <img src="{IMAGES['company_setup']}" alt="Company Setup &amp; Finance" class="card-img"/>
                    <div class="card-body">
                        <h3>Company Setup &amp; Finance</h3>
                        <p>Simplified entry and scalable operations. We assist companies in establishing foundational frameworks for compliance, finance, and operations in new markets.</p>
                        <a href="/company-setup-finance" class="know-more">Know More</a>
                    </div>
                </div>
            </div>
            <div class="col-lg-4 col-md-6">
                <div class="moar-card">
                    <img src="{IMAGES['people_advisory']}" alt="People Advisory" class="card-img"/>
                    <div class="card-body">
                        <h3>People Advisory</h3>
                        <p>Talent and people advisory services for global success. We create strong talent strategies, build leadership and shape company culture for growth.</p>
                        <a href="/people-advisory" class="know-more">Know More</a>
                    </div>
                </div>
            </div>
            <div class="col-lg-4 col-md-6">
                <div class="moar-card">
                    <img src="{IMAGES['m_select']}" alt="M-SELECT Recruitment" class="card-img"/>
                    <div class="card-body">
                        <h3>M-SELECT — Recruitment</h3>
                        <p>Strategic recruitment that powers your GCC success. AI-driven insights, practitioner expertise, and dedicated account management.</p>
                        <a href="/m-select" class="know-more">Know More</a>
                    </div>
                </div>
            </div>
            <div class="col-lg-4 col-md-6">
                <div class="moar-card">
                    <img src="{IMAGES['m_power']}" alt="M-POWER Employer Branding" class="card-img"/>
                    <div class="card-body">
                        <h3>M-POWER — Employer Branding</h3>
                        <p>Strategic communications that shape exceptional workplaces. We strengthen employer brands, attract talent, and deliver measurable impact.</p>
                        <a href="/m-power" class="know-more">Know More</a>
                    </div>
                </div>
            </div>
            <div class="col-lg-4 col-md-6">
                <div class="moar-card">
                    <img src="{IMAGES['tech_digital']}" alt="Technology &amp; Digital" class="card-img"/>
                    <div class="card-body">
                        <h3>Technology &amp; Digital Transformation</h3>
                        <p>Reimagining technology as a catalyst for enterprise growth. Modern IT architecture with strategic transformation for agility and resilience.</p>
                        <a href="/technology-digital" class="know-more">Know More</a>
                    </div>
                </div>
            </div>
            <div class="col-lg-4 col-md-6">
                <div class="moar-card">
                    <img src="{IMAGES['advisory']}" alt="Advisory Services" class="card-img"/>
                    <div class="card-body">
                        <h3>Advisory Services</h3>
                        <p>Helping companies set up, scale, and operate with the right insight and leadership in place. Research, planning, and experienced leadership.</p>
                        <a href="/advisory-services" class="know-more">Know More</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- GCC Section with images -->
<section class="moar-section moar-section-dark">
    <div class="container">
        <div class="section-title">
            <div class="section-subtitle" style="-webkit-text-fill-color: rgba(255,255,255,0.6);">GLOBAL CAPABILITY CENTERS</div>
            <h2>Global Enterprise &amp; Capability Hubs</h2>
            <p>Comprehensive GCC solutions tailored to your growth stage</p>
        </div>
        <div class="row g-4">
            <div class="col-lg-4">
                <div class="moar-card-dark">
                    <img src="{IMAGES['bot']}" alt="BOT" class="card-img"/>
                    <div class="card-body">
                        <h3>BOT — Build, Operate &amp; Transfer</h3>
                        <p>We build and operate your GCC, then transfer full ownership once it's mature and self-sustaining. Ideal for low-risk market entry.</p>
                    </div>
                </div>
            </div>
            <div class="col-lg-4">
                <div class="moar-card-dark">
                    <img src="{IMAGES['gcc_service']}" alt="GCC as a Service" class="card-img"/>
                    <div class="card-body">
                        <h3>GCC as a Service</h3>
                        <p>A fully managed model where we handle everything from infrastructure to talent, letting you focus on outcomes.</p>
                    </div>
                </div>
            </div>
            <div class="col-lg-4">
                <div class="moar-card-dark">
                    <img src="{IMAGES['assisted_gcc']}" alt="Assisted GCC" class="card-img"/>
                    <div class="card-body">
                        <h3>Assisted GCC</h3>
                        <p>For organizations that want to own the journey but need expert guidance at every step. Strategic support with full control.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Industries -->
<section class="moar-section">
    <div class="container">
        <div class="section-title">
            <div class="section-subtitle">INDUSTRIES</div>
            <h2>Industries We Serve</h2>
        </div>
        <div class="row g-3 justify-content-center">
            <div class="col-lg-2 col-md-4 col-6"><div class="moar-industry"><div class="industry-icon">&#x1F6D2;</div><h4>Retail</h4></div></div>
            <div class="col-lg-2 col-md-4 col-6"><div class="moar-industry"><div class="industry-icon">&#x1F3ED;</div><h4>Manufacturing</h4></div></div>
            <div class="col-lg-2 col-md-4 col-6"><div class="moar-industry"><div class="industry-icon">&#x1F4B0;</div><h4>Financial Services</h4></div></div>
            <div class="col-lg-2 col-md-4 col-6"><div class="moar-industry"><div class="industry-icon">&#x1F3E5;</div><h4>Healthcare</h4></div></div>
            <div class="col-lg-2 col-md-4 col-6"><div class="moar-industry"><div class="industry-icon">&#x2708;&#xFE0F;</div><h4>Aviation</h4></div></div>
        </div>
    </div>
</section>

<!-- Values -->
<section class="moar-section moar-section-gray">
    <div class="container">
        <div class="section-title">
            <div class="section-subtitle">OUR VALUES</div>
            <h2>The Way We Operate</h2>
        </div>
        <div class="row g-4">
            <div class="col-lg-3 col-md-6"><div class="moar-value"><div class="value-icon">&#x2728;</div><h4>Simplicity</h4><p>We cut through complexity to deliver clear, actionable guidance.</p></div></div>
            <div class="col-lg-3 col-md-6"><div class="moar-value"><div class="value-icon">&#x1F3AF;</div><h4>Credibility</h4><p>Our practitioners bring deep industry experience you can trust.</p></div></div>
            <div class="col-lg-3 col-md-6"><div class="moar-value"><div class="value-icon">&#x1F91D;</div><h4>Authenticity</h4><p>Genuine partnerships built on transparency and honest counsel.</p></div></div>
            <div class="col-lg-3 col-md-6"><div class="moar-value"><div class="value-icon">&#x2705;</div><h4>Accountability</h4><p>We own outcomes and deliver on our commitments, every time.</p></div></div>
        </div>
    </div>
</section>

<!-- Why MOAR -->
<section class="moar-section">
    <div class="container">
        <div class="section-title">
            <div class="section-subtitle">WHY US</div>
            <h2>Why MOAR Advisory</h2>
        </div>
        <div class="row g-4">
            <div class="col-lg-3 col-md-6"><div class="moar-card-text text-center"><h3>People, Trust &amp; Transparency</h3><p>Our relationships are built on openness and mutual respect.</p></div></div>
            <div class="col-lg-3 col-md-6"><div class="moar-card-text text-center"><h3>Practitioners, Not Consultants</h3><p>We work as an extension of your team with hands-on execution.</p></div></div>
            <div class="col-lg-3 col-md-6"><div class="moar-card-text text-center"><h3>Tailored Solutions</h3><p>No templates. Every engagement designed around your unique needs.</p></div></div>
            <div class="col-lg-3 col-md-6"><div class="moar-card-text text-center"><h3>Speed to Market</h3><p>Proven frameworks and execution speed to accelerate your timeline.</p></div></div>
        </div>
    </div>
</section>

<!-- How We Work with images -->
<section class="moar-section moar-section-gray">
    <div class="container">
        <div class="section-title">
            <div class="section-subtitle">OUR PROCESS</div>
            <h2>How We Work</h2>
        </div>
        <div class="row g-4">
            <div class="col-lg-4">
                <div class="moar-step">
                    <img src="{IMAGES['roadmap']}" alt="Build the Roadmap" class="step-img"/>
                    <div class="step-number">1</div>
                    <h3>Build the Roadmap</h3>
                    <p>We assess your needs, understand your goals, and create a strategic plan tailored to your growth objectives.</p>
                </div>
            </div>
            <div class="col-lg-4">
                <div class="moar-step">
                    <img src="{IMAGES['execution']}" alt="Partner in Execution" class="step-img"/>
                    <div class="step-number">2</div>
                    <h3>Partner in Execution</h3>
                    <p>Our team embeds with yours, bringing expertise and capability to drive implementation at speed.</p>
                </div>
            </div>
            <div class="col-lg-4">
                <div class="moar-step">
                    <img src="{IMAGES['deliver']}" alt="Deliver &amp; Execute" class="step-img"/>
                    <div class="step-number">3</div>
                    <h3>Deliver &amp; Sustain</h3>
                    <p>We ensure sustainable outcomes with ongoing support, knowledge transfer, and capability building.</p>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Leadership with real photos -->
<section class="moar-section">
    <div class="container">
        <div class="section-title">
            <div class="section-subtitle">OUR TEAM</div>
            <h2>Leadership Team</h2>
        </div>
        <div class="row g-4">
            <div class="col-lg-3 col-md-6"><div class="moar-team-card"><img src="{IMAGES['mohith']}" alt="Mohith Mohan" class="team-photo"/><div class="team-info"><h4>Mohith Mohan</h4><div class="team-role">Founder &amp; CEO</div><p class="team-bio">20+ years at Fidelity, Yahoo, Lowe's, HBC. Builds GCCs and employer brands.</p></div></div></div>
            <div class="col-lg-3 col-md-6"><div class="moar-team-card"><img src="{IMAGES['mukesh']}" alt="Mukesh Kedia" class="team-photo"/><div class="team-info"><h4>Mukesh Kedia</h4><div class="team-role">Co-Founder &amp; CFO</div><p class="team-bio">19+ years at KPMG, HBC, Giant Eagle. Expertise in fundraising, M&amp;A, compliance.</p></div></div></div>
            <div class="col-lg-3 col-md-6"><div class="moar-team-card"><img src="{IMAGES['santosh']}" alt="Santosh Gnanaprakash" class="team-photo"/><div class="team-info"><h4>Santosh Gnanaprakash</h4><div class="team-role">General Counsel, Legal</div><p class="team-bio">23+ years in litigation, consulting. ICSI member. GCC and ITeS expertise.</p></div></div></div>
            <div class="col-lg-3 col-md-6"><div class="moar-team-card"><img src="{IMAGES['anneka']}" alt="Anneka Darashah" class="team-photo"/><div class="team-info"><h4>Anneka Darashah</h4><div class="team-role">Head — People Advisory</div><p class="team-bio">20+ years in global HR. Talent function scaling and team leadership.</p></div></div></div>
            <div class="col-lg-3 col-md-6"><div class="moar-team-card"><img src="{IMAGES['sonia']}" alt="Sonia Sharma" class="team-photo"/><div class="team-info"><h4>Sonia Sharma</h4><div class="team-role">Head — Marketing</div><p class="team-bio">15+ years at ING, Marriott, Quess. Brand storytelling and digital strategy.</p></div></div></div>
            <div class="col-lg-3 col-md-6"><div class="moar-team-card"><img src="{IMAGES['rahul']}" alt="Rahul Virk" class="team-photo"/><div class="team-info"><h4>Rahul Virk</h4><div class="team-role">Head, Talent Strategy — M Select</div><p class="team-bio">20+ years in talent acquisition. GCC, technology, banking expertise.</p></div></div></div>
            <div class="col-lg-3 col-md-6"><div class="moar-team-card"><img src="{IMAGES['minoo']}" alt="Minoo Verma" class="team-photo"/><div class="team-info"><h4>Minoo Verma</h4><div class="team-role">Head — Communications</div><p class="team-bio">15+ years in employer branding, stakeholder engagement, digital strategy.</p></div></div></div>
            <div class="col-lg-3 col-md-6"><div class="moar-team-card"><img src="{IMAGES['harsha']}" alt="Harsha Nandakumar" class="team-photo"/><div class="team-info"><h4>Harsha Nandakumar</h4><div class="team-role">Director Programs &amp; Customer Success</div><p class="team-bio">15+ years in digital commerce, marketplace ops. Hudson's Bay, Swiggy, Bigbasket.</p></div></div></div>
        </div>
    </div>
</section>

<!-- CTA -->
<section class="moar-cta">
    <div class="container">
        <h2>Ready to Scale Your Business?</h2>
        <p>Talk to our experts and explore faster ways to grow.</p>
        <a href="/contactus" class="btn btn-lg">Get in Touch</a>
    </div>
</section>
"""

ABOUT_HTML = f"""
<section class="moar-hero-img" style="background-image: url('{IMAGES["about_banner"]}');">
    <div class="hero-content">
        <h1>About MOAR Advisory</h1>
        <p>Advice You Can Trust, Experience You Can Use.</p>
    </div>
</section>

<section class="moar-section">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-lg-7">
                <div class="section-subtitle">WHO WE ARE</div>
                <h2>Built by Practitioners</h2>
                <p>MOAR Advisory is built by senior practitioners who have led transformation across industries, startups, and Fortune 500 companies. Headquartered in Bengaluru with a 200+ delivery team through Yitro Global, we blend advisory expertise with hands-on execution.</p>
                <p>Our focus is helping enterprises establish, operate, and scale global capability centers (GCCs) into strategic hubs that drive innovation — not just efficiency. We combine deep industry knowledge with practical, market-grounded counsel to deliver measurable outcomes.</p>
                <a href="/contactus" class="btn btn-primary mt-3">Partner With Us</a>
            </div>
            <div class="col-lg-5">
                <div class="row">
                    <div class="col-6"><div class="moar-stat"><div class="stat-number">10+</div><div class="stat-label">Industries Served Globally</div></div></div>
                    <div class="col-6"><div class="moar-stat"><div class="stat-number">200+</div><div class="stat-label">Experienced Practitioners</div></div></div>
                    <div class="col-12"><div class="moar-stat"><div class="stat-number">5</div><div class="stat-label">International Offices</div></div></div>
                </div>
            </div>
        </div>
    </div>
</section>

<section class="moar-section moar-section-gray">
    <div class="container">
        <div class="section-title"><div class="section-subtitle">OUR REACH</div><h2>Global Footprint</h2></div>
        <div class="text-center mb-4"><img src="{IMAGES['map']}" alt="Global Map" style="max-width: 700px; width: 100%; border-radius: 12px;"/></div>
        <div class="row g-3 justify-content-center">
            <div class="col-lg-3 col-md-6"><div class="moar-card-text text-center"><h3>&#x1F1FA;&#x1F1F8; Texas</h3><p>North America operations</p></div></div>
            <div class="col-lg-3 col-md-6"><div class="moar-card-text text-center"><h3>&#x1F1EE;&#x1F1F3; Bangalore</h3><p>Global headquarters</p></div></div>
            <div class="col-lg-3 col-md-6"><div class="moar-card-text text-center"><h3>&#x1F1EE;&#x1F1F3; Chennai</h3><p>South India operations</p></div></div>
            <div class="col-lg-3 col-md-6"><div class="moar-card-text text-center"><h3>&#x1F1F5;&#x1F1ED; Manila</h3><p>Southeast Asia operations</p></div></div>
        </div>
    </div>
</section>

<section class="moar-cta"><div class="container"><h2>Partner With Us</h2><p>Let's build something exceptional together.</p><a href="/contactus" class="btn btn-lg">Get in Touch</a></div></section>
"""

LEADERS_HTML = f"""
<section class="moar-hero-gradient">
    <div class="container"><h1>Our Leaders</h1><p>Senior practitioners driving transformation across industries</p></div>
</section>

<section class="moar-section">
    <div class="container">
        <div class="section-title"><div class="section-subtitle">LEADERSHIP</div><h2>Leadership Team</h2></div>
        <div class="row g-4">
            <div class="col-lg-4 col-md-6"><div class="moar-team-card"><img src="{IMAGES['mohith']}" alt="Mohith Mohan" class="team-photo"/><div class="team-info"><h4>Mohith Mohan</h4><div class="team-role">Founder &amp; CEO</div><p class="team-bio">With 20+ years of experience at Fidelity, Yahoo, Lowe's, and HBC, Mohith specializes in building GCCs and employer brands that drive organizational growth.</p></div></div></div>
            <div class="col-lg-4 col-md-6"><div class="moar-team-card"><img src="{IMAGES['mukesh']}" alt="Mukesh Kedia" class="team-photo"/><div class="team-info"><h4>Mukesh Kedia</h4><div class="team-role">Co-Founder &amp; CFO</div><p class="team-bio">19+ years of experience at KPMG, HBC, and Giant Eagle with deep expertise in fundraising, M&amp;A, compliance, and financial strategy.</p></div></div></div>
            <div class="col-lg-4 col-md-6"><div class="moar-team-card"><img src="{IMAGES['santosh']}" alt="Santosh Gnanaprakash" class="team-photo"/><div class="team-info"><h4>Santosh Gnanaprakash</h4><div class="team-role">General Counsel, Legal</div><p class="team-bio">23+ years in litigation and consulting. ICSI member with deep expertise in GCC legal frameworks and ITeS regulations.</p></div></div></div>
            <div class="col-lg-4 col-md-6"><div class="moar-team-card"><img src="{IMAGES['anneka']}" alt="Anneka Darashah" class="team-photo"/><div class="team-info"><h4>Anneka Darashah</h4><div class="team-role">Head — People Advisory</div><p class="team-bio">20+ years in global HR with expertise in talent function scaling, team leadership, and organizational development.</p></div></div></div>
            <div class="col-lg-4 col-md-6"><div class="moar-team-card"><img src="{IMAGES['sonia']}" alt="Sonia Sharma" class="team-photo"/><div class="team-info"><h4>Sonia Sharma</h4><div class="team-role">Head — Marketing</div><p class="team-bio">15+ years at ING, Marriott, and Quess with expertise in brand storytelling, digital strategy, and employer brand marketing.</p></div></div></div>
            <div class="col-lg-4 col-md-6"><div class="moar-team-card"><img src="{IMAGES['rahul']}" alt="Rahul Virk" class="team-photo"/><div class="team-info"><h4>Rahul Virk</h4><div class="team-role">Head, Talent Strategy — M Select</div><p class="team-bio">20+ years in talent acquisition across GCC, technology, and banking sectors.</p></div></div></div>
            <div class="col-lg-4 col-md-6"><div class="moar-team-card"><img src="{IMAGES['minoo']}" alt="Minoo Verma" class="team-photo"/><div class="team-info"><h4>Minoo Verma</h4><div class="team-role">Head — Communications</div><p class="team-bio">15+ years of experience in employer branding, stakeholder engagement, and digital communications strategy.</p></div></div></div>
            <div class="col-lg-4 col-md-6"><div class="moar-team-card"><img src="{IMAGES['harsha']}" alt="Harsha Nandakumar" class="team-photo"/><div class="team-info"><h4>Harsha Nandakumar</h4><div class="team-role">Director Programs &amp; Customer Success</div><p class="team-bio">15+ years in digital commerce and marketplace operations at Hudson's Bay, Swiggy, and Bigbasket.</p></div></div></div>
        </div>
    </div>
</section>

<section class="moar-section moar-section-gray">
    <div class="container">
        <div class="section-title"><div class="section-subtitle">ADVISORS</div><h2>Advisory Committee</h2></div>
        <div class="row g-4 justify-content-center">
            <div class="col-lg-4 col-md-6"><div class="moar-team-card"><img src="{IMAGES['mahendra']}" alt="Mahendra Dhillon" class="team-photo"/><div class="team-info"><h4>Mahendra Dhillon</h4><div class="team-role">Advisory Committee</div></div></div></div>
            <div class="col-lg-4 col-md-6"><div class="moar-team-card"><img src="{IMAGES['gagan']}" alt="Gagan Ganapathy" class="team-photo"/><div class="team-info"><h4>Gagan Ganapathy</h4><div class="team-role">Advisory Committee</div></div></div></div>
            <div class="col-lg-4 col-md-6"><div class="moar-team-card"><img src="{IMAGES['tom']}" alt="Tom Ott" class="team-photo"/><div class="team-info"><h4>Tom Ott</h4><div class="team-role">Advisory Committee</div></div></div></div>
        </div>
    </div>
</section>

<section class="moar-cta"><div class="container"><h2>Join Our Team</h2><p>We're always looking for exceptional talent.</p><a href="/jobs" class="btn btn-lg">View Open Positions</a></div></section>
"""


def make_service_page(title, tagline, intro, banner_img, services, target_segments=None):
    services_html = ""
    for name, desc in services:
        services_html += f"""
            <div class="col-lg-6"><div class="moar-card-text"><h3>{name}</h3><p>{desc}</p></div></div>"""

    segments_html = ""
    if target_segments:
        seg_cards = ""
        for img_url, name, desc in target_segments:
            seg_cards += f"""
            <div class="col-lg-3 col-md-6"><div class="moar-card"><img src="{img_url}" alt="{name}" class="card-img"/><div class="card-body"><h3>{name}</h3><p>{desc}</p></div></div></div>"""
        segments_html = f"""
<section class="moar-section moar-section-gray">
    <div class="container">
        <div class="section-title"><div class="section-subtitle">CLIENTS</div><h2>Who We Support</h2></div>
        <div class="row g-4">{seg_cards}</div>
    </div>
</section>"""

    return f"""
<section class="moar-hero-img" style="background-image: url('{banner_img}');">
    <div class="hero-content"><h1>{title}</h1><p>{tagline}</p></div>
</section>

<section class="moar-section">
    <div class="container"><div class="row justify-content-center"><div class="col-lg-10"><p style="font-size:18px; text-align:center; color: var(--moar-text-light);">{intro}</p></div></div></div>
</section>

<section class="moar-section moar-section-gray">
    <div class="container">
        <div class="section-title"><div class="section-subtitle">SERVICES</div><h2>What We Offer</h2></div>
        <div class="row g-4">{services_html}</div>
    </div>
</section>
{segments_html}
<section class="moar-cta"><div class="container"><h2>Get a Call Back</h2><p>Talk to our experts and explore faster ways to scale your business.</p><a href="/contactus" class="btn btn-lg">Contact Us</a></div></section>
"""


COMPANY_SETUP_HTML = make_service_page(
    "Company Setup &amp; Finance", "Simplified Entry. Scalable Operations.",
    "Organizations entering new markets require swift compliance and structured operations. We assist companies in establishing foundational frameworks, enabling immediate growth focus. Our expertise in global business services and GCC consulting supports sustainable operations.",
    IMAGES["cs_banner"],
    [
        ("Legal Entity Setup", "Entity structuring, registration, and incorporation adapted to operational models and jurisdictional requirements."),
        ("Compliance &amp; Regulations", "Fulfillment of local legal and regulatory obligations, including licensing, filings, and governance structures."),
        ("Finance &amp; Accounting Setup", "Finance functions, accounting systems, reporting frameworks, and internal control mechanisms."),
        ("Tax Advisory &amp; Strategy", "Strategic tax structuring and continuous advisory addressing compliance, efficiency, and risk mitigation."),
        ("Banking &amp; Treasury", "Corporate bank account establishment, treasury operations, and initial capital configuration."),
        ("Procurement as a Service", "Procurement processes from vendor onboarding through sourcing and spend management."),
        ("Technology &amp; Tools Enablement", "Deploying core platforms supporting finance, procurement, and compliance operations."),
        ("Ongoing Operational Support", "Post-setup advisory and execution across finance, tax, and compliance for stability and expansion."),
    ],
    [
        (IMAGES["cs_gcc"], "GCCs &amp; Shared Services", "Organizations entering new geographies and establishing capability centers."),
        (IMAGES["cs_startup"], "Startups", "Requiring expert guidance from trusted advisors for initial operations."),
        (IMAGES["cs_sme"], "SMEs", "Seeking comprehensive advisory and global services for growth and scaling."),
        (IMAGES["cs_corp"], "Corporate Teams", "Launching new entities, business units, or functions."),
    ]
)

PEOPLE_ADVISORY_HTML = make_service_page(
    "People Advisory", "Talent and People Advisory Services for Global Success",
    "The success of any organization starts with its people. We work with businesses to create strong talent strategies, build leadership and shape company culture for growth. From growing teams and setting up global business services hubs, to developing future leaders.",
    IMAGES["people_advisory"],
    [
        ("Workforce Strategy &amp; Talent Planning", "Workforce planning aligned to business growth goals. Talent strategy for scaling teams across markets. Leadership planning for future readiness."),
        ("Talent Acquisition &amp; Employer Branding", "EVP development for talent attraction. Talent engagement and recruitment marketing. Onboarding programs that drive retention and productivity."),
        ("Organization Culture &amp; Change Advisory", "Culture design aligned to business strategy and values. Change management for transformations. DEI strategy integration for inclusive workplaces."),
        ("HR Transformation &amp; Capability Building", "HR operating model design for scaling organizations. Digital enablement of HR processes and systems. Capability building for HR teams."),
        ("Executive Coaching", "Personalized one-on-one coaching for founders, CXOs, and senior leaders. Building clarity, resilience, communication, and influence."),
    ]
)

MSELECT_HTML = make_service_page(
    "M-SELECT — Recruitment", "Strategic Recruitment That Powers Your GCC Success",
    "M-SELECT redefines recruitment for Global Capability Centers. By combining AI-driven insights, practitioner expertise, and dedicated account management, we deliver the right talent — aligned with your skills, culture, and vision — every time.",
    IMAGES["ms_banner"],
    [
        ("High-Impact Team Building", "Accelerate high-impact teams in tech, analytics, and operations with targeted talent mapping and acquisition strategies."),
        ("Personalized Candidate Journey", "Deliver a personalized candidate journey powered by subject matter experts who understand your industry and culture."),
        ("Employer Brand Integration", "Elevate your employer brand to attract and retain top talent through authentic storytelling and strategic positioning."),
        ("End-to-End Hiring", "Intelligent, fully aligned with your business goals — from talent mapping to onboarding. Build smarter teams and drive growth."),
    ]
)

MPOWER_HTML = make_service_page(
    "M-POWER — Employer Branding", "Strategic Communications That Shape Exceptional Workplaces",
    "We partner with organizations to strengthen employer brands, attract and retain talent, and deliver measurable impact through strategic communications powered by our global business services expertise.",
    IMAGES["m_power"],
    [
        ("Employer Branding &amp; EVP", "Building your reputation as an employer of choice. EVP creation and activation, recruitment marketing, DEI integration, and employee advocacy programs."),
        ("Brand &amp; Reputation Strategy", "Define and elevate your corporate identity. Brand audits, positioning frameworks, visual identity guidelines, and content strategy."),
        ("Go-to-Market Communications", "Product launches and market entries. Messaging strategy, stakeholder communication, sales enablement, and PR outreach."),
        ("Digital Employer Brand Campaigns", "SEO, content marketing, social media strategy, thought leadership, event marketing, and media relations."),
        ("Internal Communications", "Workforce alignment and inspiration. Leadership messaging, culture-building campaigns, DEI communications, and change communication."),
    ]
)

TECH_DIGITAL_HTML = make_service_page(
    "Technology &amp; Digital Transformation", "Reimagining Technology as a Catalyst for Enterprise Growth",
    "We help organizations from Global Capability Centers to SMEs build strong digital and infrastructure foundations. Combining modern IT architecture with strategic transformation to drive agility, resilience, and long-term value.",
    IMAGES["tech_digital"],
    [
        ("Enterprise IT Infrastructure", "Design, implement, and manage IT environments supporting global collaboration, business continuity and operational efficiency across cloud, hybrid, and on-premise systems."),
        ("Cloud Strategy &amp; Migration", "Public, private, and hybrid cloud strategy. Network and connectivity optimization. Infrastructure governance and compliance."),
        ("Digital Transformation Strategy", "Move from siloed, project-based approaches to product-centric operating models. Scaled Agile and DevOps adoption."),
        ("Cyber-Resilience &amp; Continuity", "Operational continuity planning, technology portfolio rationalization, and value stream mapping for delivery alignment."),
    ]
)

ADVISORY_HTML = make_service_page(
    "Advisory Services", "The Right Insight and Leadership for Growth",
    "We support organizations at various growth stages — from early-stage startups entering new markets to established businesses building regional hubs. We function as an extended team, providing research, planning, and experienced leadership to accelerate growth.",
    IMAGES["advisory"],
    [
        ("Feasibility Study", "Market validation before expansion — cost analysis, talent availability assessment, legal and regulatory risk identification, and scalability evaluation."),
        ("Location Services", "Geographic expansion guidance including city/country comparative analysis, local compliance, talent access, and ecosystem partnerships."),
        ("Leadership as a Service", "Interim executive support for market entry — office management, team building, operations setup, and leadership continuity during transitions."),
        ("Multi-Industry Expertise", "Practical, market-grounded counsel across industries. Execution support with leadership experience, not just recommendations."),
    ]
)

CASE_STUDIES_HTML = f"""
<section class="moar-hero-gradient">
    <div class="container"><h1>Case Studies</h1><p>Driving Growth Through Strategic Advisory</p></div>
</section>

<section class="moar-section">
    <div class="container">
        <div class="row g-4">
            <div class="col-lg-6"><div class="moar-card"><img src="{IMAGES['case_packaging']}" alt="Global Leader in Packaging" class="card-img"/><div class="card-body"><span class="moar-badge">Packaging</span><h3>Global Leader in Packaging</h3><p>A global leader in packaging and industrial products sought to establish a Global Capability Centre to drive digital transformation and technology innovation.</p><a href="#" class="know-more">Read More</a></div></div></div>
            <div class="col-lg-6"><div class="moar-card"><img src="{IMAGES['case_sonoco']}" alt="GCC Setup" class="card-img"/><div class="card-body"><span class="moar-badge">Manufacturing</span><h3>GCC Setup — Performance Hub</h3><p>Comprehensive GCC setup enabling a global manufacturer to build a high-performance capability center driving operational excellence and innovation.</p><a href="#" class="know-more">Read More</a></div></div></div>
            <div class="col-lg-6"><div class="moar-card-text"><span class="moar-badge">Retail</span><h3>Retail Transformation</h3><p>Improved inventory management and operational efficiency through strategic GCC establishment and technology-driven process optimization.</p></div></div>
            <div class="col-lg-6"><div class="moar-card-text"><span class="moar-badge">Financial Services</span><h3>Digital Strategy for Financial Services</h3><p>Developed and executed a comprehensive digital strategy driving technology modernization and customer experience transformation.</p></div></div>
            <div class="col-lg-6"><div class="moar-card-text"><span class="moar-badge">Healthcare</span><h3>Healthcare Staff Retention</h3><p>Designed people advisory programs that significantly improved staff retention and organizational culture within a major healthcare provider.</p></div></div>
            <div class="col-lg-6"><div class="moar-card-text"><span class="moar-badge">Aviation</span><h3>Aviation Operations Optimization</h3><p>Streamlined flight operations and technology infrastructure, improving efficiency and establishing scalable operational frameworks.</p></div></div>
        </div>
    </div>
</section>

<section class="moar-cta"><div class="container"><h2>Let's Write Your Success Story</h2><p>Partner with MOAR Advisory to drive measurable outcomes.</p><a href="/contactus" class="btn btn-lg">Get in Touch</a></div></section>
"""

MEDIA_HTML = f"""
<section class="moar-hero-gradient">
    <div class="container"><h1>Media</h1><p>Conversations That Shape Decisions</p></div>
</section>

<section class="moar-section">
    <div class="container">
        <div class="section-title"><div class="section-subtitle">CONTENT</div><h2>Podcasts &amp; Insights</h2></div>
        <div class="row g-4">
            <div class="col-lg-4"><div class="moar-card-text"><h3>&#x1F3A7; Conversations that Shape Decisions</h3><p>Our flagship podcast series exploring GCC strategy, leadership, and the future of global capability centers.</p><a href="/blog" class="btn btn-primary mt-3">Listen Now</a></div></div>
            <div class="col-lg-4"><div class="moar-card-text"><h3>&#x1F4F0; Industry Insights</h3><p>Deep dives into trends shaping business advisory, people strategy, and digital transformation.</p><a href="/blog" class="btn btn-primary mt-3">Read More</a></div></div>
            <div class="col-lg-4"><div class="moar-card-text"><h3>&#x1F3AC; Video Content</h3><p>Expert discussions, webinar recordings, and thought leadership videos from our leadership team.</p><a href="https://www.youtube.com/@MOARAdvisory" class="btn btn-primary mt-3" target="_blank">YouTube</a></div></div>
        </div>
    </div>
</section>

<section class="moar-section moar-section-gray">
    <div class="container">
        <div class="section-title"><div class="section-subtitle">EVENTS</div><h2>Upcoming Events</h2></div>
        <div class="row justify-content-center"><div class="col-lg-8"><div class="moar-card-text text-center"><h3>GCC Strategy Webinar 2026</h3><p><strong>April 15, 2026 | 10:00 AM - 11:30 AM IST</strong></p><p>Join our leadership for an insightful session on the evolving GCC landscape and talent strategies for India.</p><a href="/event" class="btn btn-gradient mt-3">Register Now</a></div></div></div>
    </div>
</section>

<section class="moar-cta"><div class="container"><h2>Stay Connected</h2><p>Follow us for the latest insights and updates.</p><a href="/contactus" class="btn btn-lg">Subscribe</a></div></section>
"""


PAGES = [
    {"name": "About - Overview", "url": "/about", "html": ABOUT_HTML},
    {"name": "Our Leaders", "url": "/our-leaders", "html": LEADERS_HTML},
    {"name": "Company Setup & Finance", "url": "/company-setup-finance", "html": COMPANY_SETUP_HTML},
    {"name": "People Advisory", "url": "/people-advisory", "html": PEOPLE_ADVISORY_HTML},
    {"name": "M-SELECT Recruitment", "url": "/m-select", "html": MSELECT_HTML},
    {"name": "M-POWER Employer Branding", "url": "/m-power", "html": MPOWER_HTML},
    {"name": "Technology & Digital Transformation", "url": "/technology-digital", "html": TECH_DIGITAL_HTML},
    {"name": "Advisory Services", "url": "/advisory-services", "html": ADVISORY_HTML},
    {"name": "Case Studies", "url": "/case-studies", "html": CASE_STUDIES_HTML},
    {"name": "Media", "url": "/media", "html": MEDIA_HTML},
]


def main():
    _url, _db, uid, password, models = connect_odoo()

    # ── Step 1: Update Custom CSS ──
    print("\n=== UPDATING CUSTOM CSS ===")
    css_views = models.execute_kw(
        DB, uid, password, "ir.ui.view", "search",
        [[["key", "=", "moar_advisory.custom_css_inject"]]]
    )
    layout_views = models.execute_kw(
        DB, uid, password, "ir.ui.view", "search_read",
        [[["key", "=", "website.layout"]]],
        {"fields": ["id"], "limit": 1}
    )
    inherit_arch = f"""<data inherit_id="{layout_views[0]['id']}">
    <xpath expr="//head" position="inside">
        <style>
{CUSTOM_CSS}
        </style>
    </xpath>
</data>"""

    if css_views:
        models.execute_kw(DB, uid, password, "ir.ui.view", "write",
            [css_views, {"arch_db": inherit_arch}])
        print(f"  Updated CSS view (ID: {css_views[0]})")
    else:
        css_id = models.execute_kw(DB, uid, password, "ir.ui.view", "create", [{
            "name": "MOAR Advisory Custom CSS",
            "type": "qweb",
            "key": "moar_advisory.custom_css_inject",
            "inherit_id": layout_views[0]["id"],
            "arch_db": inherit_arch,
            "website_id": 1,
            "active": True,
        }])
        print(f"  Created CSS view (ID: {css_id})")

    # ── Step 2: Update Homepage ──
    print("\n=== UPDATING HOMEPAGE ===")
    # Find all homepage views and update the one Odoo actually serves
    homepage_views = models.execute_kw(
        DB, uid, password, "ir.ui.view", "search_read",
        [[["key", "=", "website.homepage"]]],
        {"fields": ["id", "website_id"], "order": "id"}
    )
    new_arch = f"""<t name="Homepage" t-name="website.homepage">
    <t t-call="website.layout">
        <t t-set="pageName" t-value="'homepage'"/>
        <div id="wrap">
            {HOMEPAGE_HTML}
        </div>
    </t>
</t>"""
    for view in homepage_views:
        models.execute_kw(DB, uid, password, "ir.ui.view", "write",
            [[view["id"]], {"arch_db": new_arch}])
        print(f"  Updated homepage view (ID: {view['id']}, website: {view['website_id']})")

    # ── Step 3: Update All Pages ──
    print("\n=== UPDATING ALL PAGES ===")
    for page_config in PAGES:
        page_name = page_config["name"]
        page_url = page_config["url"]
        page_html = page_config["html"]

        existing = models.execute_kw(
            DB, uid, password, "website.page", "search_read",
            [[["url", "=", page_url], ["website_id", "=", 1]]],
            {"fields": ["id", "view_id"]}
        )

        view_arch = f"""<t name="{page_name}" t-name="website.page_{page_url.strip('/').replace('-','_').replace('/','_')}">
    <t t-call="website.layout">
        <div id="wrap">
            {page_html}
        </div>
    </t>
</t>"""

        if existing:
            view_id = existing[0]["view_id"][0]
            models.execute_kw(DB, uid, password, "ir.ui.view", "write",
                [[view_id], {"arch_db": view_arch}])
            print(f"  Updated: {page_name} ({page_url})")
        else:
            view_key = f"website.page_{page_url.strip('/').replace('-','_').replace('/','_')}"
            view_id = models.execute_kw(DB, uid, password, "ir.ui.view", "create", [{
                "name": page_name, "type": "qweb", "key": view_key,
                "arch_db": view_arch, "website_id": 1,
            }])
            page_id = models.execute_kw(DB, uid, password, "website.page", "create", [{
                "name": page_name, "url": page_url, "view_id": view_id,
                "website_id": 1, "is_published": True, "website_published": True,
            }])
            print(f"  Created: {page_name} ({page_url})")

        time.sleep(0.5)

    print("\n=== REBUILD COMPLETE ===")
    print(f"Site: {URL}")


if __name__ == "__main__":
    main()
