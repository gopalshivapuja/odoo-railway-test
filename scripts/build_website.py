#!/usr/bin/env python3
"""Build the complete MOAR Advisory website replica in Odoo via XML-RPC."""

import time

from common import connect_odoo

# ─────────────────────────────────────────────
# Custom CSS matching moaradvisory.com design
# ─────────────────────────────────────────────
CUSTOM_CSS = """
/* ═══════════════════════════════════════════
   MOAR Advisory - Custom Theme CSS
   Colors: Blue #2575fc, Purple #6a11cb, Dark #1a1a2e
   Font: Archivo
   ═══════════════════════════════════════════ */

@import url('https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;900&display=swap');

:root {
    --moar-blue: #2575fc;
    --moar-purple: #6a11cb;
    --moar-dark: #1a1a2e;
    --moar-gray: #32373c;
    --moar-light: #f8f9fa;
    --moar-text: #333333;
    --moar-text-light: #666666;
    --moar-gradient: linear-gradient(-35deg, #2575fc, #6a11cb);
}

/* ── Global Typography ── */
body, .o_website_page {
    font-family: 'Archivo', sans-serif !important;
    color: var(--moar-text);
    font-size: 16px;
    line-height: 1.7;
}

h1, h2, h3, h4, h5, h6,
.h1, .h2, .h3, .h4, .h5, .h6 {
    font-family: 'Archivo', sans-serif !important;
    font-weight: 700;
    color: var(--moar-dark);
}

h1, .h1 { font-size: 42px; }
h2, .h2 { font-size: 36px; margin-bottom: 20px; }
h3, .h3 { font-size: 24px; }
p { font-size: 18px; line-height: 1.8; color: var(--moar-text-light); }

/* ── Header / Navbar ── */
header .navbar {
    background: #ffffff !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    padding: 12px 0;
}
header .navbar-brand img {
    max-height: 45px;
}
header .nav-link {
    font-family: 'Archivo', sans-serif !important;
    font-weight: 500;
    font-size: 15px;
    color: var(--moar-dark) !important;
    padding: 8px 16px !important;
    transition: color 0.3s ease;
}
header .nav-link:hover {
    color: var(--moar-blue) !important;
}

/* ── Buttons ── */
.btn-primary, .btn-moar {
    background: var(--moar-gradient) !important;
    border: none !important;
    color: #fff !important;
    padding: 12px 32px;
    border-radius: 6px;
    font-weight: 600;
    font-size: 16px;
    transition: all 0.3s ease;
    text-transform: none;
    letter-spacing: 0.3px;
}
.btn-primary:hover, .btn-moar:hover {
    opacity: 0.9;
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(37, 117, 252, 0.3);
}
.btn-secondary, .btn-outline-moar {
    background: transparent !important;
    border: 2px solid var(--moar-blue) !important;
    color: var(--moar-blue) !important;
    padding: 10px 30px;
    border-radius: 6px;
    font-weight: 600;
    transition: all 0.3s ease;
}
.btn-secondary:hover, .btn-outline-moar:hover {
    background: var(--moar-blue) !important;
    color: #fff !important;
}

/* ── Hero Sections ── */
.moar-hero {
    background: var(--moar-gradient);
    padding: 100px 0;
    position: relative;
    overflow: hidden;
    text-align: center;
}
.moar-hero h1 {
    color: #ffffff;
    font-size: 48px;
    font-weight: 900;
    margin-bottom: 20px;
}
.moar-hero p {
    color: rgba(255,255,255,0.9);
    font-size: 20px;
    max-width: 700px;
    margin: 0 auto 30px;
}
.moar-hero .btn {
    background: #ffffff !important;
    color: var(--moar-blue) !important;
    font-weight: 700;
    padding: 14px 40px;
    border-radius: 6px;
    font-size: 16px;
}

/* ── Section Styling ── */
.moar-section {
    padding: 80px 0;
}
.moar-section-gray {
    background: var(--moar-light);
}
.moar-section-dark {
    background: var(--moar-dark);
    color: #ffffff;
}
.moar-section-dark h2,
.moar-section-dark h3 {
    color: #ffffff;
}
.moar-section-dark p {
    color: rgba(255,255,255,0.8);
}
.section-title {
    text-align: center;
    margin-bottom: 50px;
}
.section-title h2 {
    font-size: 36px;
    font-weight: 700;
    color: var(--moar-dark);
    margin-bottom: 15px;
}
.section-title p {
    font-size: 18px;
    color: var(--moar-text-light);
    max-width: 600px;
    margin: 0 auto;
}

/* ── Cards ── */
.moar-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 35px 30px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    transition: all 0.3s ease;
    height: 100%;
    border: 1px solid rgba(0,0,0,0.05);
}
.moar-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 35px rgba(0,0,0,0.1);
}
.moar-card h3 {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 15px;
    color: var(--moar-dark);
}
.moar-card p {
    font-size: 15px;
    color: var(--moar-text-light);
    line-height: 1.7;
}
.moar-card .card-icon {
    width: 60px;
    height: 60px;
    background: var(--moar-gradient);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 20px;
    color: #fff;
    font-size: 24px;
}

/* ── Stats ── */
.moar-stat {
    text-align: center;
    padding: 30px;
}
.moar-stat .stat-number {
    font-size: 48px;
    font-weight: 900;
    background: var(--moar-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.2;
}
.moar-stat .stat-label {
    font-size: 16px;
    color: var(--moar-text-light);
    font-weight: 500;
    margin-top: 8px;
}

/* ── Team Cards ── */
.moar-team-card {
    text-align: center;
    padding: 30px 20px;
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.06);
    transition: all 0.3s ease;
}
.moar-team-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 30px rgba(0,0,0,0.1);
}
.moar-team-card .team-photo {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: var(--moar-gradient);
    margin: 0 auto 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-size: 36px;
    font-weight: 700;
}
.moar-team-card h4 {
    font-size: 18px;
    font-weight: 700;
    color: var(--moar-dark);
    margin-bottom: 5px;
}
.moar-team-card .team-role {
    font-size: 14px;
    color: var(--moar-blue);
    font-weight: 600;
    margin-bottom: 10px;
}
.moar-team-card .team-bio {
    font-size: 13px;
    color: var(--moar-text-light);
    line-height: 1.6;
}

/* ── Values ── */
.moar-value {
    text-align: center;
    padding: 40px 25px;
}
.moar-value .value-icon {
    width: 70px;
    height: 70px;
    background: var(--moar-gradient);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 20px;
    color: #fff;
    font-size: 28px;
}
.moar-value h4 {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 10px;
}

/* ── Industries ── */
.moar-industry {
    background: #ffffff;
    border-radius: 12px;
    padding: 30px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.06);
    transition: all 0.3s ease;
}
.moar-industry:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
}
.moar-industry .industry-icon {
    font-size: 40px;
    margin-bottom: 15px;
    color: var(--moar-blue);
}
.moar-industry h4 {
    font-size: 18px;
    font-weight: 700;
    color: var(--moar-dark);
}

/* ── FAQ Accordion ── */
.moar-faq .accordion-button {
    font-family: 'Archivo', sans-serif;
    font-weight: 600;
    font-size: 16px;
    color: var(--moar-dark);
    background: #ffffff;
    border: none;
    padding: 18px 24px;
}
.moar-faq .accordion-button:not(.collapsed) {
    color: var(--moar-blue);
    background: var(--moar-light);
}
.moar-faq .accordion-item {
    border: 1px solid rgba(0,0,0,0.08);
    border-radius: 8px !important;
    margin-bottom: 10px;
    overflow: hidden;
}
.moar-faq .accordion-body {
    font-size: 15px;
    color: var(--moar-text-light);
    line-height: 1.8;
    padding: 20px 24px;
}

/* ── CTA Banner ── */
.moar-cta {
    background: var(--moar-gradient);
    padding: 60px 0;
    text-align: center;
}
.moar-cta h2 {
    color: #ffffff;
    font-size: 36px;
    margin-bottom: 15px;
}
.moar-cta p {
    color: rgba(255,255,255,0.9);
    font-size: 18px;
    margin-bottom: 30px;
}
.moar-cta .btn {
    background: #ffffff !important;
    color: var(--moar-blue) !important;
    font-weight: 700;
    padding: 14px 40px;
}

/* ── Footer ── */
footer, #footer {
    background: var(--moar-dark) !important;
    color: rgba(255,255,255,0.8);
    padding: 60px 0 30px;
}
footer h5, #footer h5 {
    color: #ffffff;
    font-weight: 700;
    font-size: 18px;
    margin-bottom: 20px;
}
footer a, #footer a {
    color: rgba(255,255,255,0.7) !important;
    transition: color 0.3s ease;
}
footer a:hover, #footer a:hover {
    color: var(--moar-blue) !important;
}
footer .copyright {
    border-top: 1px solid rgba(255,255,255,0.1);
    padding-top: 20px;
    margin-top: 40px;
    text-align: center;
    font-size: 14px;
}

/* ── Process Steps ── */
.moar-step {
    text-align: center;
    padding: 30px;
    position: relative;
}
.moar-step .step-number {
    width: 50px;
    height: 50px;
    background: var(--moar-gradient);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 20px;
    color: #fff;
    font-size: 20px;
    font-weight: 700;
}

/* ── Shadow Text (background watermark) ── */
.moar-shadow-text {
    font-size: 90px;
    font-weight: 700;
    color: rgba(0,0,0,0.03);
    position: absolute;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    white-space: nowrap;
    pointer-events: none;
    z-index: 0;
}

/* ── Contact Form ── */
.moar-form input,
.moar-form textarea,
.moar-form select {
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 12px 16px;
    font-size: 16px;
    font-family: 'Archivo', sans-serif;
    width: 100%;
    margin-bottom: 15px;
    transition: border-color 0.3s ease;
}
.moar-form input:focus,
.moar-form textarea:focus,
.moar-form select:focus {
    border-color: var(--moar-blue);
    outline: none;
    box-shadow: 0 0 0 3px rgba(37,117,252,0.1);
}

/* ── Blog Cards ── */
.moar-blog-card {
    background: #ffffff;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0,0,0,0.06);
    transition: all 0.3s ease;
}
.moar-blog-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 30px rgba(0,0,0,0.1);
}
.moar-blog-card .blog-content {
    padding: 25px;
}
.moar-blog-card h4 {
    font-size: 18px;
    font-weight: 700;
    color: var(--moar-dark);
    margin-bottom: 10px;
}
.moar-blog-card .read-more {
    color: var(--moar-blue);
    font-weight: 600;
    text-decoration: none;
    font-size: 14px;
}

/* ── Responsive ── */
@media (max-width: 768px) {
    .moar-hero h1 { font-size: 32px; }
    .moar-hero { padding: 60px 20px; }
    h2 { font-size: 28px; }
    .moar-section { padding: 50px 0; }
    .moar-stat .stat-number { font-size: 36px; }
    .moar-shadow-text { font-size: 40px; }
}

/* ── Animations ── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}
.moar-animate {
    animation: fadeInUp 0.8s ease-out;
}

/* ── Override Odoo defaults ── */
#wrapwrap { background: #ffffff; }
.o_footer { background: var(--moar-dark) !important; }
.o_footer_copyright { background: var(--moar-dark) !important; }
"""


