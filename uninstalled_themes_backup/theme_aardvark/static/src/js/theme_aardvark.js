/** @odoo-module **/

// Aardvark Book Club Interactive Features
function initAardvarkTheme() {
    // 1. Monthly Books Carousel Controls & Drag Scroll
    const track = document.getElementById('aardvarkBooksTrack');
    const prevBtn = document.querySelector('.books-slider__btn.is--prev');
    const nextBtn = document.querySelector('.books-slider__btn.is--next');

    if (track) {
        if (prevBtn) {
            prevBtn.addEventListener('click', () => {
                const scrollAmount = track.offsetWidth > 768 ? 382 : 320;
                track.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
            });
        }
        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                const scrollAmount = track.offsetWidth > 768 ? 382 : 320;
                track.scrollBy({ left: scrollAmount, behavior: 'smooth' });
            });
        }

        // Optional Drag-to-scroll for desktop mouse users
        let isDown = false;
        let startX;
        let scrollLeft;

        track.addEventListener('mousedown', (e) => {
            isDown = true;
            track.classList.add('is-dragging');
            startX = e.pageX - track.offsetLeft;
            scrollLeft = track.scrollLeft;
        });

        track.addEventListener('mouseleave', () => {
            isDown = false;
            track.classList.remove('is-dragging');
        });

        track.addEventListener('mouseup', () => {
            isDown = false;
            track.classList.remove('is-dragging');
        });

        track.addEventListener('mousemove', (e) => {
            if (!isDown) return;
            e.preventDefault();
            const x = e.pageX - track.offsetLeft;
            const walk = (x - startX) * 1.5;
            track.scrollLeft = scrollLeft - walk;
        });
    }

    // 2. Book Detail Modal Viewer
    const detailModalEl = document.getElementById('aardvarkBookDetailModal');
    if (detailModalEl && window.bootstrap) {
        const modal = new window.bootstrap.Modal(detailModalEl);
        document.querySelectorAll('.js-open-book-detail').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const card = btn.closest('.books-slider__card');
                if (!card) return;

                const title = card.getAttribute('data-title') || 'Book Title';
                const author = card.getAttribute('data-author') || '';
                const desc = card.getAttribute('data-desc') || '';
                const tag = card.getAttribute('data-tag') || '';
                const img = card.getAttribute('data-img') || '';

                const titleEl = document.getElementById('modalBookTitle');
                const authorEl = document.getElementById('modalBookAuthor');
                const descEl = document.getElementById('modalBookDesc');
                const tagEl = document.getElementById('modalBookTag');
                const imgEl = document.getElementById('modalBookImg');

                if (titleEl) titleEl.textContent = title;
                if (authorEl) authorEl.textContent = author;
                if (descEl) descEl.textContent = desc;
                if (tagEl) {
                    tagEl.textContent = tag;
                    tagEl.style.display = tag ? 'inline-block' : 'none';
                }
                if (imgEl) imgEl.src = img;

                modal.show();
            });
        });
    }

    // 3. Smooth Anchor Scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId && targetId !== '#') {
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    e.preventDefault();
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // 4. Aardvark Box Opening Sequence (120-frame Local High-Res WebP Canvas Animation)
    const boxCanvas = document.getElementById('aardvarkBoxCanvas');
    if (boxCanvas) {
        const ctx = boxCanvas.getContext('2d');
        const totalFrames = 120;
        const frames = new Array(totalFrames);
        let currentFrame = 0;
        let targetFrame = 0;
        let isAnimating = false;
        let framesPreloaded = false;
        let lastRenderedImg = null;

        // Set native high-res canvas dimensions (16:9)
        boxCanvas.width = 1920;
        boxCanvas.height = 1080;

        function drawToCanvas(img) {
            if (!img || !img.complete || img.naturalWidth === 0) return;
            ctx.clearRect(0, 0, boxCanvas.width, boxCanvas.height);
            ctx.drawImage(img, 0, 0, boxCanvas.width, boxCanvas.height);
        }

        // Draw initial closed box immediately from local asset
        const initialImg = new Image();
        initialImg.src = '/theme_aardvark/static/src/img/box/frame-000.webp';
        if (initialImg.complete && initialImg.naturalWidth > 0) {
            drawToCanvas(initialImg);
            lastRenderedImg = initialImg;
        } else {
            initialImg.onload = () => {
                if (!lastRenderedImg) {
                    drawToCanvas(initialImg);
                    lastRenderedImg = initialImg;
                }
            };
        }

        // Preload all 120 frames locally from disk
        function preloadFrames() {
            if (framesPreloaded) return;
            framesPreloaded = true;
            for (let i = 0; i < totalFrames; i++) {
                const img = new Image();
                const pad = String(i).padStart(3, '0');
                img.src = `/theme_aardvark/static/src/img/box/frame-${pad}.webp`;
                img.onload = () => {
                    if (Math.round(currentFrame) === i) {
                        drawToCanvas(img);
                        lastRenderedImg = img;
                    }
                };
                frames[i] = img;
            }
        }

        function renderFrame(index) {
            const idx = Math.max(0, Math.min(totalFrames - 1, Math.round(index)));
            const targetImg = frames[idx];
            if (targetImg && targetImg.complete && targetImg.naturalWidth > 0) {
                drawToCanvas(targetImg);
                lastRenderedImg = targetImg;
            } else if (idx === 0 && initialImg.complete && initialImg.naturalWidth > 0) {
                drawToCanvas(initialImg);
                lastRenderedImg = initialImg;
            }
        }

        function stepAnimation() {
            isAnimating = true;
            if (Math.abs(currentFrame - targetFrame) > 0.4) {
                currentFrame += (targetFrame - currentFrame) * 0.16;
                renderFrame(currentFrame);
                requestAnimationFrame(stepAnimation);
            } else {
                currentFrame = targetFrame;
                renderFrame(currentFrame);
                isAnimating = false;
            }
        }

        function setTarget(newTarget) {
            preloadFrames();
            targetFrame = Math.max(0, Math.min(totalFrames - 1, newTarget));
            if (!isAnimating) stepAnimation();
        }

        // Start preloading frames in background
        setTimeout(preloadFrames, 150);

        // Scroll handler: opens box smoothly as user scrolls past section
        function onScroll() {
            const rect = boxCanvas.getBoundingClientRect();
            const winH = window.innerHeight;
            if (rect.top < winH && rect.bottom > 0) {
                preloadFrames();
                const boxCenter = rect.top + rect.height / 2;
                const start = winH * 0.88;
                const end = winH * 0.28;
                const progress = (start - boxCenter) / (start - end);
                const clamped = Math.max(0, Math.min(1, progress));
                // Map progress to frames 0 to 75 (open box view)
                setTarget(Math.round(clamped * 75));
            }
        }

        window.addEventListener('scroll', onScroll, { passive: true });
        // Initial trigger check after layout settles
        setTimeout(onScroll, 300);
        setTimeout(onScroll, 800);

        // Click to toggle open (frame 70) / closed (frame 0)
        boxCanvas.addEventListener('click', () => {
            const dest = targetFrame > 35 ? 0 : 70;
            setTarget(dest);
        });

        // Hover effect: slight opening peek on mouse enter
        boxCanvas.addEventListener('mouseenter', () => {
            if (targetFrame < 25) {
                setTarget(35);
            }
        });
    }
}

// Auto-run whether DOM is loading or already ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAardvarkTheme);
} else {
    initAardvarkTheme();
}
