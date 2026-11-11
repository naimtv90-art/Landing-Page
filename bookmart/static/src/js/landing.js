/**
 * Single Page Multi-Product Landing Page Interactive Engine
 * Handles image gallery, variant switching, quantity adjustments,
 * live pricing calculations, popup checkout modals, and Odoo order submission.
 */

// =============================================================================
// Odoo 19 Compatibility Polyfill: zoomOdoo
// Prevents "this.$(...).zoomOdoo is not a function" when website_root initializes
// before zoomodoo.js is evaluated in web.assets_frontend_lazy.
// =============================================================================
(function () {
    'use strict';
    function ensureZoomOdoo() {
        if (typeof window !== 'undefined') {
            const jq = window.jQuery || window.$;
            if (jq && jq.fn && !jq.fn.zoomOdoo) {
                jq.fn.zoomOdoo = function () {
                    return this;
                };
            }
        }
    }
    ensureZoomOdoo();
    if (typeof window !== 'undefined') {
        window.addEventListener('DOMContentLoaded', ensureZoomOdoo);
        // Intercept late jQuery definitions/reassignments
        let _jq = window.jQuery;
        try {
            Object.defineProperty(window, 'jQuery', {
                configurable: true,
                enumerable: true,
                get: function () { return _jq; },
                set: function (val) {
                    _jq = val;
                    ensureZoomOdoo();
                }
            });
        } catch (e) {}

        let _dollar = window.$;
        try {
            Object.defineProperty(window, '$', {
                configurable: true,
                enumerable: true,
                get: function () { return _dollar; },
                set: function (val) {
                    _dollar = val;
                    ensureZoomOdoo();
                }
            });
        } catch (e) {}
    }
})();

