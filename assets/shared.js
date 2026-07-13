
(function () {
    // Inject stylesheet immediately to minimize FOUC
    if (!document.querySelector('link[href*="shared.css"]')) {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = '/assets/shared.css';
        document.head.appendChild(link);
    }

    // Inject Google Fonts
    if (!document.querySelector('link[href*="fonts.googleapis.com"]')) {
        const fontLink = document.createElement('link');
        fontLink.rel = 'stylesheet';
        fontLink.href = 'https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap';
        document.head.appendChild(fontLink);
    }


    document.addEventListener('DOMContentLoaded', () => {
        const config = window.PAGE_CONFIG || {};

        // Ensure <aside> wrapper exists
        let aside = document.querySelector('aside');
        if (!aside) {
            aside = document.createElement('aside');
            document.body.insertBefore(aside, document.body.firstChild);
        }
        aside.className = 'sidebar-drawer';
        aside.innerHTML = '';

        const scrollContainer = document.createElement('div');
        scrollContainer.className = 'sidebar-scroll-container';


        const backBtn = document.createElement('a');
        backBtn.href = '/index.html';
        backBtn.className = 'back-btn';
        backBtn.innerHTML = `
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <line x1="19" y1="12" x2="5" y2="12"></line>
                <polyline points="12 19 5 12 12 5"></polyline>
            </svg>
            Back to Roadmap
        `;
        scrollContainer.appendChild(backBtn);


        const logoWrapper = document.createElement('div');
        logoWrapper.className = 'sidebar-header';

        let logoHtml = '';
        if (config.logo) {
            logoHtml = `
                <div class="logo-container">
                    <div class="logo-title">
                        ${config.logo.main}<span class="logo-accent">${config.logo.accent}</span>
                    </div>
                    <div class="logo-sub">${config.logo.sub}</div>
                </div>
            `;
        } else {

            const pageTitle = document.querySelector('header h1')?.textContent || 'Play';
            const words = pageTitle.split(' ');
            const mainWord = words[0] || 'Play';
            const accentWord = words.slice(1).join(' ') || 'Math';
            logoHtml = `
                <div class="logo-container">
                    <div class="logo-title">
                        ${mainWord} <span class="logo-accent">${accentWord}</span>
                    </div>
                    <div class="logo-sub">Math explorer</div>
                </div>
            `;
        }
        logoWrapper.innerHTML = logoHtml;
        scrollContainer.appendChild(logoWrapper);


        const navWrapper = document.createElement('nav');
        navWrapper.className = 'sidebar-nav';

        const navMenu = document.createElement('ul');
        navMenu.className = 'syllabus-menu';
        navMenu.id = 'syllabusMenu';

        let navItems = [];
        if (config.navigation) {
            navItems = config.navigation;
        } else {
            // Auto-deduce nav from <section> tags when config.navigation is absent
            const sections = document.querySelectorAll('main section');
            sections.forEach((sec, idx) => {
                const secId = sec.getAttribute('id');
                if (secId) {
                    const secTitle = sec.querySelector('h2')?.textContent || `Section ${idx + 1}`;
                    const secDesc = sec.querySelector('.section-tag')?.textContent || 'Interactive';
                    navItems.push({
                        label: secTitle,
                        desc: secDesc,
                        href: `#${secId}`
                    });
                }
            });
        }

        navItems.forEach((item, idx) => {
            const numStr = String(idx + 1).padStart(2, '0');
            const li = document.createElement('li');
            li.className = 'syllabus-item';

            const hash = window.location.hash;
            const isActive = hash ? item.href === hash : idx === 0;
            if (isActive) {
                li.classList.add('active');
            }

            li.innerHTML = `
                <a href="${item.href}">
                    <span class="syllabus-title">${item.label}</span>
                    <span class="syllabus-desc">${item.desc || ''}</span>
                    <span class="syllabus-number">${numStr}</span>
                </a>
            `;


            li.addEventListener('click', () => {
                document.querySelectorAll('.syllabus-item').forEach(el => el.classList.remove('active'));
                li.classList.add('active');
            });

            navMenu.appendChild(li);
        });
        navWrapper.appendChild(navMenu);
        scrollContainer.appendChild(navWrapper);


        const footer = document.createElement('div');
        footer.className = 'sidebar-footer';

        const path = window.location.pathname;
        let edition = 'Math Edition';
        if (path.includes('decimals')) edition = 'Decimals Edition';
        else if (path.includes('decimal_operations')) edition = 'Decimal Operations Edition';
        else if (path.includes('decimal_place_value')) edition = 'Decimal Place Value Edition';
        else if (path.includes('multi_digit_division')) edition = 'Division Edition';
        else if (path.includes('fractions') || path.includes('fraction_multiplication_division')) edition = 'Fractions Edition';
        else if (path.includes('ratios')) edition = 'Ratios Edition';
        else if (path.includes('pemdas')) edition = 'Arithmetic Edition';
        else if (path.includes('number_systems')) edition = 'Numbers Edition';
        else if (path.includes('03_geometry_measurement')) edition = 'Geometry Edition';
        else if (path.includes('solving_linear_equations') || path.includes('02_algebra')) edition = 'Algebra Edition';
        else if (path.includes('trignometric_identities')) edition = 'Trig Edition';
        else if (path.includes('scatter_plots_and_association') || path.includes('basic_graphs_and_charts') || path.includes('advanced_graphs_and_charts') || path.includes('charts_and_tables')) edition = 'Stats Edition';
        else if (path.includes('mathematical_visualization_with_code')) edition = 'Computational Math Edition';
        else if (path.includes('python_data_science_intro')) edition = 'Python Edition';
        else if (path.includes('05_calculus')) edition = 'Calculus Edition';

        footer.innerHTML = `
            Math Simulation Engine v Beta 1.4.5<br>
            Copyright (c) 2026 by Sebastian Mass.
            <br>Assisted by Antigravity.
            <span class="edition-text">${edition}</span>
        `;
        scrollContainer.appendChild(footer);
        aside.appendChild(scrollContainer);


        let toggleBtn = document.querySelector('.sidebar-toggle-btn');
        if (!toggleBtn) {
            toggleBtn = document.createElement('button');
            toggleBtn.className = 'sidebar-toggle-btn';
            toggleBtn.ariaLabel = 'Toggle Sidebar';
            toggleBtn.innerHTML = `
                <svg class="toggle-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                    <polyline points="15 18 9 12 15 6"></polyline>
                </svg>
            `;
            document.body.appendChild(toggleBtn);
        }

        const isCollapsed = localStorage.getItem('sidebar-collapsed') === 'true';
        if (isCollapsed) {
            document.body.classList.add('sidebar-collapsed');
            aside.classList.add('collapsed');
            toggleBtn.classList.add('collapsed');
        }

        toggleBtn.addEventListener('click', () => {
            const collapsing = !document.body.classList.contains('sidebar-collapsed');
            if (collapsing) {
                document.body.classList.add('sidebar-collapsed');
                aside.classList.add('collapsed');
                toggleBtn.classList.add('collapsed');
            } else {
                document.body.classList.remove('sidebar-collapsed');
                aside.classList.remove('collapsed');
                toggleBtn.classList.remove('collapsed');
            }
            localStorage.setItem('sidebar-collapsed', collapsing);

            setTimeout(() => {
                window.dispatchEvent(new Event('resize'));
            }, 300);
        });

        const domain = config.domain || '01_arithmetic_number_sense';
        document.documentElement.setAttribute('data-domain', domain);

        // Domain accent palette
        const colors = {
            '01_arithmetic_number_sense': { accent: '#38bdf8', glow: 'rgba(56, 189, 248, 0.35)' },
            '02_algebra': { accent: '#f43f5e', glow: 'rgba(244, 63, 94, 0.35)' },
            '03_geometry_measurement': { accent: '#10b981', glow: 'rgba(16, 185, 129, 0.35)' },
            '04_trigonometry': { accent: '#ffb000', glow: 'rgba(255, 176, 0, 0.35)' },
            '05_calculus': { accent: '#6366f1', glow: 'rgba(99, 102, 241, 0.35)' },
            '06_data_science_statistics': { accent: '#a855f7', glow: 'rgba(168, 85, 247, 0.35)' }
        };
        const theme = colors[domain] || colors['01_arithmetic_number_sense'];
        document.documentElement.style.setProperty('--color-accent', theme.accent);
        document.documentElement.style.setProperty('--color-accent-glow', theme.glow);
    });
})();
