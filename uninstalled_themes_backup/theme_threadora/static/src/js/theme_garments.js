/** @odoo-module **/

/* =========================================================================
   THREADORA GARMENTS & APPAREL - FRONTEND INTERACTION CONTROLLERS
   ========================================================================= */

document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initStickyHeader();
    initStatsCounter();
    initFAQAccordion();
    initProductSwatches();
    initCategoryFilter();
});

/* 1. DARK / LIGHT THEME TOGGLE */
function initThemeToggle() {
    const toggleBtn = document.getElementById('garmentThemeToggle');
    if (!toggleBtn) return;

    const savedTheme = localStorage.getItem('threadora-theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);

    toggleBtn.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('threadora-theme', newTheme);
        
        const icon = toggleBtn.querySelector('i');
        if (icon) {
            if (newTheme === 'dark') {
                icon.classList.remove('fa-moon-o');
                icon.classList.add('fa-sun-o');
            } else {
                icon.classList.remove('fa-sun-o');
                icon.classList.add('fa-moon-o');
            }
        }
    });
}

/* 2. STICKY HEADER GLASS EFFECT */
function initStickyHeader() {
    const header = document.querySelector('#top');
    if (!header) return;

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });
}

/* 3. ANIMATED NUMBER COUNTERS (STATS) */
function initStatsCounter() {
    const statsSection = document.querySelector('.s_garment_stats');
    if (!statsSection) return;

    let hasRun = false;
    const observer = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting && !hasRun) {
            hasRun = true;
            document.querySelectorAll('.s_garment_stat_number .counter').forEach(counter => {
                const target = parseInt(counter.getAttribute('data-target') || counter.textContent);
                let count = 0;
                const speed = 2000 / (target || 1);
                const timer = setInterval(() => {
                    count += Math.ceil(target / 40);
                    if (count >= target) {
                        counter.textContent = target;
                        clearInterval(timer);
                    } else {
                        counter.textContent = count;
                    }
                }, 30);
            });
        }
    }, { threshold: 0.2 });

    observer.observe(statsSection);
}

/* 4. FAQ ACCORDION CONTROLLER */
function initFAQAccordion() {
    const faqItems = document.querySelectorAll('.s_garment_faq_item');
    faqItems.forEach(item => {
        const header = item.querySelector('.s_garment_faq_header');
        const body = item.querySelector('.s_garment_faq_body');
        if (!header || !body) return;

        header.addEventListener('click', () => {
            const isOpen = body.style.display === 'block';
            document.querySelectorAll('.s_garment_faq_body').forEach(b => b.style.display = 'none');
            document.querySelectorAll('.s_garment_faq_header .fa').forEach(i => {
                i.classList.remove('fa-minus');
                i.classList.add('fa-plus');
            });

            if (!isOpen) {
                body.style.display = 'block';
                const icon = header.querySelector('.fa');
                if (icon) {
                    icon.classList.remove('fa-plus');
                    icon.classList.add('fa-minus');
                }
            }
        });
    });
}

/* 5. PRODUCT COLOR SWATCH SWITCHER */
function initProductSwatches() {
    document.querySelectorAll('.s_garment_product_card').forEach(card => {
        const swatches = card.querySelectorAll('.s_garment_swatch');
        const img = card.querySelector('.s_garment_prod_img');
        swatches.forEach(swatch => {
            swatch.addEventListener('click', (e) => {
                e.preventDefault();
                swatches.forEach(s => s.classList.remove('active'));
                swatch.classList.add('active');
                const newImg = swatch.getAttribute('data-img');
                if (newImg && img) {
                    img.src = newImg;
                }
            });
        });
    });
}

/* 6. CATEGORY FILTER TABS */
function initCategoryFilter() {
    const filterBtns = document.querySelectorAll('.garment-filter-btn');
    const prodItems = document.querySelectorAll('.garment-prod-item');
    if (!filterBtns.length || !prodItems.length) return;

    filterBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            filterBtns.forEach(b => {
                b.classList.remove('active', 'btn-dark');
                b.classList.add('btn-outline-dark');
            });
            btn.classList.add('active', 'btn-dark');
            btn.classList.remove('btn-outline-dark');

            const filter = btn.getAttribute('data-filter');
            prodItems.forEach(item => {
                const category = item.getAttribute('data-category');
                if (filter === 'all' || category === filter) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });
}