# ─────────────────────────────────────────────
# Page HTML Content
# ─────────────────────────────────────────────

HOMEPAGE_HTML = """
<!-- Hero Section -->
<section class="moar-hero">
    <div class="container">
        <h1 class="moar-animate">Advice You Can Trust.<br/>Experience You Can Use.</h1>
        <p class="moar-animate">Expertise that helps organisations build stronger brands, cultures, and capabilities.</p>
        <a href="/blog" class="btn btn-lg moar-animate">Discover Now</a>
    </div>
</section>

<!-- About MOAR Section -->
<section class="moar-section">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-lg-6">
                <h2>Your Partner in Growth</h2>
                <p>We go beyond traditional consulting by working alongside you to set up, scale and optimize your business. With deep expertise in GCC consulting, people advisory, and digital transformation, MOAR Advisory delivers results that matter.</p>
                <p>Headquartered in Bengaluru with a 200+ delivery team, we blend advisory expertise with hands-on execution to help enterprises establish, operate, and scale global capability centers with measurable outcomes.</p>
                <a href="/about" class="btn btn-primary mt-3">Learn MOAR</a>
            </div>
            <div class="col-lg-6 text-center">
                <div class="moar-stat">
                    <div class="stat-number">200+</div>
                    <div class="stat-label">Experienced Practitioners</div>
                </div>
                <div class="row">
                    <div class="col-6">
                        <div class="moar-stat">
                            <div class="stat-number">10+</div>
                            <div class="stat-label">Industries Served</div>
                        </div>
                    </div>
                    <div class="col-6">
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

<!-- Services Section -->
<section class="moar-section moar-section-gray">
    <div class="container">
        <div class="section-title">
            <h2>What We Do — Our Offerings</h2>
            <p>End-to-end advisory services for your strategic growth</p>
        </div>
        <div class="row g-4">
            <div class="col-lg-4 col-md-6">
                <div class="moar-card">
                    <div class="card-icon">&#x1F3E2;</div>
                    <h3>Company Setup &amp; Finance</h3>
                    <p>Simplified entry and scalable operations. We assist companies in establishing foundational frameworks for compliance, finance, and operations in new markets.</p>
                    <a href="/company-setup-finance" class="btn-outline-moar btn mt-3">Know More</a>
                </div>
            </div>
            <div class="col-lg-4 col-md-6">
                <div class="moar-card">
                    <div class="card-icon">&#x1F465;</div>
                    <h3>People Advisory</h3>
                    <p>Talent and people advisory services for global success. We create strong talent strategies, build leadership and shape company culture for growth.</p>
                    <a href="/people-advisory" class="btn-outline-moar btn mt-3">Know More</a>
                </div>
            </div>
            <div class="col-lg-4 col-md-6">
                <div class="moar-card">
                    <div class="card-icon">&#x1F50D;</div>
                    <h3>M-SELECT — Recruitment</h3>
                    <p>Strategic recruitment that powers your GCC success. AI-driven insights, practitioner expertise, and dedicated account management for the right talent.</p>
                    <a href="/m-select" class="btn-outline-moar btn mt-3">Know More</a>
                </div>
            </div>
            <div class="col-lg-4 col-md-6">
                <div class="moar-card">
                    <div class="card-icon">&#x1F4E3;</div>
                    <h3>M-POWER — Employer Branding</h3>
                    <p>Strategic communications that shape exceptional workplaces. We strengthen employer brands, attract talent, and deliver measurable impact.</p>
                    <a href="/m-power" class="btn-outline-moar btn mt-3">Know More</a>
                </div>
            </div>
            <div class="col-lg-4 col-md-6">
                <div class="moar-card">
                    <div class="card-icon">&#x1F4BB;</div>
                    <h3>Technology &amp; Digital Transformation</h3>
                    <p>Reimagining technology as a catalyst for enterprise growth. Modern IT architecture with strategic transformation to drive agility and resilience.</p>
                    <a href="/technology-digital" class="btn-outline-moar btn mt-3">Know More</a>
                </div>
            </div>
            <div class="col-lg-4 col-md-6">
                <div class="moar-card">
                    <div class="card-icon">&#x1F4C8;</div>
                    <h3>Advisory Services</h3>
                    <p>Helping companies set up, scale, and operate with the right insight and leadership in place. Research, planning, and experienced leadership for growth.</p>
                    <a href="/advisory-services" class="btn-outline-moar btn mt-3">Know More</a>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- GCC Section -->
<section class="moar-section moar-section-dark">
    <div class="container">
        <div class="section-title">
            <h2>Global Enterprise &amp; Capability Hubs</h2>
            <p>Comprehensive GCC solutions tailored to your growth stage</p>
        </div>
        <div class="row g-4">
            <div class="col-lg-4">
                <div class="moar-card" style="background: rgba(255,255,255,0.08); border-color: rgba(255,255,255,0.15);">
                    <h3 style="color:#fff;">BOT — Build, Operate &amp; Transfer</h3>
                    <p style="color:rgba(255,255,255,0.75);">We build and operate your GCC, then transfer full ownership once it's mature and self-sustaining. Ideal for companies wanting a low-risk market entry.</p>
                </div>
            </div>
            <div class="col-lg-4">
                <div class="moar-card" style="background: rgba(255,255,255,0.08); border-color: rgba(255,255,255,0.15);">
                    <h3 style="color:#fff;">GCC as a Service</h3>
                    <p style="color:rgba(255,255,255,0.75);">A fully managed model where we handle everything from infrastructure to talent, letting you focus on outcomes without operational overhead.</p>
                </div>
            </div>
            <div class="col-lg-4">
                <div class="moar-card" style="background: rgba(255,255,255,0.08); border-color: rgba(255,255,255,0.15);">
                    <h3 style="color:#fff;">Assisted GCC</h3>
                    <p style="color:rgba(255,255,255,0.75);">For organizations that want to own the journey but need expert guidance at every step. We provide strategic support while you maintain full control.</p>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Industries Section -->
<section class="moar-section moar-section-gray">
    <div class="container">
        <div class="section-title">
            <h2>Industries We Serve</h2>
        </div>
        <div class="row g-4 justify-content-center">
            <div class="col-lg-2 col-md-4 col-6">
                <div class="moar-industry">
                    <div class="industry-icon">&#x1F6D2;</div>
                    <h4>Retail</h4>
                </div>
            </div>
            <div class="col-lg-2 col-md-4 col-6">
                <div class="moar-industry">
                    <div class="industry-icon">&#x1F3ED;</div>
                    <h4>Manufacturing</h4>
                </div>
            </div>
            <div class="col-lg-2 col-md-4 col-6">
                <div class="moar-industry">
                    <div class="industry-icon">&#x1F4B0;</div>
                    <h4>Financial Services</h4>
                </div>
            </div>
            <div class="col-lg-2 col-md-4 col-6">
                <div class="moar-industry">
                    <div class="industry-icon">&#x1F3E5;</div>
                    <h4>Healthcare</h4>
                </div>
            </div>
            <div class="col-lg-2 col-md-4 col-6">
                <div class="moar-industry">
                    <div class="industry-icon">&#x2708;</div>
                    <h4>Aviation</h4>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Values Section -->
<section class="moar-section">
    <div class="container">
        <div class="section-title">
            <h2>The Way We Operate — Our Values</h2>
        </div>
        <div class="row g-4">
            <div class="col-lg-3 col-md-6">
                <div class="moar-value">
                    <div class="value-icon">&#x2728;</div>
                    <h4>Simplicity</h4>
                    <p>We cut through complexity to deliver clear, actionable guidance.</p>
                </div>
            </div>
            <div class="col-lg-3 col-md-6">
                <div class="moar-value">
                    <div class="value-icon">&#x1F3AF;</div>
                    <h4>Credibility</h4>
                    <p>Our practitioners bring deep industry experience you can trust.</p>
                </div>
            </div>
            <div class="col-lg-3 col-md-6">
                <div class="moar-value">
                    <div class="value-icon">&#x1F91D;</div>
                    <h4>Authenticity</h4>
                    <p>Genuine partnerships built on transparency and honest counsel.</p>
                </div>
            </div>
            <div class="col-lg-3 col-md-6">
                <div class="moar-value">
                    <div class="value-icon">&#x2705;</div>
                    <h4>Accountability</h4>
                    <p>We own outcomes and deliver on our commitments, every time.</p>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Why MOAR Section -->
<section class="moar-section moar-section-gray">
    <div class="container">
        <div class="section-title">
            <h2>Why MOAR Advisory</h2>
        </div>
        <div class="row g-4">
            <div class="col-lg-3 col-md-6">
                <div class="moar-card text-center">
                    <h3>People, Trust &amp; Transparency</h3>
                    <p>Our relationships are built on a foundation of openness and mutual respect.</p>
                </div>
            </div>
            <div class="col-lg-3 col-md-6">
                <div class="moar-card text-center">
                    <h3>Practitioners, Not Consultants</h3>
                    <p>We work as an extension of your team, bringing hands-on execution capability.</p>
                </div>
            </div>
            <div class="col-lg-3 col-md-6">
                <div class="moar-card text-center">
                    <h3>Tailored Solutions</h3>
                    <p>No templates. Every engagement is designed around your unique needs and context.</p>
                </div>
            </div>
            <div class="col-lg-3 col-md-6">
                <div class="moar-card text-center">
                    <h3>Speed to Market</h3>
                    <p>We accelerate your go-to-market timeline with proven frameworks and execution speed.</p>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- How We Work Section -->
<section class="moar-section">
    <div class="container">
        <div class="section-title">
            <h2>Our Strategy — How We Work</h2>
        </div>
        <div class="row g-4">
            <div class="col-lg-4">
                <div class="moar-step">
                    <div class="step-number">1</div>
                    <h3>Build the Roadmap</h3>
                    <p>We assess your needs, understand your goals, and create a strategic plan tailored to your growth objectives.</p>
                </div>
            </div>
            <div class="col-lg-4">
                <div class="moar-step">
                    <div class="step-number">2</div>
                    <h3>Partner in Execution</h3>
                    <p>Our team embeds with yours, bringing expertise and capability to drive implementation at speed.</p>
                </div>
            </div>
            <div class="col-lg-4">
                <div class="moar-step">
                    <div class="step-number">3</div>
                    <h3>Deliver &amp; Sustain</h3>
                    <p>We ensure sustainable outcomes with ongoing support, knowledge transfer, and capability building.</p>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Leadership Section -->
<section class="moar-section moar-section-gray">
    <div class="container">
        <div class="section-title">
            <h2>Leadership Team</h2>
        </div>
        <div class="row g-4">
            <div class="col-lg-3 col-md-6">
                <div class="moar-team-card">
                    <div class="team-photo">MM</div>
                    <h4>Mohith Mohan</h4>
                    <div class="team-role">Founder &amp; CEO</div>
                    <p class="team-bio">20+ years at Fidelity, Yahoo, Lowe's, HBC. Builds GCCs and employer brands.</p>
                </div>
            </div>
            <div class="col-lg-3 col-md-6">
                <div class="moar-team-card">
                    <div class="team-photo">MK</div>
                    <h4>Mukesh Kedia</h4>
                    <div class="team-role">Co-Founder &amp; CFO</div>
                    <p class="team-bio">19+ years at KPMG, HBC, Giant Eagle. Expertise in fundraising, M&amp;A, compliance.</p>
                </div>
            </div>
            <div class="col-lg-3 col-md-6">
                <div class="moar-team-card">
                    <div class="team-photo">GS</div>
                    <h4>Gopal Shivapuja</h4>
                    <div class="team-role">Partner — Product &amp; Emerging Technology</div>
                    <p class="team-bio">Enterprise platforms, global delivery, large-scale tech transformation.</p>
                </div>
            </div>
            <div class="col-lg-3 col-md-6">
                <div class="moar-team-card">
                    <div class="team-photo">SG</div>
                    <h4>Santosh Gnanaprakash</h4>
                    <div class="team-role">General Counsel, Legal</div>
                    <p class="team-bio">23+ years in litigation, consulting. ICSI member. GCC and ITeS expertise.</p>
                </div>
            </div>
            <div class="col-lg-3 col-md-6">
                <div class="moar-team-card">
                    <div class="team-photo">AD</div>
                    <h4>Anneka Darashah</h4>
                    <div class="team-role">Head — People Advisory</div>
                    <p class="team-bio">20+ years in global HR. Talent function scaling and team leadership.</p>
                </div>
            </div>
            <div class="col-lg-3 col-md-6">
                <div class="moar-team-card">
                    <div class="team-photo">SS</div>
                    <h4>Sonia Sharma</h4>
                    <div class="team-role">Head — Marketing</div>
                    <p class="team-bio">15+ years at ING, Marriott, Quess. Brand storytelling and digital strategy.</p>
                </div>
            </div>
            <div class="col-lg-3 col-md-6">
                <div class="moar-team-card">
                    <div class="team-photo">RV</div>
                    <h4>Rahul Virk</h4>
                    <div class="team-role">Head, Talent Strategy — M Select</div>
                    <p class="team-bio">20+ years in talent acquisition. GCC, technology, banking expertise.</p>
                </div>
            </div>
            <div class="col-lg-3 col-md-6">
                <div class="moar-team-card">
                    <div class="team-photo">MV</div>
                    <h4>Minoo Verma</h4>
                    <div class="team-role">Head — Communications</div>
                    <p class="team-bio">15+ years in employer branding, stakeholder engagement, digital strategy.</p>
                </div>
            </div>
        </div>
        <div class="row mt-4">
            <div class="col-lg-3 col-md-6 mx-auto">
                <div class="moar-team-card">
                    <div class="team-photo">HN</div>
                    <h4>Harsha Nandakumar</h4>
                    <div class="team-role">Director Programs &amp; Customer Success</div>
                    <p class="team-bio">15+ years in digital commerce, marketplace ops. Hudson's Bay, Swiggy, Bigbasket.</p>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- CTA Section -->
<section class="moar-cta">
    <div class="container">
        <h2>Ready to Scale Your Business?</h2>
        <p>Talk to our experts and explore faster ways to grow.</p>
        <a href="/contactus" class="btn btn-lg">Get in Touch</a>
    </div>
</section>
"""