(function () {
    'use strict';

    // Helper: Safely parse a numeric price from an element or string
    function getNumericPrice(el) {
        if (!el) return 0.0;
        if (typeof el === 'number') return el;
        if (el.hasAttribute && el.hasAttribute('data-price')) {
            const p = parseFloat(el.getAttribute('data-price'));
            if (!isNaN(p)) return p;
        }
        const text = (el.textContent || el.value || String(el)).replace(/[^0-9.]/g, '');
        const val = parseFloat(text);
        return isNaN(val) ? 0.0 : val;
    }

    // Helper: Recalculate subtotal, shipping, and grand total for a product checkout
    function recalculateSummary(productIndex) {
        const summaryPriceEl = document.getElementById(`summary-unit-price-${productIndex}`);
        const inputQty = document.getElementById(`input-qty-${productIndex}`);
        const carrierSelect = document.querySelector(`select[name="delivery_carrier_id"][data-product-index="${productIndex}"]`);

        if (!summaryPriceEl || !inputQty) return;

        const unitPrice = getNumericPrice(summaryPriceEl);
        let qty = parseInt(inputQty.value, 10);
        if (isNaN(qty) || qty < 1) qty = 1;

        const subtotal = unitPrice * qty;

        let deliveryPrice = 60.0;
        const checkedRadio = document.querySelector(`input[name="carrier_id"][data-product-index="${productIndex}"]:checked`) || 
                             document.querySelector(`#product-${productIndex}-checkout input[name="carrier_id"]:checked`);
        if (checkedRadio) {
            deliveryPrice = parseFloat(checkedRadio.getAttribute('data-price') || '60.0') || 0.0;
        } else if (carrierSelect && carrierSelect.options && carrierSelect.selectedIndex >= 0) {
            const opt = carrierSelect.options[carrierSelect.selectedIndex];
            if (opt) {
                deliveryPrice = parseFloat(opt.getAttribute('data-price') || '60.0') || 0.0;
            }
        }

        const grandTotal = subtotal + deliveryPrice;

        const calcSubtotal = document.getElementById(`calc-subtotal-${productIndex}`);
        if (calcSubtotal) {
            calcSubtotal.textContent = subtotal.toFixed(2);
        }

        const calcShipping = document.getElementById(`calc-shipping-${productIndex}`);
        if (calcShipping) {
            calcShipping.textContent = deliveryPrice > 0 ? deliveryPrice.toFixed(2) : 'FREE';
        }

        const calcTotal = document.getElementById(`calc-total-${productIndex}`);
        if (calcTotal) {
            calcTotal.textContent = grandTotal.toFixed(2);
        }

        const calcTotalFooter = document.getElementById(`calc-total-footer-${productIndex}`);
        if (calcTotalFooter) {
            calcTotalFooter.textContent = grandTotal.toFixed(2);
        }
    }

    // Helper: Open a Bootstrap modal safely
    function openModalById(modalId) {
        const el = document.getElementById(modalId.replace('#', ''));
        if (!el) return;
        if (window.bootstrap && window.bootstrap.Modal) {
            try {
                const modal = bootstrap.Modal.getOrCreateInstance(el);
                modal.show();
                return;
            } catch (err) {}
        }
        // Fallback for environments without global bootstrap.Modal
        el.classList.add('show');
        el.style.display = 'block';
        el.removeAttribute('aria-hidden');
        el.setAttribute('aria-modal', 'true');
        document.body.classList.add('modal-open');
        if (!document.querySelector('.modal-backdrop')) {
            const backdrop = document.createElement('div');
            backdrop.className = 'modal-backdrop fade show';
            document.body.appendChild(backdrop);
        }
    }

    // Helper: Close a Bootstrap modal safely
    function closeModalById(modalId) {
        const el = document.getElementById(modalId.replace('#', ''));
        if (!el) return;
        if (window.bootstrap && window.bootstrap.Modal) {
            try {
                const inst = bootstrap.Modal.getInstance(el) || bootstrap.Modal.getOrCreateInstance(el);
                if (inst) inst.hide();
            } catch (err) {}
        }
        // Always ensure full manual cleanup so modal NEVER gets stuck
        el.classList.remove('show');
        el.style.display = 'none';
        el.setAttribute('aria-hidden', 'true');
        el.removeAttribute('aria-modal');
        document.body.classList.remove('modal-open');
        document.body.style.removeProperty('overflow');
        document.body.style.removeProperty('padding-right');
        document.querySelectorAll('.modal-backdrop').forEach(b => b.remove());
    }

    // =========================================================================
    // GLOBAL EVENT DELEGATION
    // (Works immediately and permanently, regardless of DOM load timing)
    // =========================================================================

    // 1. CLICK EVENTS
    document.addEventListener('click', function (e) {
        // --- Modal Dismiss / Close Buttons ([data-bs-dismiss="modal"], .btn-close, etc.) ---
        const dismissBtn = e.target.closest('[data-bs-dismiss="modal"], .btn-close, [data-dismiss="modal"]');
        if (dismissBtn) {
            e.preventDefault();
            e.stopPropagation();
            const modalEl = dismissBtn.closest('.modal');
            if (modalEl) {
                closeModalById(modalEl.id);
            }
            return;
        }

        // --- Click on Modal Backdrop to Dismiss (Success Receipt) ---
        if (e.target.classList.contains('modal') && e.target.classList.contains('show')) {
            if (e.target.id === 'landingOrderSuccessModal' || !e.target.hasAttribute('data-bs-backdrop')) {
                closeModalById(e.target.id);
                return;
            }
        }

        // --- Dismiss Product Picker Wrap Button ---
        const dismissPickerBtn = e.target.closest('.landing-picker-dismiss-btn');
        if (dismissPickerBtn) {
            e.preventDefault();
            e.stopPropagation();
            const pickerWrap = dismissPickerBtn.closest('.landing-product-picker-wrap');
            if (pickerWrap) {
                pickerWrap.style.transition = 'all 0.3s ease';
                pickerWrap.style.opacity = '0';
                pickerWrap.style.maxHeight = '0px';
                pickerWrap.style.padding = '0px';
                pickerWrap.style.margin = '0px';
                pickerWrap.style.overflow = 'hidden';
                setTimeout(() => pickerWrap.remove(), 300);
            }
            return;
        }

        // --- Quantity Buttons (+ / -) ---
        const qtyBtn = e.target.closest('.landing-qty-btn');
        if (qtyBtn) {
            e.preventDefault();
            e.stopPropagation();

            const productIndex = qtyBtn.getAttribute('data-product-index');
            const action = qtyBtn.getAttribute('data-action');
            const input = document.getElementById(`input-qty-${productIndex}`);

            if (input) {
                let currentVal = parseInt(input.value, 10);
                if (isNaN(currentVal) || currentVal < 1) currentVal = 1;

                if (action === 'plus') {
                    if (currentVal < 99) currentVal += 1;
                } else if (action === 'minus') {
                    if (currentVal > 1) currentVal -= 1;
                }

                input.value = currentVal;
                recalculateSummary(productIndex);
            }
            return;
        }

        // --- Product Variant Buttons ---
        const variantBtn = e.target.closest('.landing-variant-btn');
        if (variantBtn) {
            e.preventDefault();

            const productIndex = variantBtn.getAttribute('data-product-index');
            const variantId = variantBtn.getAttribute('data-variant-id');
            const variantName = variantBtn.getAttribute('data-name');
            const price = parseFloat(variantBtn.getAttribute('data-price') || '0');

            // Synchronize active states across all chips for this product
            document.querySelectorAll(`.landing-variant-btn[data-product-index="${productIndex}"]`).forEach(btn => {
                if (btn.getAttribute('data-variant-id') === variantId) {
                    btn.classList.add('active');
                } else {
                    btn.classList.remove('active');
                }
            });

            // Update display price on showcase section
            const displayPriceEl = document.getElementById(`display-price-${productIndex}`);
            if (displayPriceEl) {
                displayPriceEl.textContent = price.toFixed(2);
                displayPriceEl.setAttribute('data-price', price);
            }

            // Update checkout summary variant name and unit price
            const summaryNameEl = document.getElementById(`summary-variant-name-${productIndex}`);
            if (summaryNameEl) {
                summaryNameEl.textContent = variantName;
            }

            const summaryPriceEl = document.getElementById(`summary-unit-price-${productIndex}`);
            if (summaryPriceEl) {
                summaryPriceEl.textContent = price.toFixed(2);
                summaryPriceEl.setAttribute('data-price', price);
            }

            // Update hidden input product_id
            const inputProductId = document.getElementById(`input-product-id-${productIndex}`);
            if (inputProductId) {
                inputProductId.value = variantId;
            }

            // Recalculate totals
            recalculateSummary(productIndex);
            return;
        }

        // --- Gallery Thumbnail Buttons ---
        const thumbBtn = e.target.closest('.landing-thumb-btn');
        if (thumbBtn) {
            e.preventDefault();
            const targetId = thumbBtn.getAttribute('data-target');
            const newSrc = thumbBtn.getAttribute('data-src');
            const mainImg = document.getElementById(targetId);

            if (mainImg && newSrc) {
                mainImg.src = newSrc;
                const parentRow = thumbBtn.closest('.landing-thumbnails-row');
                if (parentRow) {
                    parentRow.querySelectorAll('.landing-thumb-btn').forEach(b => b.classList.remove('active'));
                    thumbBtn.classList.add('active');
                }
            }
            return;
        }

        // --- Checkout Modal Opener Links (Links or Buttons targeting -checkout) ---
        const checkoutOpener = e.target.closest('a[href*="-checkout"], button[data-bs-target*="-checkout"], .landing-buy-now-trigger, .snippet-trigger-order');
        if (checkoutOpener) {
            e.preventDefault();
            const section = checkoutOpener.closest('section, .landing-product-section');
            const localModal = section ? section.querySelector('.landing-checkout-modal') : null;
            if (localModal && localModal.id) {
                openModalById(localModal.id);
                return;
            }
            const targetHref = checkoutOpener.getAttribute('href') || checkoutOpener.getAttribute('data-bs-target') || '';
            const match = targetHref.match(/#?(product-[a-zA-Z0-9_-]+-checkout)/);
            if (match) {
                openModalById(match[1]);
                return;
            }
        }

        // --- Smooth Scroll for in-page anchors ---
        const anchor = e.target.closest('a[href^="#"]:not([href*="-checkout"])');
        if (anchor) {
            const href = anchor.getAttribute('href');
            if (href && href !== '#' && !href.includes('-checkout')) {
                const targetEl = document.querySelector(href);
                if (targetEl && !targetEl.classList.contains('modal')) {
                    e.preventDefault();
                    const headerOffset = 70;
                    const elementPosition = targetEl.getBoundingClientRect().top;
                    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                    window.scrollTo({
                        top: offsetPosition,
                        behavior: 'smooth'
                    });
                }
            }
        }
    });

    // 2. INPUT / CHANGE EVENTS FOR QUANTITY & CARRIER
    document.addEventListener('input', function (e) {
        const qtyInput = e.target.closest('.landing-qty-input');
        if (qtyInput) {
            const productIndex = qtyInput.getAttribute('data-product-index');
            let val = parseInt(qtyInput.value, 10);
            if (isNaN(val) || val < 1) val = 1;
            if (val > 99) val = 99;
            qtyInput.value = val;
            recalculateSummary(productIndex);
        }
    });

    document.addEventListener('change', function (e) {
        // --- Carrier select or radio change ---
        const carrierInput = e.target.closest('.landing-carrier-select, .landing-carrier-radio');
        if (carrierInput) {
            const modal = carrierInput.closest('.modal');
            const modalIdMatch = modal && modal.id ? modal.id.match(/\d+/) : null;
            const productIndex = carrierInput.getAttribute('data-product-index') || (modalIdMatch ? modalIdMatch[0] : 'snippet');
            if (carrierInput.type === 'radio') {
                const form = carrierInput.closest('form');
                if (form) {
                    form.querySelectorAll('.landing-carrier-option').forEach(l => l.classList.remove('border-primary'));
                    const parentLabel = carrierInput.closest('.landing-carrier-option');
                    if (parentLabel) parentLabel.classList.add('border-primary');
                }
            }
            recalculateSummary(productIndex);
            return;
        }

        // --- Snippet Admin Product Selector Change Handler ---
        if (e.target && e.target.classList.contains('landing-product-picker-select')) {
            const select = e.target;
            const selectedOpt = select.options[select.selectedIndex];
            if (!selectedOpt || !selectedOpt.value) return;

            const section = select.closest('.landing-product-section, section');
            if (!section) return;

            const variantId = selectedOpt.value;
            const name = selectedOpt.getAttribute('data-name');
            const price = parseFloat(selectedOpt.getAttribute('data-price') || '0');
            const tagline = selectedOpt.getAttribute('data-tagline');
            const imgSrc = selectedOpt.getAttribute('data-img');
            const thumbSrc = selectedOpt.getAttribute('data-thumb') || imgSrc;
            const tmplId = selectedOpt.getAttribute('data-template-id') || variantId;

            section.setAttribute('data-product-template-id', tmplId);
            section.setAttribute('data-product-id', variantId);

            // 1. Update Display Elements in Product Card
            const titleEl = section.querySelector('.snippet-display-title');
            if (titleEl && name) titleEl.textContent = name;

            const taglineEl = section.querySelector('.snippet-display-tagline');
            if (taglineEl && tagline) taglineEl.textContent = tagline;

            const priceEl = section.querySelector('.snippet-display-price');
            if (priceEl && !isNaN(price)) priceEl.textContent = price.toFixed(2);

            const imgEl = section.querySelector('.snippet-display-img');
            if (imgEl && imgSrc) {
                imgEl.src = imgSrc;
                imgEl.alt = name;
            }

            // 2. Update Add-to-cart button
            const cartBtn = section.querySelector('.snippet-trigger-cart, .landing-add-to-cart-btn');
            if (cartBtn && variantId) cartBtn.setAttribute('data-product-id', variantId);

            // 3. Update Modal Elements
            let modal = null;
            const buyBtn = section.querySelector('.landing-buy-now-trigger');
            if (buyBtn && buyBtn.getAttribute('data-bs-target')) {
                modal = document.querySelector(buyBtn.getAttribute('data-bs-target'));
            }
            if (!modal) {
                modal = section.querySelector('.landing-checkout-modal');
            }
            if (modal) {
                const modalTitle = modal.querySelector('.snippet-modal-title, .modal-title');
                if (modalTitle) {
                    modalTitle.textContent = 'অর্ডার সম্পন্ন করুন';
                }

                const summaryTitle = modal.querySelector('.snippet-summary-title, .fw-bold.text-dark.text-truncate');
                if (summaryTitle && name) summaryTitle.textContent = name;

                const summaryImg = modal.querySelector('.snippet-summary-img, .modal-body img');
                if (summaryImg && thumbSrc) summaryImg.src = thumbSrc;

                const summaryUnitPrice = modal.querySelector('#summary-unit-price-snippet, [id^="summary-unit-price-"]');
                if (summaryUnitPrice && !isNaN(price)) {
                    summaryUnitPrice.textContent = price.toFixed(2);
                    summaryUnitPrice.setAttribute('data-price', price);
                }

                const inputProductId = modal.querySelector('#input-product-id-snippet, input[name="product_id"]');
                if (inputProductId && variantId) inputProductId.value = variantId;

                const modalIdMatch = modal.id ? modal.id.match(/\d+/) : null;
                const pIdx = select.getAttribute('data-product-index') || (modalIdMatch ? modalIdMatch[0] : 'snippet');
                recalculateSummary(pIdx);
            }

            // 4. Smoothly remove selector bar completely so ONLY the product card remains
            const pickerWrap = select.closest('.landing-product-picker-wrap');
            if (pickerWrap) {
                pickerWrap.style.transition = 'all 0.35s ease';
                pickerWrap.style.opacity = '0';
                pickerWrap.style.maxHeight = '0px';
                pickerWrap.style.padding = '0px';
                pickerWrap.style.margin = '0px';
                pickerWrap.style.overflow = 'hidden';
                setTimeout(() => {
                    pickerWrap.remove();
                }, 350);
            }

            if (typeof syncProductNamesToMenuAndFooter === 'function') {
                syncProductNamesToMenuAndFooter();
            }
            return;
        }
    });

    // 3. CHECKOUT FORM SUBMISSION
    document.addEventListener('submit', async function (e) {
        const form = e.target.closest('.landing-checkout-form');
        if (!form) return;

        e.preventDefault();
        e.stopPropagation();

        const productIndex = form.getAttribute('data-product-index');
        const submitBtn = document.getElementById(`submit-btn-${productIndex}`);
        const errorAlert = document.getElementById(`error-alert-${productIndex}`);

        // Reset errors
        if (errorAlert) {
            errorAlert.classList.add('d-none');
            errorAlert.textContent = '';
        }
        form.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));

        // Collect form data
        const formData = new FormData(form);
        const name = (formData.get('name') || formData.get('customer_name') || '').trim();
        const phone = (formData.get('phone') || formData.get('customer_phone') || '').trim();
        let email = (formData.get('email') || '').trim();
        if (!email) {
            const cleanDigits = phone.replace(/[^0-9]/g, '') || Math.floor(Math.random() * 100000);
            email = `guest_${cleanDigits}@order.local`;
        }
        const street = (formData.get('street') || formData.get('customer_address') || '').trim();
        const city = (formData.get('city') || 'Local Area').trim();
        const orderNotes = (formData.get('order_notes') || '').trim();
        const productId = parseInt(formData.get('product_id'), 10);
        const quantity = parseInt(formData.get('quantity') || '1', 10);
        const carrierId = formData.get('carrier_id') || formData.get('delivery_carrier_id') ? parseInt(formData.get('carrier_id') || formData.get('delivery_carrier_id'), 10) : false;

        // Fast client validation (Name, Phone, Address are essential)
        let hasError = false;
        if (!name) {
            const input = form.querySelector('[name="name"], [name="customer_name"]');
            if (input) input.classList.add('is-invalid');
            hasError = true;
        }
        if (!phone) {
            const input = form.querySelector('[name="phone"], [name="customer_phone"]');
            if (input) input.classList.add('is-invalid');
            hasError = true;
        }
        if (!street) {
            const input = form.querySelector('[name="street"], [name="customer_address"]');
            if (input) input.classList.add('is-invalid');
            hasError = true;
        }

        if (hasError) {
            if (errorAlert) {
                errorAlert.textContent = 'অনুগ্রহ করে আপনার নাম, মোবাইল নম্বর এবং ডেলিভারি ঠিকানা লিখুন।';
                errorAlert.classList.remove('d-none');
            }
            return;
        }

        // Disable button & show spinner to prevent duplicate orders
        if (submitBtn) {
            submitBtn.disabled = true;
            const spinner = submitBtn.querySelector('.spinner-border');
            const btnText = submitBtn.querySelector('.btn-text');
            if (spinner) spinner.classList.remove('d-none');
            if (btnText) btnText.textContent = 'অর্ডার গ্রহণ করা হচ্ছে...';
        }

        const payload = {
            product_id: productId,
            quantity: quantity,
            name: name,
            phone: phone,
            email: email,
            street: street,
            city: city || 'Local Area',
            order_notes: orderNotes,
            delivery_carrier_id: carrierId,
            payment_method: 'cod',
        };

        try {
            const response = await fetch('/landing/submit_order', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    jsonrpc: '2.0',
                    method: 'call',
                    params: payload,
                    id: Math.floor(Math.random() * 1000000),
                }),
            });

            const data = await response.json();
            const result = data.result || {};

            if (result.status === 'success') {
                // 1. Close checkout modal
                const modalEl = form.closest('.modal');
                if (modalEl && modalEl.id) {
                    closeModalById(modalEl.id);
                } else {
                    closeModalById(`product-${productIndex}-checkout`);
                }

                // 2. Populate Order Confirmation Receipt Modal
                const setEl = (id, val) => {
                    const el = document.getElementById(id);
                    if (el) el.textContent = val;
                };

                const currSym = result.currency_symbol || '৳';
                const bookPriceVal = (result.price_unit != null && result.price_unit > 0)
                    ? (Number(result.price_unit) * Number(result.quantity || 1))
                    : (result.amount_untaxed != null && result.amount_delivery != null
                        ? Math.max(0, Number(result.amount_untaxed) - Number(result.amount_delivery))
                        : Number(result.amount_untaxed || 350));
                const delivVal = Number(result.amount_delivery || 0);
                const totalVal = (result.amount_total != null && result.amount_total > 0)
                    ? Number(result.amount_total)
                    : (bookPriceVal + delivVal);

                // Populate actual element IDs in landingOrderSuccessModal
                setEl('successOrderRef', result.order_name || 'Confirmed');
                setEl('successProductName', result.product_name || 'বই');
                setEl('successCustomerName', result.customer_name || name);
                setEl('successCustomerPhone', result.customer_phone || phone);
                setEl('successCustomerAddress', result.delivery_address || street);
                setEl('successSubtotal', `${currSym}${bookPriceVal.toFixed(2)}`);
                setEl('successDelivery', delivVal > 0 ? `${currSym}${delivVal.toFixed(2)}` : 'ফ্রি');
                setEl('successTotal', result.amount_total_formatted || `${currSym}${totalVal.toFixed(2)}`);

                // Backward compatibility for modal* IDs
                setEl('modalOrderRef', result.order_name || 'Confirmed');
                setEl('modalProductName', result.product_name || 'বই');
                setEl('modalProductQty', result.quantity || 1);
                setEl('modalSubtotal', `${currSym}${bookPriceVal.toFixed(2)}`);
                setEl('modalDelivery', delivVal > 0 ? `${currSym}${delivVal.toFixed(2)}` : 'FREE');
                setEl('modalTotalAmount', result.amount_total_formatted || `${currSym}${totalVal.toFixed(2)}`);
                setEl('modalCustomerName', result.customer_name || name);
                setEl('modalCustomerPhone', result.customer_phone || phone);
                setEl('modalCustomerAddress', result.delivery_address || street);
                setEl('modalPaymentMethod', result.payment_method || 'Cash on Delivery');

                // 3. Open Success Modal
                setTimeout(() => {
                    openModalById('landingOrderSuccessModal');
                }, 200);

                // 4. Reset form & update cart badge
                form.reset();
                recalculateSummary(productIndex);

                const badge = document.querySelector('.landing-cart-badge');
                if (badge) {
                    const currentQty = parseInt(badge.textContent, 10) || 0;
                    badge.textContent = currentQty + (result.quantity || 1);
                }

            } else {
                if (errorAlert) {
                    errorAlert.textContent = result.message || 'অর্ডার সম্পন্ন করা সম্ভব হয়নি। অনুগ্রহ করে তথ্যগুলো আবার যাচাই করুন।';
                    errorAlert.classList.remove('d-none');
                }
            }

        } catch (err) {
            console.error('Order submission error:', err);
            if (errorAlert) {
                errorAlert.textContent = 'নেটওয়ার্ক সংযোগে সমস্যা হয়েছে। অনুগ্রহ করে ইন্টারনেট সংযোগ চেক করে আবার চেষ্টা করুন।';
                errorAlert.classList.remove('d-none');
            }
        } finally {
            if (submitBtn) {
                submitBtn.disabled = false;
                const spinner = submitBtn.querySelector('.spinner-border');
                const btnText = submitBtn.querySelector('.btn-text');
                if (spinner) spinner.classList.add('d-none');
                if (btnText) btnText.textContent = 'Confirm Order';
            }
        }
    });

    // Smooth animated slide to target section
    document.addEventListener('click', function (e) {
        const link = e.target.closest('a[href^="#product-"]');
        if (link) {
            const targetId = link.getAttribute('href');
            if (targetId && targetId.startsWith('#')) {
                const targetEl = document.querySelector(targetId);
                if (targetEl) {
                    e.preventDefault();
                    targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    const card = targetEl.querySelector('.landing-product-card');
                    if (card) {
                        card.classList.add('landing-card-slide-active');
                    }
                }
            }
        }
    });

    // -------------------------------------------------------------
    // Add to Cart Functionality (Multi-Product Order Support)
    // -------------------------------------------------------------
    function showCartFloatingToast(productName, cartQuantity) {
        let toast = document.getElementById('landing-cart-toast');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'landing-cart-toast';
            document.body.appendChild(toast);
        }

        toast.innerHTML = `
            <div class="rounded-circle bg-success text-white d-flex align-items-center justify-content-center flex-shrink-0" style="width: 36px; height: 36px; font-size: 1rem;">
                <i class="fa fa-shopping-bag"></i>
            </div>
            <div class="flex-grow-1 overflow-hidden" style="min-width: 0; line-height: 1.25;">
                <div class="fw-bold text-white text-truncate small">${productName || 'বই'}</div>
                <div class="text-white-50" style="font-size: 0.76rem;">কার্টে যোগ হয়েছে! (মোট: <strong class="text-warning">${cartQuantity}</strong>)</div>
            </div>
            <button type="button" class="btn btn-warning btn-sm rounded-pill fw-bold text-dark text-nowrap px-2.5 py-1.5 shadow-sm landing-open-cart-checkout flex-shrink-0" style="font-size: 0.8rem;" data-bs-toggle="modal" data-bs-target="#landingCartCheckoutModal">
                কার্ট চেকআউট
            </button>
            <button type="button" class="btn-close btn-close-white small flex-shrink-0" aria-label="Close" onclick="const t = this.closest('#landing-cart-toast'); if (t) { t.style.opacity='0'; setTimeout(()=>t.remove(), 250); }"></button>
        `;

        toast.style.opacity = '1';
        toast.style.transform = 'translateY(0)';

        if (window._cartToastTimer) clearTimeout(window._cartToastTimer);
        window._cartToastTimer = setTimeout(() => {
            if (toast && toast.parentElement) {
                toast.style.opacity = '0';
                toast.style.transform = 'translateY(15px)';
                setTimeout(() => toast.remove(), 300);
            }
        }, 5000);
    }

    document.addEventListener('click', async function (e) {
        const btn = e.target.closest('.landing-add-to-cart-btn');
        if (!btn) return;
        e.preventDefault();

        const btnText = btn.querySelector('.btn-text');
        const spinner = btn.querySelector('.spinner-border');
        const icon = btn.querySelector('i');
        const originalText = btnText ? btnText.textContent : 'কার্টে যোগ করুন • Add to Cart';

        // Find associated product
        const productIndex = btn.getAttribute('data-product-index') || '1';
        const section = btn.closest('.landing-product-section');
        let tmplId = btn.getAttribute('data-product-template-id');
        let prodId = btn.getAttribute('data-product-id');

        if (section) {
            tmplId = tmplId || section.getAttribute('data-product-template-id');
            prodId = prodId || section.getAttribute('data-product-id');
        }

        // Try modal input if not found on section
        const modal = document.getElementById(`product-${productIndex}-checkout`) || (section && section.querySelector('.landing-checkout-modal'));
        if (modal) {
            const inputProd = modal.querySelector('input[name="product_id"]');
            if (inputProd && inputProd.value) {
                prodId = prodId || inputProd.value;
            }
        }

        if (!prodId && !tmplId) {
            // Default fallback based on productIndex
            if (productIndex === '1') { tmplId = 6; prodId = 23; }
            else if (productIndex === '2') { tmplId = 8; prodId = 24; }
            else if (productIndex === '3') { tmplId = 11; prodId = 25; }
        } else if (!prodId && tmplId) {
            if (tmplId == 6) prodId = 23;
            else if (tmplId == 8) prodId = 24;
            else if (tmplId == 11) prodId = 25;
            else prodId = tmplId;
        }

        // UI Loading state
        btn.disabled = true;
        if (spinner) spinner.classList.remove('d-none');
        if (btnText) btnText.textContent = 'যোগ করা হচ্ছে...';

        try {
            const resp = await fetch('/shop/cart/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: JSON.stringify({
                    jsonrpc: '2.0',
                    method: 'call',
                    params: {
                        product_id: parseInt(prodId, 10),
                        product_template_id: parseInt(tmplId, 10),
                        quantity: 1,
                    },
                    id: Math.floor(Math.random() * 1000000),
                }),
            });

            const data = await resp.json();
            const res = data.result;

            if (res && res.cart_quantity !== undefined) {
                // Update Sticky Header Cart Badge
                const badges = document.querySelectorAll('.landing-cart-badge');
                badges.forEach(b => {
                    b.textContent = res.cart_quantity;
                    b.classList.remove('bg-dark');
                    b.classList.add('bg-warning', 'text-dark');
                });

                // Sync with local cart for instant checkout modal
                const prodTitle = (section && section.querySelector('.snippet-display-title')?.textContent.trim()) || 
                                  (res.notification_info && res.notification_info.lines && res.notification_info.lines[0]?.name) || 'Product';

                try {
                    const priceText = section ? (section.querySelector('.snippet-display-price')?.textContent || '350') : '350';
                    const itemPrice = parseFloat(priceText.replace(/[^0-9.]/g, '') || '350');
                    const itemImg = section ? (section.querySelector('.landing-main-img')?.src || '') : '';
                    let localCart = JSON.parse(localStorage.getItem('landing_cart') || '[]');
                    let existing = localCart.find(i => i.id == prodId);
                    if (existing) {
                        existing.qty += 1;
                    } else {
                        localCart.push({
                            id: parseInt(prodId, 10),
                            name: prodTitle,
                            price: itemPrice,
                            qty: 1,
                            img: itemImg
                        });
                    }
                    localStorage.setItem('landing_cart', JSON.stringify(localCart));
                } catch (e) {
                    console.warn('LocalStorage cart error:', e);
                }

                // Success Feedback on Button
                btn.classList.remove('btn-outline-dark');
                btn.classList.add('btn-success', 'text-white', 'border-success');
                if (icon) icon.className = 'fa fa-check me-1';
                if (btnText) btnText.textContent = 'কার্টে যোগ হয়েছে! ✓';

                showCartFloatingToast(prodTitle, res.cart_quantity);

                setTimeout(() => {
                    btn.classList.remove('btn-success', 'text-white', 'border-success');
                    btn.classList.add('btn-outline-dark');
                    if (icon) icon.className = 'fa fa-shopping-bag me-1';
                    if (btnText) btnText.textContent = originalText;
                    btn.disabled = false;
                }, 2200);

            } else {
                const errorMsg = (data.error && data.error.data && data.error.data.message) || (res ? res.message : 'Error adding product to cart.');
                console.warn('Add to cart response issue:', data);
                btn.disabled = false;
                if (btnText) btnText.textContent = originalText;
            }
        } catch (err) {
            console.error('Add to cart network error:', err);
            btn.disabled = false;
            if (btnText) btnText.textContent = originalText;
        } finally {
            if (spinner) spinner.classList.add('d-none');
        }
    });

    // -------------------------------------------------------------
    // Multi-Product Cart Checkout Modal Engine
    // -------------------------------------------------------------
    const cartModal = document.getElementById('landingCartCheckoutModal');
    const cartItemsContainer = document.getElementById('cartModalItemsContainer');
    const cartSubtotalEl = document.getElementById('cartModalSubtotal');
    const cartDeliveryEl = document.getElementById('cartModalDelivery');
    const cartGrandTotalEl = document.getElementById('cartModalGrandTotal');
    const cartPayableEl = document.getElementById('cartModalPayable');
    const cartSubmitBtn = document.getElementById('cartSubmitBtn');
    const cartSubmitBtnText = document.getElementById('cartSubmitBtnText');
    const cartForm = document.getElementById('landingCartCheckoutForm');

    function getSelectedCartCarrierId() {
        const checked = document.querySelector('input[name="cart_delivery_carrier_id"]:checked');
        return checked ? parseInt(checked.value) : 1;
    }

    function renderClientCart() {
        let cart = [];
        try {
            cart = JSON.parse(localStorage.getItem('landing_cart') || '[]');
        } catch (e) { cart = []; }

        const carrierId = getSelectedCartCarrierId();
        const deliveryCharge = carrierId === 2 ? 120.0 : 60.0;
        const carrierName = carrierId === 2 ? 'ঢাকার বাইরে' : 'ঢাকার ভেতরে';

        let subtotal = 0;
        const items = cart.map(i => {
            const lineSub = (i.price || 350) * (i.qty || 1);
            subtotal += lineSub;
            return {
                line_id: i.id,
                product_id: i.id,
                name: i.name,
                price: i.price || 350,
                price_formatted: `৳${(i.price || 350).toFixed(2)}`,
                quantity: i.qty || 1,
                subtotal: lineSub,
                subtotal_formatted: `৳${lineSub.toFixed(2)}`,
                image_url: i.img || '/bookmart/static/src/img/book_atomic_habits.jpg'
            };
        });

        const total = subtotal + deliveryCharge;
        renderCartModal({
            status: 'success',
            cart_quantity: cart.reduce((acc, i) => acc + (i.qty || 0), 0),
            items: items,
            subtotal: subtotal,
            subtotal_formatted: `৳${subtotal.toFixed(2)}`,
            delivery_charge: deliveryCharge,
            delivery_formatted: `৳${deliveryCharge.toFixed(2)}`,
            carrier_name: carrierName,
            total: total,
            total_formatted: `৳${total.toFixed(2)}`
        });
    }

    async function loadCartData() {
        if (!cartItemsContainer) return;
        cartItemsContainer.innerHTML = `
            <div class="text-center py-4 text-muted small">
                <i class="fa fa-spinner fa-spin fa-2x mb-2 text-secondary"></i>
                <div>কার্ট লোড করা হচ্ছে...</div>
            </div>`;

        try {
            const carrierId = getSelectedCartCarrierId();
            const resp = await fetch('/landing/get_cart_data', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    jsonrpc: '2.0',
                    method: 'call',
                    params: { carrier_id: carrierId },
                    id: Math.floor(Math.random() * 100000)
                })
            });
            if (resp.ok) {
                const data = await resp.json();
                if (data.result && data.result.status === 'success' && data.result.items && data.result.items.length > 0) {
                    renderCartModal(data.result);
                    return;
                }
            }
        } catch (err) {}

        renderClientCart();
    }

    function renderCartModal(data) {
        if (!cartItemsContainer) return;

        // Update all badges across page
        document.querySelectorAll('.landing-cart-badge').forEach(b => {
            b.textContent = data.cart_quantity || 0;
            if (data.cart_quantity > 0) {
                b.classList.remove('bg-dark');
                b.classList.add('bg-warning', 'text-dark');
            } else {
                b.classList.remove('bg-warning', 'text-dark');
                b.classList.add('bg-dark', 'text-white');
            }
        });

        if (!data.items || data.items.length === 0) {
            cartItemsContainer.innerHTML = `
                <div class="text-center py-4 text-muted">
                    <div class="rounded-circle bg-light d-inline-flex p-3 mb-2 text-secondary">
                        <i class="fa fa-shopping-bag fa-2x"></i>
                    </div>
                    <div class="fw-bold text-dark mb-1">আপনার কার্ট বর্তমানে খালি আছে!</div>
                    <div class="small text-muted">বই কিনতে ল্যান্ডিং পেজের "কার্টে যোগ করুন" বাটনে ক্লিক করুন।</div>
                </div>`;
            if (cartSubtotalEl) cartSubtotalEl.textContent = '৳০.০০';
            if (cartDeliveryEl) cartDeliveryEl.textContent = '৳০.০০';
            if (cartGrandTotalEl) cartGrandTotalEl.textContent = '৳০.০০';
            if (cartPayableEl) cartPayableEl.textContent = '৳০.০০';
            if (cartSubmitBtn) {
                cartSubmitBtn.disabled = true;
                cartSubmitBtn.classList.add('opacity-50');
            }
            return;
        }

        if (cartSubmitBtn) {
            cartSubmitBtn.disabled = false;
            cartSubmitBtn.classList.remove('opacity-50');
        }

        let html = '';
        data.items.forEach(item => {
            html += `
                <div class="d-flex align-items-center justify-content-between p-2.5 rounded-3 border bg-light-subtle gap-2">
                    <img src="${item.image_url}" class="rounded border bg-white flex-shrink-0" style="width: 44px; height: 56px; object-fit: cover;" alt="${item.name}"/>
                    <div class="flex-grow-1 min-w-0">
                        <div class="fw-bold text-dark text-truncate small" title="${item.name}">${item.name}</div>
                        <div class="text-muted small">${item.price_formatted} × ${item.quantity} = <strong class="text-dark">${item.subtotal_formatted}</strong></div>
                    </div>
                    <div class="d-flex align-items-center gap-1 flex-shrink-0">
                        <button type="button" class="btn btn-sm btn-outline-secondary cart-qty-action-btn p-0 d-flex align-items-center justify-content-center" data-line-id="${item.line_id}" data-action="decrease" data-qty="${item.quantity}" style="width: 24px; height: 24px; font-weight: bold; line-height: 1;">-</button>
                        <span class="fw-bold small px-1 text-center" style="min-width: 20px;">${item.quantity}</span>
                        <button type="button" class="btn btn-sm btn-outline-secondary cart-qty-action-btn p-0 d-flex align-items-center justify-content-center" data-line-id="${item.line_id}" data-action="increase" data-qty="${item.quantity}" style="width: 24px; height: 24px; font-weight: bold; line-height: 1;">+</button>
                        <button type="button" class="btn btn-sm text-danger cart-remove-action-btn p-0 ms-1 d-flex align-items-center justify-content-center" data-line-id="${item.line_id}" title="মুছে ফেলুন" style="width: 22px; height: 22px;"><i class="fa fa-trash"></i></button>
                    </div>
                </div>`;
        });
        cartItemsContainer.innerHTML = html;

        if (cartSubtotalEl) cartSubtotalEl.textContent = data.subtotal_formatted;
        if (cartDeliveryEl) cartDeliveryEl.textContent = data.delivery_formatted;
        if (cartGrandTotalEl) cartGrandTotalEl.textContent = data.total_formatted;
        if (cartPayableEl) cartPayableEl.textContent = data.total_formatted;
    }

    if (cartModal) {
        cartModal.addEventListener('show.bs.modal', () => {
            loadCartData();
        });
    }

    document.querySelectorAll('input[name="cart_delivery_carrier_id"]').forEach(radio => {
        radio.addEventListener('change', () => {
            loadCartData();
        });
    });

    if (cartItemsContainer) {
        cartItemsContainer.addEventListener('click', async (e) => {
            const qtyBtn = e.target.closest('.cart-qty-action-btn');
            const removeBtn = e.target.closest('.cart-remove-action-btn');

            if (qtyBtn) {
                const lineId = qtyBtn.getAttribute('data-line-id');
                const action = qtyBtn.getAttribute('data-action');
                const curQty = parseInt(qtyBtn.getAttribute('data-qty') || 1);
                const newQty = action === 'increase' ? curQty + 1 : curQty - 1;

                qtyBtn.disabled = true;
                await updateCartLine(lineId, newQty);
            } else if (removeBtn) {
                const lineId = removeBtn.getAttribute('data-line-id');
                removeBtn.disabled = true;
                await updateCartLine(lineId, 0);
            }
        });
    }

    async function updateCartLine(lineId, quantity) {
        try {
            const carrierId = getSelectedCartCarrierId();
            const resp = await fetch('/landing/update_cart_line', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    jsonrpc: '2.0',
                    method: 'call',
                    params: {
                        line_id: parseInt(lineId),
                        quantity: quantity,
                        carrier_id: carrierId
                    },
                    id: Math.floor(Math.random() * 100000)
                })
            });
            if (resp.ok) {
                const data = await resp.json();
                if (data.result && data.result.status === 'success') {
                    renderCartModal(data.result);
                    return;
                }
            }
        } catch (err) {}

        // Fallback: update in localStorage
        try {
            let cart = JSON.parse(localStorage.getItem('landing_cart') || '[]');
            if (quantity <= 0) {
                cart = cart.filter(i => i.id != lineId);
            } else {
                const item = cart.find(i => i.id == lineId);
                if (item) item.qty = quantity;
            }
            localStorage.setItem('landing_cart', JSON.stringify(cart));
        } catch (e) {}

        renderClientCart();
    }

    function onCartOrderSuccess(res, customerName, customerPhone, deliveryAddress) {
        try {
            localStorage.removeItem('landing_cart');
        } catch (e) {}

        if (cartForm) cartForm.reset();
        document.querySelectorAll('.landing-cart-badge').forEach(b => {
            b.textContent = '0';
            b.classList.remove('bg-warning', 'text-dark');
            b.classList.add('bg-dark', 'text-white');
        });

        // Close cart modal
        if (window.bootstrap && bootstrap.Modal) {
            const mInstance = bootstrap.Modal.getInstance(cartModal) || new bootstrap.Modal(cartModal);
            mInstance.hide();
        } else if (cartModal) {
            cartModal.classList.remove('show');
            cartModal.style.display = 'none';
            document.body.classList.remove('modal-open');
            const bd = document.querySelector('.modal-backdrop');
            if (bd) bd.remove();
        }

        // Open Success Modal
        const successModal = document.getElementById('landingOrderSuccessModal');
        if (successModal) {
            const refEl = document.getElementById('successOrderRef');
            const nameEl = document.getElementById('successCustomerName');
            const phoneEl = document.getElementById('successCustomerPhone');
            const addrEl = document.getElementById('successCustomerAddress');
            const prodEl = document.getElementById('successProductName');
            const subtotalEl = document.getElementById('successSubtotal');
            const delivEl = document.getElementById('successDelivery');
            const totalEl = document.getElementById('successTotal');

            if (refEl) refEl.textContent = res.order_name || 'Confirmed';
            if (nameEl) nameEl.textContent = res.customer_name || customerName;
            if (phoneEl) phoneEl.textContent = res.customer_phone || customerPhone;
            if (addrEl) addrEl.textContent = res.delivery_address || deliveryAddress;
            if (prodEl) prodEl.textContent = res.product_name || 'অর্ডারকৃত বইসমূহ';
            const currSym = res.currency_symbol || '৳';
            const delivVal = Number(res.amount_delivery || 0);
            const bookPriceVal = (res.amount_untaxed != null && delivVal > 0)
                ? Math.max(0, Number(res.amount_untaxed) - delivVal)
                : ((res.subtotal != null && res.subtotal > 0) ? Number(res.subtotal) : Number(res.amount_untaxed || 0));
            const totalVal = (res.amount_total != null) ? Number(res.amount_total) : (bookPriceVal + delivVal);

            if (subtotalEl) subtotalEl.textContent = `${currSym}${bookPriceVal.toFixed(2)}`;
            if (delivEl) delivEl.textContent = delivVal > 0 ? `${currSym}${delivVal.toFixed(2)}` : 'ফ্রি';
            if (totalEl) totalEl.textContent = res.amount_total_formatted || `${currSym}${totalVal.toFixed(2)}`;

            if (window.bootstrap && bootstrap.Modal) {
                new bootstrap.Modal(successModal).show();
            } else {
                successModal.classList.add('show');
                successModal.style.display = 'block';
                document.body.classList.add('modal-open');
            }
        }
    }

    if (cartForm) {
        cartForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const name = (cartForm.querySelector('input[name="name"]')?.value || '').trim();
            const phone = (cartForm.querySelector('input[name="phone"]')?.value || '').trim();
            const street = (cartForm.querySelector('textarea[name="street"]')?.value || '').trim();
            const carrierId = getSelectedCartCarrierId();

            if (!name || !phone || !street) {
                alert('অনুগ্রহ করে আপনার নাম, মোবাইল নম্বর এবং ডেলিভারি ঠিকানা লিখুন।');
                return;
            }

            if (cartSubmitBtn) {
                cartSubmitBtn.disabled = true;
                if (cartSubmitBtnText) {
                    cartSubmitBtnText.innerHTML = '<i class="fa fa-spinner fa-spin"></i> অর্ডার গ্রহণ করা হচ্ছে...';
                }
            }

            // 1. Try server endpoint first
            try {
                const resp = await fetch('/landing/submit_cart_order', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        jsonrpc: '2.0',
                        method: 'call',
                        params: {
                            name: name,
                            phone: phone,
                            street: street,
                            delivery_carrier_id: carrierId
                        },
                        id: Math.floor(Math.random() * 100000)
                    })
                });

                if (resp.ok) {
                    const data = await resp.json();
                    if (data.result && data.result.status === 'success') {
                        onCartOrderSuccess(data.result, name, phone, street);
                        return;
                    }
                }
            } catch (err) {}

            // 2. Fallback: submit using live /landing/submit_order endpoint
            try {
                const cart = JSON.parse(localStorage.getItem('landing_cart') || '[]');
                if (!cart.length) {
                    alert('আপনার কার্ট বর্তমানে খালি আছে।');
                    return;
                }

                const cleanDigits = phone.replace(/[^0-9]/g, '') || Math.floor(Math.random() * 100000);
                const email = `guest_${cleanDigits}@order.local`;
                const city = carrierId === 1 ? 'ঢাকা' : 'ঢাকার বাইরে';

                let mainOrderResult = null;
                let productSummaries = [];
                let totalAmount = 0;

                for (let idx = 0; idx < cart.length; idx++) {
                    const item = cart[idx];
                    productSummaries.push(`${item.name} (x${item.qty})`);
                    const itemCarrier = idx === 0 ? carrierId : false; // carrier charge only once

                    const orderResp = await fetch('/landing/submit_order', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            jsonrpc: '2.0',
                            method: 'call',
                            params: {
                                product_id: item.id,
                                quantity: item.qty,
                                name: name,
                                phone: phone,
                                email: email,
                                street: street,
                                city: city,
                                delivery_carrier_id: itemCarrier,
                                order_notes: `কার্ট অর্ডার: ${item.name} (x${item.qty})`,
                                payment_method: 'cod'
                            },
                            id: Math.floor(Math.random() * 100000)
                        })
                    });

                    const orderData = await orderResp.json();
                    if (orderData.result && orderData.result.status === 'success') {
                        if (!mainOrderResult) mainOrderResult = orderData.result;
                        totalAmount += (orderData.result.amount_total || (item.price * item.qty));
                    }
                }

                if (mainOrderResult) {
                    mainOrderResult.product_name = productSummaries.join(', ');
                    mainOrderResult.amount_total_formatted = `৳${(totalAmount + (carrierId === 2 ? 120 : 60)).toFixed(2)}`;
                    onCartOrderSuccess(mainOrderResult, name, phone, street);
                } else {
                    alert('অর্ডার সম্পন্ন করতে সমস্যা হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।');
                }
            } catch (err) {
                console.error('Order submit error:', err);
                alert('নেটওয়ার্ক ত্রুটি। অনুগ্রহ করে আবার চেষ্টা করুন।');
            } finally {
                if (cartSubmitBtn) {
                    cartSubmitBtn.disabled = false;
                    if (cartSubmitBtnText) {
                        cartSubmitBtnText.textContent = 'অর্ডার কনফার্ম করুন';
                    }
                }
            }
        });
    }

    // Initialize cart badge from localStorage on page load
    try {
        const savedCart = JSON.parse(localStorage.getItem('landing_cart') || '[]');
        const totalQty = savedCart.reduce((sum, item) => sum + (item.qty || 0), 0);
        if (totalQty > 0) {
            document.querySelectorAll('.landing-cart-badge').forEach(b => {
                b.textContent = totalQty;
                b.classList.remove('bg-dark');
                b.classList.add('bg-warning', 'text-dark');
            });
        }
    } catch (e) {}

    // Automatic Product Synchronization to Header Menu, Hero Strip & Footer
    function syncProductNamesToMenuAndFooter() {
        [1, 2, 3].forEach(idx => {
            const section = document.getElementById(`product-${idx}`);
            if (!section) return;
            const titleEl = section.querySelector('.snippet-display-title');
            if (!titleEl) return;
            const name = titleEl.textContent.trim();
            if (!name) return;

            // Header navigation has a single unified "Products" link pointing to #product-1 (do not overwrite)
            // Footer & Hero Quick Jump Strip continue to sync dynamically

            // Update Hero Quick Jump Strip
            const stripCard = document.querySelector(`.landing-product-strip-wrapper a[href="#product-${idx}"]`);
            if (stripCard) {
                const stripTitle = stripCard.querySelector('.fw-bold.text-dark.text-truncate');
                if (stripTitle && stripTitle.textContent.trim() !== name) {
                    stripTitle.textContent = name;
                }
                const priceEl = section.querySelector('.snippet-display-price');
                const stripPrice = stripCard.querySelector('.fw-bold.text-primary');
                if (priceEl && stripPrice) {
                    const priceVal = priceEl.textContent.trim();
                    if (priceVal) stripPrice.textContent = '৳' + priceVal;
                }
                const mainImg = section.querySelector('.landing-main-img');
                const stripImg = stripCard.querySelector('img');
                if (mainImg && stripImg && mainImg.src && stripImg.src !== mainImg.src) {
                    stripImg.src = mainImg.src;
                    stripImg.alt = name;
                }
            }

            // Update Footer Product Link
            const footerLinks = document.querySelectorAll(`footer a[href="#product-${idx}"]`);
            footerLinks.forEach(link => {
                if (link.textContent.trim() !== name) {
                    link.textContent = name;
                }
            });
        });
    }

    // Observe inline edits to product titles in Website Editor so menu and footer update instantly
    function initTitleSyncObserver() {
        const titles = document.querySelectorAll('.snippet-display-title');
        if (!titles.length || !window.MutationObserver) return;
        const observer = new MutationObserver(() => {
            syncProductNamesToMenuAndFooter();
        });
        titles.forEach(t => {
            observer.observe(t, { childList: true, characterData: true, subtree: true });
        });
    }

    // Auto Card Slide-Up on Scroll Engine (IntersectionObserver)
    // Re-triggers every single time the user scrolls to each product card ("potibar hbe")
    function initCardSlideObserver() {
        const cards = document.querySelectorAll('.landing-product-card');
        if (!cards.length) return;

        if ('IntersectionObserver' in window) {
            const observerOptions = {
                root: null,
                rootMargin: '0px 0px -12% 0px',
                threshold: 0.10
            };

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('landing-card-slide-active');
                    } else {
                        // Reset when leaving view so it slides in EVERY TIME!
                        if (entry.target === cards[0] && window.scrollY < 250) {
                            entry.target.classList.add('landing-card-slide-active');
                            return;
                        }
                        entry.target.classList.remove('landing-card-slide-active');
                    }
                });
            }, observerOptions);

            cards.forEach((card, idx) => {
                card.classList.add('landing-card-slide-ready');
                // Ensure first product card is displayed immediately if near top
                if (idx === 0 && window.scrollY < 250) {
                    setTimeout(() => card.classList.add('landing-card-slide-active'), 50);
                }
                observer.observe(card);
            });
        } else {
            cards.forEach(card => card.classList.add('landing-card-slide-active'));
        }
    }

    // -------------------------------------------------------------
    // Light & Dark Mode Toggle System
    // -------------------------------------------------------------
    function applyTheme(theme) {
        if (theme === 'dark') {
            document.body.classList.add('dark-mode');
            document.documentElement.setAttribute('data-bs-theme', 'dark');
            const root = document.querySelector('.landing-page-root');
            if (root) root.classList.add('dark-mode');
            const wrap = document.getElementById('wrapwrap');
            if (wrap) wrap.classList.add('dark-mode');
        } else {
            document.body.classList.remove('dark-mode');
            document.documentElement.setAttribute('data-bs-theme', 'light');
            const root = document.querySelector('.landing-page-root');
            if (root) root.classList.remove('dark-mode');
            const wrap = document.getElementById('wrapwrap');
            if (wrap) wrap.classList.remove('dark-mode');
        }
    }

    function initThemeMode() {
        const savedTheme = localStorage.getItem('landing_theme') || 'light';
        applyTheme(savedTheme);

        document.addEventListener('click', function (e) {
            const toggleBtn = e.target.closest('.landing-theme-toggle');
            if (!toggleBtn) return;
            e.preventDefault();
            const isDark = document.body.classList.contains('dark-mode') || document.documentElement.getAttribute('data-bs-theme') === 'dark';
            const newTheme = isDark ? 'light' : 'dark';
            applyTheme(newTheme);
            localStorage.setItem('landing_theme', newTheme);
        });
    }

    // -------------------------------------------------------------
    // Sticky Header Frosted Glass Dynamic Scroll Effect
    // -------------------------------------------------------------
    function initHeaderScrollEffect() {
        const header = document.querySelector('.landing-header');
        if (!header) return;
        const onScroll = () => {
            if (window.scrollY > 25) {
                header.classList.add('landing-header-scrolled');
            } else {
                header.classList.remove('landing-header-scrolled');
            }
        };
        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll();
    }

    // Initialize all summaries & slide animations
    function initAll() {
        initThemeMode();
        initHeaderScrollEffect();
        [1, 2, 3, 'snippet'].forEach(idx => recalculateSummary(idx));
        syncProductNamesToMenuAndFooter();
        initTitleSyncObserver();
        initCardSlideObserver();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAll);
    } else {
        initAll();
    }

})();
