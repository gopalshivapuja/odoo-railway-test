/**
 * MOAR Advisory — Inject social icons into header and load Poppins font.
 * Uses JS because theme_ modules store templates as theme.ir.ui.view
 * which requires manual theme application. JS assets load directly.
 */
(function () {
    'use strict';

    // Load Poppins font
    if (!document.querySelector('link[href*="Poppins"]')) {
        const preconnect1 = document.createElement('link');
        preconnect1.rel = 'preconnect';
        preconnect1.href = 'https://fonts.googleapis.com';
        document.head.appendChild(preconnect1);

        const preconnect2 = document.createElement('link');
        preconnect2.rel = 'preconnect';
        preconnect2.href = 'https://fonts.gstatic.com';
        preconnect2.crossOrigin = 'anonymous';
        document.head.appendChild(preconnect2);

        const fontLink = document.createElement('link');
        fontLink.rel = 'stylesheet';
        fontLink.href = 'https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;900&display=swap';
        document.head.appendChild(fontLink);
    }

    // Inject social icons into header
    function injectSocialIcons() {
        const rightUl = document.querySelector('header nav[aria-label="Main"] ul.flex-shrink-0');
        if (!rightUl || rightUl.querySelector('.moar-social-icons')) return;

        const li = document.createElement('li');
        li.className = 'd-flex align-items-center gap-2 ms-2 moar-social-icons';
        li.innerHTML = `
            <a href="https://www.linkedin.com/company/moar-advisory/" target="_blank"
               class="btn rounded-circle p-0 d-flex align-items-center justify-content-center"
               style="background:#1a2954;color:#fff;width:36px;height:36px;min-width:36px;">
                <i class="fa fa-linkedin"></i>
            </a>
            <a href="https://www.youtube.com/@MOARAdvisory" target="_blank"
               class="btn rounded-circle p-0 d-flex align-items-center justify-content-center"
               style="background:#1a2954;color:#fff;width:36px;height:36px;min-width:36px;">
                <i class="fa fa-youtube-play"></i>
            </a>
        `;
        rightUl.appendChild(li);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectSocialIcons);
    } else {
        injectSocialIcons();
    }
})();