ABOUT_HTML = """
<!-- Hero -->
<section class="moar-hero">
    <div class="container">
        <h1>About MOAR Advisory</h1>
        <p>Advice You Can Trust, Experience You Can Use.</p>
    </div>
</section>

<!-- About Content -->
<section class="moar-section">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-lg-7">
                <h2>Who We Are</h2>
                <p>MOAR Advisory is built by senior practitioners who have led transformation across industries, startups, and Fortune 500 companies. Headquartered in Bengaluru with a 200+ delivery team through Yitro Global, we blend advisory expertise with hands-on execution.</p>
                <p>Our focus is helping enterprises establish, operate, and scale global capability centers (GCCs) into strategic hubs that drive innovation — not just efficiency. We combine deep industry knowledge with practical, market-grounded counsel to deliver measurable outcomes.</p>
            </div>
            <div class="col-lg-5">
                <div class="row">
                    <div class="col-6">
                        <div class="moar-stat">
                            <div class="stat-number">10+</div>
                            <div class="stat-label">Industries Served Globally</div>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="moar-stat">
                            <div class="stat-number">200+</div>
                            <div class="stat-label">Experienced Practitioners</div>
                        </div>
                    </div>
                    <div class="col-12">
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

<!-- Global Footprint -->
<section class="moar-section moar-section-gray">
    <div class="container">
        <div class="section-title">
            <h2>Our Global Footprint</h2>
        </div>
        <div class="row g-4 justify-content-center">
            <div class="col-lg-3 col-md-6">
                <div class="moar-card text-center">
                    <h3>&#x1F1FA;&#x1F1F8; Texas</h3>
                    <p>North America operations</p>
                </div>
            </div>
            <div class="col-lg-3 col-md-6">
                <div class="moar-card text-center">
                    <h3>&#x1F1EE;&#x1F1F3; Bangalore</h3>
                    <p>Global headquarters</p>
                </div>
            </div>
            <div class="col-lg-3 col-md-6">
                <div class="moar-card text-center">
                    <h3>&#x1F1EE;&#x1F1F3; Chennai</h3>
                    <p>South India operations</p>
                </div>
            </div>
            <div class="col-lg-3 col-md-6">
                <div class="moar-card text-center">
                    <h3>&#x1F1F5;&#x1F1ED; Manila</h3>
                    <p>Southeast Asia operations</p>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- CTA -->
<section class="moar-cta">
    <div class="container">
        <h2>Partner With Us</h2>
        <p>Let's build something exceptional together.</p>
        <a href="/contactus" class="btn btn-lg">Get in Touch</a>
    </div>
</section>
"""

LEADERS_HTML = """
<!-- Hero -->
<section class="moar-hero">
    <div class="container">
        <h1>Our Leaders</h1>
        <p>Senior practitioners driving transformation across industries</p>
    </div>
</section>

<!-- Leadership Team -->
<section class="moar-section">
    <div class="container">
        <div class="section-title">
            <h2>Leadership Team</h2>
        </div>
        <div class="row g-4">
            <div class="col-lg-4 col-md-6">
                <div class="moar-team-card">
                    <div class="team-photo">MM</div>
                    <h4>Mohith Mohan</h4>
                    <div class="team-role">Founder &amp; CEO</div>
                    <p class="team-bio">With 20+ years of experience at Fidelity, Yahoo, Lowe's, and HBC, Mohith specializes in building GCCs and employer brands that drive organizational growth.</p>
                </div>
            </div>
            <div class="col-lg-4 col-md-6">
                <div class="moar-team-card">
                    <div class="team-photo">MK</div>
                    <h4>Mukesh Kedia</h4>
                    <div class="team-role">Co-Founder &amp; CFO</div>
                    <p class="team-bio">19+ years of experience at KPMG, HBC, and Giant Eagle with deep expertise in fundraising, M&amp;A, compliance, and financial strategy.</p>
                </div>
            </div>
            <div class="col-lg-4 col-md-6">
                <div class="moar-team-card">
                    <div class="team-photo">GS</div>
                    <h4>Gopal Shivapuja</h4>
                    <div class="team-role">Partner — Product &amp; Emerging Technology</div>
                    <p class="team-bio">Expert in enterprise platforms, global delivery models, and large-scale technology transformation programs.</p>
                </div>
            </div>
            <div class="col-lg-4 col-md-6">
                <div class="moar-team-card">
                    <div class="team-photo">SG</div>
                    <h4>Santosh Gnanaprakash</h4>
                    <div class="team-role">General Counsel, Legal</div>
                    <p class="team-bio">23+ years in litigation and consulting. ICSI member with deep expertise in GCC legal frameworks and ITeS regulations.</p>
                </div>
            </div>
            <div class="col-lg-4 col-md-6">
                <div class="moar-team-card">
                    <div class="team-photo">AD</div>
                    <h4>Anneka Darashah</h4>
                    <div class="team-role">Head — People Advisory</div>
                    <p class="team-bio">20+ years in global HR with expertise in talent function scaling, team leadership, and organizational development.</p>
                </div>
            </div>
            <div class="col-lg-4 col-md-6">
                <div class="moar-team-card">
                    <div class="team-photo">SS</div>
                    <h4>Sonia Sharma</h4>
                    <div class="team-role">Head — Marketing</div>
                    <p class="team-bio">15+ years at ING, Marriott, and Quess with expertise in brand storytelling, digital strategy, and employer brand marketing.</p>
                </div>
            </div>
            <div class="col-lg-4 col-md-6">
                <div class="moar-team-card">
                    <div class="team-photo">RV</div>
                    <h4>Rahul Virk</h4>
                    <div class="team-role">Head, Talent Strategy — M Select</div>
                    <p class="team-bio">20+ years in talent acquisition across GCC, technology, and banking sectors. Strategic recruitment leadership.</p>
                </div>
            </div>
            <div class="col-lg-4 col-md-6">
                <div class="moar-team-card">
                    <div class="team-photo">MV</div>
                    <h4>Minoo Verma</h4>
                    <div class="team-role">Head — Communications</div>
                    <p class="team-bio">15+ years of experience in employer branding, stakeholder engagement, and digital communications strategy.</p>
                </div>
            </div>
            <div class="col-lg-4 col-md-6">
                <div class="moar-team-card">
                    <div class="team-photo">HN</div>
                    <h4>Harsha Nandakumar</h4>
                    <div class="team-role">Director Programs &amp; Customer Success</div>
                    <p class="team-bio">15+ years in digital commerce and marketplace operations at Hudson's Bay, Swiggy, and Bigbasket.</p>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- CTA -->
<section class="moar-cta">
    <div class="container">
        <h2>Join Our Team</h2>
        <p>We're always looking for exceptional talent to join MOAR Advisory.</p>
        <a href="/contactus" class="btn btn-lg">Get in Touch</a>
    </div>
</section>
"""


def make_service_page(title, tagline, intro, services, target_segments=None):
    """Generate HTML for a service page."""
    services_html = ""
    for i, (name, desc) in enumerate(services):
        services_html += f"""
            <div class="col-lg-6 col-md-6">
                <div class="moar-card">
                    <h3>{name}</h3>
                    <p>{desc}</p>
                </div>
            </div>"""

    segments_html = ""
    if target_segments:
        segments_html = """
<section class="moar-section moar-section-gray">
    <div class="container">
        <div class="section-title">
            <h2>Who We Support</h2>
        </div>
        <div class="row g-4">"""
        for name, desc in target_segments:
            segments_html += f"""
            <div class="col-lg-3 col-md-6">
                <div class="moar-card text-center">
                    <h3>{name}</h3>
                    <p>{desc}</p>
                </div>
            </div>"""
        segments_html += """
        </div>
    </div>
</section>"""

    return f"""
<!-- Hero -->
<section class="moar-hero">
    <div class="container">
        <h1>{title}</h1>
        <p>{tagline}</p>
    </div>
</section>

<!-- Intro -->
<section class="moar-section">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-10">
                <p style="font-size:20px; text-align:center;">{intro}</p>
            </div>
        </div>
    </div>
</section>

<!-- Services -->
<section class="moar-section moar-section-gray">
    <div class="container">
        <div class="section-title">
            <h2>Our Services</h2>
        </div>
        <div class="row g-4">
            {services_html}
        </div>
    </div>
</section>

{segments_html}

<!-- CTA -->
<section class="moar-cta">
    <div class="container">
        <h2>Get a Call Back</h2>
        <p>Talk to our experts and explore faster ways to scale your business.</p>
        <a href="/contactus" class="btn btn-lg">Contact Us</a>
    </div>
</section>
"""


COMPANY_SETUP_HTML = make_service_page(
    "Company Setup &amp; Finance",
    "Simplified Entry. Scalable Operations.",
    "Organizations entering new markets require swift compliance and structured operations. We assist companies in establishing foundational frameworks, enabling immediate growth focus. Our expertise in global business services and GCC consulting supports sustainable operations.",
    [
        ("Legal Entity Setup", "Steering clients through entity structuring, registration, and incorporation adapted to operational models and jurisdictional requirements."),
        ("Compliance &amp; Regulations", "Supporting fulfillment of local legal and regulatory obligations, including licensing, filings, and governance structures."),
        ("Finance &amp; Accounting Setup", "Constructing and deploying finance functions, accounting systems, reporting frameworks, and internal control mechanisms."),
        ("Tax Advisory &amp; Strategy", "Strategic tax structuring and continuous advisory addressing compliance, operational efficiency, and risk mitigation."),
        ("Banking &amp; Treasury", "Facilitating corporate bank account establishment, treasury operations, and initial capital configuration."),
        ("Procurement as a Service", "Establishing or expanding procurement processes, from vendor onboarding through sourcing and spend management."),
        ("Technology &amp; Tools Enablement", "Guidance on deploying core platforms supporting finance, procurement, and compliance operations."),
        ("Ongoing Operational Support", "Post-setup advisory and execution assistance across finance, tax, and compliance to maintain stability and enable expansion."),
    ],
    [
        ("GCCs &amp; Shared Services", "Organizations entering new geographies and establishing capability centers."),
        ("Startups", "Requiring expert guidance for initial operations establishment."),
        ("SMEs", "Seeking comprehensive advisory and global services for growth and scaling."),
        ("Corporate Teams", "Launching new entities, business units, or functions."),
    ]
)

PEOPLE_ADVISORY_HTML = make_service_page(
    "People Advisory",
    "Talent and People Advisory Services for Global Success",
    "The success of any organization starts with its people. We work with businesses to create strong talent strategies, build leadership and shape company culture for growth. From growing teams and setting up global business services hubs, to developing future leaders.",
    [
        ("Workforce Strategy &amp; Talent Planning", "Workforce planning aligned to business growth goals. Talent strategy for scaling teams across markets. Leadership planning for future readiness."),
        ("Talent Acquisition &amp; Employer Branding", "EVP development for talent attraction. Talent engagement and recruitment marketing. Onboarding programs that drive retention and productivity."),
        ("Organization Culture &amp; Change Advisory", "Culture design aligned to business strategy and values. Change management for transformations. DEI strategy integration for inclusive workplaces."),
        ("HR Transformation &amp; Capability Building", "HR operating model design for scaling organizations. Digital enablement of HR processes and systems. Capability building for HR teams."),
        ("Executive Coaching", "Personalized one-on-one coaching for founders, CXOs, and senior leaders. Building clarity, resilience, communication, and influence."),
    ]
)

MSELECT_HTML = make_service_page(
    "M-SELECT — Recruitment",
    "Strategic Recruitment That Powers Your GCC Success",
    "M-SELECT redefines recruitment for Global Capability Centers. By combining AI-driven insights, practitioner expertise, and dedicated account management, we deliver the right talent — aligned with your skills, culture, and vision — every time.",
    [
        ("High-Impact Team Building", "Accelerate high-impact teams in tech, analytics, and operations with targeted talent mapping and acquisition strategies."),
        ("Personalized Candidate Journey", "Deliver a personalized candidate journey powered by subject matter experts who understand your industry and culture."),
        ("Employer Brand Integration", "Elevate your employer brand to attract and retain top talent through authentic storytelling and strategic positioning."),
        ("End-to-End Hiring", "Intelligent, fully aligned with your business goals — from talent mapping to onboarding. Build smarter teams and drive growth."),
    ]
)

MPOWER_HTML = make_service_page(
    "M-POWER — Employer Branding &amp; Communications",
    "Strategic Communications That Shape Exceptional Workplaces",
    "We partner with organizations to strengthen employer brands, attract and retain talent, and deliver measurable impact through strategic communications powered by our global business services expertise.",
    [
        ("Employer Branding &amp; EVP", "Building your reputation as an employer of choice. EVP creation and activation, recruitment marketing, DEI integration, and employee advocacy programs."),
        ("Brand &amp; Reputation Strategy", "Define and elevate your corporate identity. Brand audits, positioning frameworks, visual identity guidelines, and content strategy."),
        ("Go-to-Market Communications", "Product launches and market entries. Messaging strategy, stakeholder communication, sales enablement, and PR outreach."),
        ("Digital Employer Brand Campaigns", "SEO, content marketing, social media strategy, thought leadership, event marketing, and media relations."),
        ("Internal Communications", "Workforce alignment and inspiration. Leadership messaging, culture-building campaigns, DEI communications, and change communication."),
    ]
)

TECH_DIGITAL_HTML = make_service_page(
    "Technology &amp; Digital Transformation",
    "Reimagining Technology as a Catalyst for Enterprise Growth",
    "We help organizations from Global Capability Centers to SMEs build strong digital and infrastructure foundations. Combining modern IT architecture with strategic transformation to drive agility, resilience, and long-term value.",
    [
        ("Enterprise IT Infrastructure", "Design, implement, and manage IT environments supporting global collaboration, business continuity and operational efficiency across cloud, hybrid, and on-premise systems."),
        ("Cloud Strategy &amp; Migration", "Public, private, and hybrid cloud strategy. Network and connectivity optimization. Infrastructure governance and compliance."),
        ("Digital Transformation Strategy", "Move from siloed, project-based approaches to product-centric operating models. Scaled Agile and DevOps adoption."),
        ("Cyber-Resilience &amp; Continuity", "Operational continuity planning, technology portfolio rationalization, and value stream mapping for delivery alignment."),
    ]
)

ADVISORY_HTML = make_service_page(
    "Advisory Services",
    "Helping companies set up, scale, and operate with the right insight and leadership",
    "We support organizations at various growth stages — from early-stage startups entering new markets to established businesses building regional hubs. We function as an extended team, providing research, planning, and experienced leadership to accelerate growth.",
    [
        ("Feasibility Study", "Market validation before expansion — cost analysis, talent availability assessment, legal and regulatory risk identification, and scalability evaluation."),
        ("Location Services", "Geographic expansion guidance including city/country comparative analysis, local compliance, talent access, and ecosystem partnerships."),
        ("Leadership as a Service", "Interim executive support for market entry — office management, team building, operations setup, and leadership continuity during transitions."),
        ("Multi-Industry Expertise", "Practical, market-grounded counsel across industries. Execution support with leadership experience, not just recommendations."),
    ]
)

CASE_STUDIES_HTML = """
<!-- Hero -->
<section class="moar-hero">
    <div class="container">
        <h1>Case Studies</h1>
        <p>Driving Growth Through Strategic Advisory</p>
    </div>
</section>

<!-- Case Studies -->
<section class="moar-section">
    <div class="container">
        <div class="row g-4">
            <div class="col-lg-6">
                <div class="moar-card">
                    <span style="display:inline-block; background:var(--moar-gradient); color:#fff; padding:4px 14px; border-radius:20px; font-size:13px; font-weight:600; margin-bottom:15px;">Packaging</span>
                    <h3>Global Leader in Packaging</h3>
                    <p>A global leader in packaging and industrial products sought to establish a Global Capability Centre to drive digital transformation and technology innovation. MOAR Advisory partnered to design and execute the GCC setup strategy.</p>
                </div>
            </div>
            <div class="col-lg-6">
                <div class="moar-card">
                    <span style="display:inline-block; background:var(--moar-gradient); color:#fff; padding:4px 14px; border-radius:20px; font-size:13px; font-weight:600; margin-bottom:15px;">Retail</span>
                    <h3>Retail Transformation</h3>
                    <p>Improved inventory management and operational efficiency for a leading retail organization through strategic GCC establishment and technology-driven process optimization.</p>
                </div>
            </div>
            <div class="col-lg-6">
                <div class="moar-card">
                    <span style="display:inline-block; background:var(--moar-gradient); color:#fff; padding:4px 14px; border-radius:20px; font-size:13px; font-weight:600; margin-bottom:15px;">Manufacturing</span>
                    <h3>Manufacturing Excellence</h3>
                    <p>Comprehensive HR and operational systems transformation for a manufacturing enterprise, enabling scalable workforce management and streamlined operations across geographies.</p>
                </div>
            </div>
            <div class="col-lg-6">
                <div class="moar-card">
                    <span style="display:inline-block; background:var(--moar-gradient); color:#fff; padding:4px 14px; border-radius:20px; font-size:13px; font-weight:600; margin-bottom:15px;">Financial Services</span>
                    <h3>Digital Strategy for Financial Services</h3>
                    <p>Developed and executed a comprehensive digital strategy for a financial services firm, driving technology modernization and customer experience transformation.</p>
                </div>
            </div>
            <div class="col-lg-6">
                <div class="moar-card">
                    <span style="display:inline-block; background:var(--moar-gradient); color:#fff; padding:4px 14px; border-radius:20px; font-size:13px; font-weight:600; margin-bottom:15px;">Healthcare</span>
                    <h3>Healthcare Staff Retention</h3>
                    <p>Designed and implemented people advisory programs that significantly improved staff retention and organizational culture within a major healthcare provider.</p>
                </div>
            </div>
            <div class="col-lg-6">
                <div class="moar-card">
                    <span style="display:inline-block; background:var(--moar-gradient); color:#fff; padding:4px 14px; border-radius:20px; font-size:13px; font-weight:600; margin-bottom:15px;">Aviation</span>
                    <h3>Aviation Operations Optimization</h3>
                    <p>Streamlined flight operations and technology infrastructure for an aviation company, improving efficiency and establishing scalable operational frameworks.</p>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- CTA -->
<section class="moar-cta">
    <div class="container">
        <h2>Let's Write Your Success Story</h2>
        <p>Partner with MOAR Advisory to drive measurable outcomes for your business.</p>
        <a href="/contactus" class="btn btn-lg">Get in Touch</a>
    </div>
</section>
"""

MEDIA_HTML = """
<!-- Hero -->
<section class="moar-hero">
    <div class="container">
        <h1>Media</h1>
        <p>Conversations That Shape Decisions</p>
    </div>
</section>

<!-- Podcasts & Media -->
<section class="moar-section">
    <div class="container">
        <div class="section-title">
            <h2>Podcasts &amp; Insights</h2>
            <p>Stay updated with MOAR Advisory's thought leadership and industry perspectives</p>
        </div>
        <div class="row g-4">
            <div class="col-lg-4">
                <div class="moar-card">
                    <h3>&#x1F3A7; Conversations that Shape Decisions</h3>
                    <p>Our flagship podcast series exploring GCC strategy, leadership, and the future of global capability centers. Featuring industry leaders and practitioners.</p>
                    <a href="/blog" class="btn btn-primary mt-3">Listen Now</a>
                </div>
            </div>
            <div class="col-lg-4">
                <div class="moar-card">
                    <h3>&#x1F4F0; Industry Insights</h3>
                    <p>Deep dives into trends shaping business advisory, people strategy, and digital transformation across industries we serve.</p>
                    <a href="/blog" class="btn btn-primary mt-3">Read More</a>
                </div>
            </div>
            <div class="col-lg-4">
                <div class="moar-card">
                    <h3>&#x1F3AC; Video Content</h3>
                    <p>Expert discussions, webinar recordings, and thought leadership videos from MOAR Advisory's leadership team.</p>
                    <a href="https://www.youtube.com/@MOARAdvisory" class="btn btn-primary mt-3" target="_blank">Watch on YouTube</a>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Events -->
<section class="moar-section moar-section-gray">
    <div class="container">
        <div class="section-title">
            <h2>Upcoming Events</h2>
        </div>
        <div class="row justify-content-center">
            <div class="col-lg-8">
                <div class="moar-card">
                    <h3>GCC Strategy Webinar 2026</h3>
                    <p><strong>April 15, 2026 | 10:00 AM - 11:30 AM IST</strong></p>
                    <p>Join MOAR Advisory's leadership for an insightful session on the evolving GCC landscape, choosing the right GCC model, and talent strategies for India.</p>
                    <a href="/event" class="btn btn-primary mt-3">Register Now</a>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- CTA -->
<section class="moar-cta">
    <div class="container">
        <h2>Stay Connected</h2>
        <p>Follow us for the latest insights and updates.</p>
        <a href="/contactus" class="btn btn-lg">Subscribe</a>
    </div>
</section>
"""

# ─────────────────────────────────────────────
# Pages configuration
# ─────────────────────────────────────────────
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
    url, db, uid, password, models = connect_odoo()

    # ── Step 1: Inject Custom CSS ──
    print("\n=== INJECTING CUSTOM CSS ===")

    # Create a custom CSS asset via ir.asset
    css_view_name = "moar_advisory_custom_css"

    # Check if view already exists
    existing_views = models.execute_kw(
        db, uid, password, "ir.ui.view", "search",
        [[["name", "=", css_view_name]]]
    )


    if existing_views:
        models.execute_kw(
            db, uid, password, "ir.ui.view", "write",
            [existing_views, {
                "arch_db": """<data>
    <xpath expr="//head" position="before">
        <t t-call-assets="web.assets_frontend" t-js="false"/>
    </xpath>
</data>"""
            }]
        )
        print(f"  Updated existing CSS view (ID: {existing_views[0]})")

    # Use website.page custom_css or inject via a simpler method
    # Let's create a dedicated view that injects into the frontend
    inject_view_name = "moar_custom_styles"
    models.execute_kw(
        db, uid, password, "ir.ui.view", "search",
        [[["name", "=", inject_view_name], ["type", "=", "qweb"]]]
    )


    # Alternative approach: use website.assets_frontend to inject CSS
    # Find the website layout view and add CSS
    layout_views = models.execute_kw(
        db, uid, password, "ir.ui.view", "search_read",
        [[["key", "=", "website.layout"]]],
        {"fields": ["id", "name", "key"], "limit": 1}
    )

    if layout_views:
        # Create an inherited view to inject our CSS
        css_inherit_name = "moar_advisory.custom_css_inject"
        existing_css_inherit = models.execute_kw(
            db, uid, password, "ir.ui.view", "search",
            [[["key", "=", css_inherit_name]]]
        )


        # Simpler approach using customize_show
        inherit_arch = f"""<data inherit_id="{layout_views[0]['id']}">
    <xpath expr="//head" position="inside">
        <style>
{CUSTOM_CSS}
        </style>
    </xpath>
</data>"""

        if existing_css_inherit:
            models.execute_kw(
                db, uid, password, "ir.ui.view", "write",
                [existing_css_inherit, {"arch_db": inherit_arch}]
            )
            print(f"  Updated CSS injection view (ID: {existing_css_inherit[0]})")
        else:
            css_view_id = models.execute_kw(
                db, uid, password, "ir.ui.view", "create",
                [{
                    "name": "MOAR Advisory Custom CSS",
                    "type": "qweb",
                    "key": css_inherit_name,
                    "inherit_id": layout_views[0]["id"],
                    "arch_db": inherit_arch,
                    "website_id": 1,
                    "active": True,
                }]
            )
            print(f"  Created CSS injection view (ID: {css_view_id})")
    else:
        print("  WARNING: Could not find website.layout view for CSS injection")

    # ── Step 2: Update Homepage ──
    print("\n=== UPDATING HOMEPAGE ===")

    # Find the homepage view
    homepage_pages = models.execute_kw(
        db, uid, password, "website.page", "search_read",
        [[["url", "=", "/"], ["website_id", "=", 1]]],
        {"fields": ["id", "name", "view_id"]}
    )

    if homepage_pages:
        view_id = homepage_pages[0]["view_id"][0]
        # Read current arch to understand structure
        models.execute_kw(
            db, uid, password, "ir.ui.view", "read",
            [[view_id], ["arch_db", "name"]]
        )

        # Update the homepage content
        new_arch = f"""<t name="Homepage" t-name="website.homepage">
    <t t-call="website.layout">
        <t t-set="pageName" t-value="'homepage'"/>
        <div id="wrap" class="oe_structure oe_empty">
            {HOMEPAGE_HTML}
        </div>
    </t>
</t>"""

        models.execute_kw(
            db, uid, password, "ir.ui.view", "write",
            [[view_id], {"arch_db": new_arch}]
        )
        print(f"  Updated homepage view (ID: {view_id})")
    else:
        print("  Homepage not found - will create as page")

    # ── Step 3: Create All Pages ──
    print("\n=== CREATING PAGES ===")

    for page_config in PAGES:
        page_name = page_config["name"]
        page_url = page_config["url"]
        page_html = page_config["html"]

        # Check if page already exists
        existing = models.execute_kw(
            db, uid, password, "website.page", "search_read",
            [[["url", "=", page_url], ["website_id", "=", 1]]],
            {"fields": ["id", "name", "view_id"]}
        )

        view_arch = f"""<t name="{page_name}" t-name="website.page_{page_url.strip('/').replace('-', '_').replace('/', '_')}">
    <t t-call="website.layout">
        <div id="wrap" class="oe_structure oe_empty">
            {page_html}
        </div>
    </t>
</t>"""

        if existing:
            # Update existing page
            view_id = existing[0]["view_id"][0]
            models.execute_kw(
                db, uid, password, "ir.ui.view", "write",
                [[view_id], {"arch_db": view_arch}]
            )
            print(f"  Updated: {page_name} ({page_url}) - view ID {view_id}")
        else:
            # Create new page
            try:
                # First create the view
                view_key = f"website.page_{page_url.strip('/').replace('-', '_').replace('/', '_')}"
                view_id = models.execute_kw(
                    db, uid, password, "ir.ui.view", "create",
                    [{
                        "name": page_name,
                        "type": "qweb",
                        "key": view_key,
                        "arch_db": view_arch,
                        "website_id": 1,
                    }]
                )

                # Then create the page linking to the view
                page_id = models.execute_kw(
                    db, uid, password, "website.page", "create",
                    [{
                        "name": page_name,
                        "url": page_url,
                        "view_id": view_id,
                        "website_id": 1,
                        "is_published": True,
                        "website_published": True,
                    }]
                )
                print(f"  Created: {page_name} ({page_url}) - page ID {page_id}, view ID {view_id}")
            except Exception as e:
                print(f"  ERROR creating {page_name}: {e}")

        time.sleep(1)

    print("\n=== BUILD COMPLETE ===")
    print(f"Site: {url}")
    print("All pages created with MOAR Advisory branding and content.")
    print("\nPages available:")
    print("  / (Homepage)")
    for p in PAGES:
        print(f"  {p['url']} ({p['name']})")
    print("  /blog (MOAR Lens)")
    print("  /contactus (Contact Us)")
    print("  /jobs (Careers)")
    print("  /event (Events)")
    print("  /shop (eCommerce)")
    print("  /forum (Forum)")
    print("  /slides (Courses)")


if __name__ == "__main__":
    main()
