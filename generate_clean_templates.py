# -*- coding: utf-8 -*-
import os

TEMPLATES_XML = '''<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Master Landing Page View -->
    <template id="landing_page" name="Single Page Multi-Product Landing">
        <t t-call="website.layout">
            <t t-set="additional_title" t-value="'Exclusive 3-Product Flagship Showcase'"/>
            <t t-set="no_header" t-value="True"/>
            <t t-set="no_footer" t-value="True"/>

            <div id="wrap" class="landing-page-root oe_structure oe_empty">
                <!-- Inline Early Theme Switcher (Prevents Dark/Light Flash) -->
                <script>
                    try {
                        if (localStorage.getItem('landing_theme') === 'dark') {
                            document.body.classList.add('dark-mode');
                            document.documentElement.setAttribute('data-bs-theme', 'dark');
                            var wrapEl = document.getElementById('wrap');
                            if (wrapEl) wrapEl.classList.add('dark-mode');
                            var wrapwrapEl = document.getElementById('wrapwrap');
                            if (wrapwrapEl) wrapwrapEl.classList.add('dark-mode');
                        }
                    } catch(e) {}
                </script>
                <!-- TOP EDITABLE SNIPPET ZONE -->
                <div class="oe_structure oe_empty" id="oe_structure_landing_top"/>
                
                <!-- TOP ANNOUNCEMENT BAR -->
                <div class="landing-announcement-bar py-2 px-3 text-center text-white small fw-medium">
                    <div class="container-fluid d-flex justify-content-center align-items-center gap-2">
                        <span class="badge bg-warning text-dark px-2 py-1 rounded-pill text-uppercase fw-bold" style="font-size: 0.7rem;">সীমিত সময়ের অফার</span>
                        <span>★ সারা দেশে দ্রুত হোম ডেলিভারি ও ক্যাশ অন ডেলিভারি সুবিধা</span>
                    </div>
                </div>

                <!-- STICKY NAVIGATION HEADER -->
                <header class="landing-header sticky-top">
                    <div class="container">
                        <div class="d-flex align-items-center justify-content-between py-2 py-sm-3 landing-header-inner">
                            <!-- Logo / Brand -->
                            <a href="#hero" class="landing-logo navbar-brand logo d-flex align-items-center text-decoration-none" data-name="Navbar Logo">
                                <span t-field="website.logo" t-options="{'widget': 'image'}" role="img" t-att-aria-label="'Logo of %s' % website.name" t-att-title="website.name" class="landing-logo-img-wrap"/>
                            </a>

                            <!-- Anchor Navigation -->
                            <nav class="d-none d-lg-flex align-items-center gap-4 landing-nav">
                                <a href="#hero" class="nav-link-custom active">হোম</a>
                                <a href="#product-1" class="nav-link-custom">বইসমূহ</a>
                                <a href="#trust-section" class="nav-link-custom">কেন আমরা</a>
                                <a href="#reviews-section" class="nav-link-custom">পাঠক রিভিউ</a>
                                <a href="#faq-section" class="nav-link-custom">প্রশ্নোত্তর</a>
                            </nav>

                            <!-- Actions -->
                            <div class="d-flex align-items-center gap-2 gap-sm-3 landing-header-actions">
                                <button type="button" 
                                        class="btn btn-outline-secondary btn-sm rounded-circle landing-theme-toggle p-0 d-flex align-items-center justify-content-center" 
                                        id="landingThemeToggleBtn"
                                        aria-label="Toggle Light and Dark Mode" 
                                        title="লাইট / ডার্ক মোড পরিবর্তন করুন">
                                    <i class="fa fa-moon-o theme-icon-dark"></i>
                                    <i class="fa fa-sun-o theme-icon-light text-warning"></i>
                                </button>
                                <button type="button" class="btn btn-outline-dark btn-sm rounded-pill px-2 px-sm-3 py-1.5 py-sm-2 d-flex align-items-center gap-2 position-relative text-decoration-none landing-open-cart-checkout" data-bs-toggle="modal" data-bs-target="#landingCartCheckoutModal">
                                    <i class="fa fa-shopping-bag"></i>
                                    <span class="d-none d-sm-inline">কার্ট</span>
                                    <span class="landing-cart-badge badge bg-dark text-white rounded-pill">0</span>
                                </button>
                            </div>
                        </div>
                    </div>
                </header>

                <!-- SECTION 02: HERO SECTION -->
                <section id="hero" class="landing-hero-section pt-4 pt-lg-5 pb-2 pb-lg-3 position-relative overflow-hidden" data-snippet="s_banner">
                    <div class="container pt-lg-2 pb-0 text-center">
                        <div class="landing-hero-badge-wrap mb-3">
                            <span class="badge bg-dark text-white rounded-pill px-3 py-2 fw-bold text-uppercase tracking-wider shadow-sm" style="font-size: 0.78rem;">
                                🎯 জীবন বদলে দেওয়ার ৩টি মাস্টারপিস বইয়ের কালেকশন
                            </span>
                        </div>
                        <h1 class="display-4 fw-bolder text-dark tracking-tight mb-3 mx-auto" style="max-width: 820px; line-height: 1.2;">
                            সফল মানুষের চিন্তাভাবনা, অভ্যাস ও ফোকাস গড়ে তোলার সেরা ৩টি বই
                        </h1>
                        <p class="lead text-muted mx-auto mb-3" style="max-width: 680px; font-size: 1.15rem;">
                            আন্তর্জাতিক সর্বাধিক বিক্রিত ৩টি জীবন পরিবর্তনকারী বই এখন বাংলা ভাষায় প্রিমিয়াম প্রিন্ট ও মজবুত সেলাই বাঁধাইয়ে আপনার দোরগোড়ায়। ক্যাশ অন ডেলিভারিতে চেক করে মূল্য পরিশোধের ১০০% গ্যারান্টি।
                        </p>

                        <!-- Social Trust Elements -->
                        <div class="d-flex justify-content-center align-items-center gap-2 gap-sm-3 mb-2 flex-column flex-sm-row">
                            <div class="d-flex align-items-center gap-1 text-warning">
                                <i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i>
                                <span class="text-dark fw-bold ms-1">৪.৯/৫.০</span>
                            </div>
                            <span class="text-muted d-none d-sm-inline">•</span>
                            <span class="text-muted small fw-medium">১০,০০০+ সন্তুষ্ট পাঠকের ভালোবাসা</span>
                            <span class="text-muted d-none d-sm-inline">•</span>
                            <span class="text-success small fw-semibold"><i class="fa fa-shield me-1"></i>১০০% ক্যাশ অন ডেলিভারি</span>
                        </div>
                    </div>
                </section>

                <!-- DYNAMIC PRODUCT SHOWCASE & CHECKOUT SECTIONS (Card Style Deck) -->
                <div class="landing-products-wrapper">
                    <t t-set="p1" t-value="products[0] if (products and len(products) &gt; 0) else request.env['product.template'].sudo().browse(6)"/>
                    <t t-set="p2" t-value="products[1] if (products and len(products) &gt; 1) else request.env['product.template'].sudo().browse(8)"/>
                    <t t-set="p3" t-value="products[2] if (products and len(products) &gt; 2) else request.env['product.template'].sudo().browse(11)"/>
                    
                    <!-- ==========================================
                         PRODUCT 01: ATOMIC HABITS
                         ========================================== -->
                    <section id="product-1" class="landing-product-section pt-1 pb-4 pt-lg-2 pb-lg-5 position-relative" data-name="বই ০১ Showcase" data-snippet="s_single_product_showcase" data-product-template-id="6" data-product-id="23">
                        <div class="container" style="max-width: 1140px;">
                            <div class="landing-product-card shadow-sm border bg-white rounded-4 rounded-lg-5 p-3 p-sm-4 p-lg-5">
                            
                                <!-- PRODUCT HEADER / PILL BADGE -->
                                <div class="d-flex align-items-center justify-content-between mb-3 mb-sm-4 flex-wrap gap-2">
                                    <div class="d-flex align-items-center gap-2">
                                        <span class="badge bg-dark text-white rounded-pill px-3 py-2 fw-bold text-uppercase" style="font-size: 0.75rem;">
                                            বই ০১
                                        </span>
                                        <span class="badge bg-primary-subtle text-primary border border-primary-subtle rounded-pill px-3 py-2 fw-semibold">
                                            আন্তর্জাতিক বেস্টসেলার • অভ্যাস পরিবর্তনের সহজ উপায়
                                        </span>
                                    </div>
                                    <div class="d-flex align-items-center gap-2 small text-muted">
                                        <div class="text-warning">
                                            <i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i>
                                        </div>
                                        <span class="fw-bold text-dark">4.9</span>
                                        <span>(১৮৪০+ রিভিউ)</span>
                                    </div>
                                </div>

                                <!-- 2-COLUMN DESKTOP LAYOUT -->
                                <div class="row g-4 g-lg-5 align-items-start">
                                
                                    <!-- LEFT COLUMN: PRODUCT IMAGES -->
                                    <div class="col-12 col-lg-6 landing-slide-left">
                                        <div class="landing-gallery-sticky">
                                            <div class="landing-main-image-container rounded-4 overflow-hidden border bg-white shadow-sm position-relative mb-3">
                                                <img id="main-image-1" 
                                                     src="/theme_multiproduct_landing/static/src/img/book_atomic_habits.jpg" 
                                                     alt="Atomic Habits (অ্যাটোমিক হ্যাবিটস)" 
                                                     class="img-fluid w-100 landing-main-img snippet-display-img" 
                                                     style="max-height: 520px; object-fit: contain; padding: 24px; transition: transform 0.4s ease;"/>
                                                <span class="position-absolute top-0 start-0 m-3 badge bg-white text-dark border shadow-sm px-3 py-2 rounded-pill fw-semibold">
                                                    <i class="fa fa-check text-success me-1"></i> স্টকে আছে • দ্রুত ডেলিভারি
                                                </span>
                                            </div>

                                            <!-- Thumbnails Strip -->
                                            <div class="d-flex gap-2 landing-thumbnails-row">
                                                <button type="button" class="btn p-0 border rounded-3 overflow-hidden landing-thumb-btn active" data-target="main-image-1" data-src="/theme_multiproduct_landing/static/src/img/book_atomic_habits.jpg" style="width: 72px; height: 72px;">
                                                    <img src="/theme_multiproduct_landing/static/src/img/book_atomic_habits.jpg" alt="Atomic Habits Cover" class="w-100 h-100 object-fit-cover"/>
                                                </button>
                                            </div>
                                        </div>
                                    </div>

                                    <!-- RIGHT COLUMN: PRODUCT INFORMATION -->
                                    <div class="col-12 col-lg-6 landing-slide-right">
                                        <div class="landing-product-info ps-lg-3">
                                            <h2 class="display-6 fw-bolder text-dark mb-2 snippet-display-title">Atomic Habits (অ্যাটোমিক হ্যাবিটস)</h2>
                                            
                                            <p class="text-primary fw-semibold fs-5 mb-3 snippet-display-tagline">দৈনন্দিন অভ্যাস বদলে দেওয়ার এক অনন্য ও বৈজ্ঞানিক উপায়</p>

                                            <!-- Pricing Block -->
                                            <div class="d-flex align-items-baseline gap-3 mb-4">
                                                <span class="display-6 fw-bold text-dark">
                                                    ৳<span id="display-price-1" class="snippet-display-price">350.00</span>
                                                </span>
                                                <span class="text-muted text-decoration-line-through fs-5">
                                                    ৳500.00
                                                </span>
                                                <span class="badge bg-danger-subtle text-danger px-3 py-2 rounded-pill fw-bold">
                                                    সাশ্রয় ৳১৫০
                                                </span>
                                            </div>

                                            <!-- Description -->
                                            <div class="text-muted mb-4 fs-6 leading-relaxed snippet-display-desc">
                                                বিশ্বখ্যাত আচরণবিজ্ঞান বিশেষজ্ঞ জেমস ক্লিয়ারের সর্বাধিক বিক্রিত বই। প্রতিদিন মাত্র ১% পরিবর্তনের মাধ্যমে কীভাবে দীর্ঘস্থায়ী সুঅভ্যাস গড়ে তুলবেন এবং খারাপ অভ্যাস দূর করবেন—তার বৈজ্ঞানিক ও ব্যবহারিক গাইডলাইন।
                                            </div>

                                            <!-- Key Benefits Checklist -->
                                            <div class="landing-benefits-box mb-4">
                                                <h6 class="text-uppercase fw-bold text-dark small tracking-wider mb-3">বইটির মূল বিষয় ও উপকারিতা</h6>
                                                <div class="row g-2">
                                                    <t t-if="p1 and p1.get_landing_benefits_list()">
                                                        <t t-foreach="p1.get_landing_benefits_list()" t-as="benefit">
                                                            <div class="col-12 col-sm-6">
                                                                <div class="d-flex align-items-center gap-2 small text-dark">
                                                                    <i class="fa fa-check-circle text-success fs-6"></i>
                                                                    <span t-esc="benefit"/>
                                                                </div>
                                                            </div>
                                                        </t>
                                                    </t>
                                                    <t t-else="">
                                                        <div class="col-12 col-sm-6">
                                                            <div class="d-flex align-items-center gap-2 small text-dark">
                                                                <i class="fa fa-check-circle text-success fs-6"></i>
                                                                <span>চার স্তরের প্রমাণিত অভ্যাস কাঠামো (সংকেত, আকাঙ্ক্ষা, প্রতিক্রিয়া ও পুরস্কার)</span>
                                                            </div>
                                                        </div>
                                                        <div class="col-12 col-sm-6">
                                                            <div class="d-flex align-items-center gap-2 small text-dark">
                                                                <i class="fa fa-check-circle text-success fs-6"></i>
                                                                <span>খারাপ অভ্যাস চিরতরে বর্জনের সহজ মনস্তাত্ত্বিক পদ্ধতি</span>
                                                            </div>
                                                        </div>
                                                        <div class="col-12 col-sm-6">
                                                            <div class="d-flex align-items-center gap-2 small text-dark">
                                                                <i class="fa fa-check-circle text-success fs-6"></i>
                                                                <span>প্রতিদিন মাত্র ১% ইতিবাচক পরিবর্তনের মাধ্যমে অভূতপূর্ব সাফল্য</span>
                                                            </div>
                                                        </div>
                                                        <div class="col-12 col-sm-6">
                                                            <div class="d-flex align-items-center gap-2 small text-dark">
                                                                <i class="fa fa-check-circle text-success fs-6"></i>
                                                                <span>৮০ জিএসএম আই-ফ্রেন্ডলি সুইডিশ ক্রিম পেপার ও স্পষ্ট বড় ফন্ট</span>
                                                            </div>
                                                        </div>
                                                    </t>
                                                </div>
                                            </div>

                                            <!-- Technical Specifications Table -->
                                            <div class="landing-specs-box mb-4 p-3 bg-white rounded-3 border" t-if="p1 and p1.get_landing_specs_list()">
                                                <h6 class="text-uppercase fw-bold text-dark small tracking-wider mb-2">বইয়ের বিবরণ ও স্পেসিফিকেশন</h6>
                                                <div class="table-responsive rounded-2 border overflow-hidden">
                                                    <table class="table table-sm table-bordered mb-0 small align-middle">
                                                        <tbody>
                                                            <t t-foreach="p1.get_landing_specs_list()" t-as="spec">
                                                                <t t-if="spec.get('value') and spec.get('value').strip()">
                                                                    <tr>
                                                                        <td class="text-secondary fw-bold py-2 px-3 bg-light" style="width: 35%;" t-esc="spec['label']"/>
                                                                        <td class="text-dark fw-medium py-2 px-3" t-esc="spec['value']"/>
                                                                    </tr>
                                                                </t>
                                                            </t>
                                                        </tbody>
                                                    </table>
                                                </div>
                                            </div>

                                            <!-- Buy Now Action (Triggers Checkout Popup Modal) -->
                                            <div class="landing-action-box pt-2">
                                                <button type="button" 
                                                        class="btn btn-outline-dark btn-lg w-100 rounded-pill py-3 fw-bold shadow-sm d-flex align-items-center justify-content-center gap-2 mb-3 landing-add-to-cart-btn"
                                                        data-product-index="1"
                                                        data-product-template-id="6"
                                                        data-product-id="23">
                                                    <i class="fa fa-shopping-bag me-1"></i>
                                                    <span class="btn-text">কার্টে যোগ করুন</span>
                                                    <div class="spinner-border spinner-border-sm d-none" role="status"></div>
                                                </button>
                                                <button type="button" 
                                                        class="btn btn-dark btn-lg w-100 rounded-pill py-3 fw-bold shadow-sm d-flex align-items-center justify-content-center gap-2 landing-buy-now-trigger" 
                                                        data-bs-toggle="modal" 
                                                        data-bs-target="#product-1-checkout">
                                                    <i class="fa fa-book me-1"></i>
                                                    <span>বইটি অর্ডার করুন</span>
                                                    <i class="fa fa-arrow-right small ms-1"></i>
                                                </button>
                                                <div class="text-center text-muted small mt-2">
                                                    <i class="fa fa-truck me-1 text-primary"></i> সারা দেশে ক্যাশ অন ডেলিভারি ও ফ্রি হোম ডেলিভারি
                                                </div>
                                            </div>

                                        </div>
                                    </div>
                                </div>

                            </div>
                        </div>
                    </section>

                    <!-- EDITABLE DROPZONE BETWEEN PRODUCT 1 AND 2 -->
                    <div class="oe_structure oe_empty" id="oe_structure_landing_after_p1"/>

                    <!-- POPUP CHECKOUT MODAL FOR PRODUCT 01 -->
                    <div id="product-1-checkout" class="modal fade landing-checkout-modal" tabindex="-1" aria-labelledby="checkoutModalLabel-1" aria-hidden="true" data-bs-backdrop="static">
                        <div class="modal-dialog modal-dialog-centered modal-lg modal-dialog-scrollable">
                            <div class="modal-content rounded-4 border-0 shadow-lg overflow-hidden">
                                
                                <!-- Modal Header -->
                                <div class="modal-header bg-dark text-white p-3 p-lg-4 border-0">
                                    <div class="d-flex align-items-center justify-content-between w-100 me-2">
                                        <div class="d-flex align-items-center gap-3">
                                            <div class="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center flex-shrink-0" style="width: 40px; height: 40px; font-size: 1.1rem;">
                                                <i class="fa fa-shopping-bag"></i>
                                            </div>
                                            <div>
                                                <h5 class="modal-title fw-bold mb-0 text-white" id="checkoutModalLabel-1">
                                                    অর্ডার সম্পন্ন করুন
                                                </h5>
                                                <p class="text-white-50 small mb-0">ক্যাশ অন ডেলিভারিতে অর্ডার সম্পন্ন করতে নিচের তথ্যগুলো পূরণ করুন</p>
                                            </div>
                                        </div>
                                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                                    </div>
                                </div>

                                <!-- Order Form -->
                                <form id="checkout-form-1" class="landing-checkout-form" data-product-index="1">
                                    <input type="hidden" name="csrf_token" t-att-value="request.csrf_token()"/>
                                    
                                    <div class="modal-body p-3 p-lg-4 bg-light">
                                        <div class="row g-4">
                                            
                                            <!-- LEFT COLUMN: CUSTOMER DETAILS -->
                                            <div class="col-12 col-lg-7">
                                                <h6 class="fw-bold text-dark mb-3 d-flex align-items-center gap-2">
                                                    <span class="badge bg-dark rounded-circle" style="width: 24px; height: 24px; font-size: 0.75rem; display: inline-flex; align-items: center; justify-content: center;">1</span>
                                                    <span>আপনার ডেলিভারি তথ্য প্রদান করুন</span>
                                                </h6>

                                                <!-- Full Name -->
                                                <div class="mb-3">
                                                    <label class="form-label small fw-semibold text-dark">নাম <span class="text-danger">*</span></label>
                                                    <div class="input-group">
                                                        <span class="input-group-text bg-white border-end-0 text-muted"><i class="fa fa-user"></i></span>
                                                        <input type="text" name="name" class="form-control border-start-0" placeholder="আপনার নাম লিখুন" required="required"/>
                                                    </div>
                                                </div>

                                                <!-- Mobile Phone -->
                                                <div class="mb-3">
                                                    <label class="form-label small fw-semibold text-dark">মোবাইল নম্বর <span class="text-danger">*</span></label>
                                                    <div class="input-group">
                                                        <span class="input-group-text bg-white border-end-0 text-muted"><i class="fa fa-phone"></i></span>
                                                        <input type="tel" name="phone" class="form-control border-start-0" placeholder="01XXXXXXXXX" required="required"/>
                                                    </div>
                                                    <div class="form-text small">ডেলিভারির সময় এই নম্বরে কল করা হবে।</div>
                                                </div>

                                                <!-- Full Delivery Address -->
                                                <div class="mb-3">
                                                    <label class="form-label small fw-semibold text-dark">সম্পূর্ণ ডেলিভারি ঠিকানা <span class="text-danger">*</span></label>
                                                    <div class="input-group">
                                                        <span class="input-group-text bg-white border-end-0 text-muted"><i class="fa fa-map-marker"></i></span>
                                                        <textarea name="street" rows="2" class="form-control border-start-0" placeholder="বাসা/রোড নম্বর, এলাকা, থানা ও জেলা উল্লেখ করুন" required="required"></textarea>
                                                    </div>
                                                </div>
                                                <input type="hidden" name="city" value="Dhaka"/>

                                                <!-- Delivery Carrier Option -->
                                                <div class="mb-3">
                                                    <label class="form-label small fw-semibold text-dark">ডেলিভারি এরিয়া নির্বাচন করুন <span class="text-danger">*</span></label>
                                                    <div class="d-flex flex-column gap-2">
                                                        <label class="p-2.5 bg-white rounded-3 border border-primary d-flex align-items-center justify-content-between cursor-pointer landing-carrier-option" style="cursor: pointer;">
                                                            <div class="form-check d-flex align-items-center gap-2 mb-0">
                                                                <input class="form-check-input landing-carrier-radio" type="radio" name="carrier_id" value="1" checked="checked" data-price="60.0" data-product-index="1" id="carrier_1_inside_1"/>
                                                                <span class="form-check-label fw-semibold text-dark small" for="carrier_1_inside_1">ঢাকার ভেতরে</span>
                                                            </div>
                                                            <span class="badge bg-primary text-white fw-bold small px-2.5 py-1.5 rounded-pill">৳60</span>
                                                        </label>
                                                        <label class="p-2.5 bg-white rounded-3 border d-flex align-items-center justify-content-between cursor-pointer landing-carrier-option" style="cursor: pointer;">
                                                            <div class="form-check d-flex align-items-center gap-2 mb-0">
                                                                <input class="form-check-input landing-carrier-radio" type="radio" name="carrier_id" value="2" data-price="120.0" data-product-index="1" id="carrier_2_outside_1"/>
                                                                <span class="form-check-label fw-semibold text-dark small" for="carrier_2_outside_1">ঢাকার বাইরে</span>
                                                            </div>
                                                            <span class="badge bg-secondary-subtle text-dark border fw-bold small px-2.5 py-1.5 rounded-pill">৳120</span>
                                                        </label>
                                                    </div>
                                                </div>

                                                <!-- পেমেন্ট পদ্ধতি Section -->
                                                <h6 class="fw-bold text-dark mt-3 mb-2 d-flex align-items-center gap-2">
                                                    <span class="badge bg-dark rounded-circle" style="width: 24px; height: 24px; font-size: 0.75rem; display: inline-flex; align-items: center; justify-content: center;">2</span>
                                                    <span>পেমেন্ট পদ্ধতি</span>
                                                </h6>
                                                <div class="p-3 bg-white rounded-3 border d-flex align-items-center justify-content-between">
                                                    <div class="form-check d-flex align-items-center gap-2 mb-0">
                                                        <input class="form-check-input" type="radio" name="payment_method_1" value="cod" checked="checked" id="codOption-1"/>
                                                        <label class="form-check-label fw-bold text-dark" for="codOption-1">
                                                            ক্যাশ অন ডেলিভারি (পণ্য হাতে পেয়ে মূল্য পরিশোধ)
                                                        </label>
                                                    </div>
                                                    <span class="badge bg-success-subtle text-success border border-success-subtle rounded-pill px-3 py-1 fw-semibold small">
                                                        <i class="fa fa-shield me-1"></i> ক্যাশ অন ডেলিভারি
                                                    </span>
                                                </div>
                                            </div>

                                            <!-- RIGHT COLUMN: ORDER SUMMARY -->
                                            <div class="col-12 col-lg-5">
                                                <div class="bg-white p-3 rounded-4 border shadow-sm">
                                                    <h6 class="fw-bold text-dark mb-3">অর্ডারের সারসংক্ষেপ</h6>

                                                    <!-- Product Summary Card -->
                                                    <div class="d-flex align-items-center gap-3 p-3 bg-light rounded-3 border mb-3">
                                                        <div class="rounded-2 overflow-hidden border bg-white" style="width: 56px; height: 56px; flex-shrink: 0;">
                                                            <img src="/theme_multiproduct_landing/static/src/img/book_atomic_habits.jpg" alt="Atomic Habits" class="w-100 h-100 object-fit-cover"/>
                                                        </div>
                                                        <div class="flex-grow-1 overflow-hidden">
                                                            <div class="fw-bold text-dark text-truncate small">Atomic Habits (অ্যাটোমিক হ্যাবিটস)</div>
                                                            <span id="summary-variant-name-1" class="d-none">Atomic Habits</span>
                                                            <div class="fw-bold text-primary small mt-1">
                                                                ৳<span id="summary-unit-price-1" data-price="350.00">350.00</span>
                                                            </div>
                                                        </div>
                                                    </div>

                                                    <!-- Hidden Product ID -->
                                                    <input type="hidden" name="product_id" id="input-product-id-1" value="23"/>

                                                    <!-- Quantity Adjuster with Prominent Buttons -->
                                                    <div class="d-flex justify-content-between align-items-center mb-3 p-2 bg-light rounded-3 border">
                                                        <span class="fw-bold text-dark small ps-2">পরিমাণ</span>
                                                        <div class="d-flex align-items-center gap-2">
                                                            <button type="button" class="btn btn-dark btn-sm landing-qty-btn rounded-circle d-flex align-items-center justify-content-center" data-product-index="1" data-action="minus" style="width: 32px; height: 32px; font-size: 1.1rem; line-height: 1; padding: 0;">-</button>
                                                            <input type="number" name="quantity" id="input-qty-1" value="1" min="1" max="99" class="form-control text-center fw-bold landing-qty-input border-0 py-0 bg-transparent fs-6" style="width: 48px;" data-product-index="1"/>
                                                            <button type="button" class="btn btn-dark btn-sm landing-qty-btn rounded-circle d-flex align-items-center justify-content-center" data-product-index="1" data-action="plus" style="width: 32px; height: 32px; font-size: 1.1rem; line-height: 1; padding: 0;">+</button>
                                                        </div>
                                                    </div>

                                                    <!-- Live Cost Breakdown -->
                                                    <div class="landing-cost-breakdown pt-2 border-top">
                                                        <div class="d-flex justify-content-between align-items-center mb-2 small text-muted">
                                                            <span>বইয়ের মূল্য</span>
                                                            <span class="text-dark fw-semibold">
                                                                ৳<span id="calc-subtotal-1">350.00</span>
                                                            </span>
                                                        </div>
                                                        <div class="d-flex justify-content-between align-items-center mb-2 small text-muted">
                                                            <span>ডেলিভারি চার্জ</span>
                                                            <span class="text-primary fw-semibold">৳<span id="calc-shipping-1">60.00</span></span>
                                                        </div>
                                                        <div class="d-flex justify-content-between align-items-center pt-2 border-top fs-5 fw-bold text-dark">
                                                            <span>সর্বমোট মূল্য</span>
                                                            <span class="text-primary">
                                                                ৳<span id="calc-total-1">410.00</span>
                                                            </span>
                                                        </div>
                                                    </div>

                                                </div>
                                            </div>

                                        </div>
                                    </div>

                                    <!-- ALWAYS-VISIBLE MODAL FOOTER -->
                                    <div class="modal-footer bg-white border-top p-2.5 p-sm-3 d-flex flex-row justify-content-between align-items-center gap-2 gap-sm-3">
                                        <div class="d-flex flex-column align-items-start">
                                            <span class="text-muted small fw-medium" style="font-size: 0.72rem; line-height: 1.1;">সর্বমোট প্রদেয়:</span>
                                            <span class="fs-5 fs-sm-4 fw-bolder text-primary lh-1">
                                                ৳<span id="calc-total-footer-1">410.00</span>
                                            </span>
                                        </div>
                                        <button type="submit" id="submit-btn-1" class="btn btn-dark btn-md px-3 px-sm-4 py-2.5 py-sm-3 rounded-pill fw-bold shadow landing-submit-order-btn d-flex align-items-center justify-content-center gap-2 flex-grow-1 flex-sm-grow-0" style="max-width: 260px;">
                                            <i class="fa fa-check-circle"></i>
                                            <span class="btn-text">অর্ডার কনফার্ম করুন</span>
                                            <div class="spinner-border spinner-border-sm d-none" role="status"></div>
                                        </button>
                                    </div>

                                </form>

                            </div>
                        </div>
                    </div>

                    <!-- ==========================================
                         PRODUCT 02: THE PSYCHOLOGY OF MONEY
                         ========================================== -->
                    <section id="product-2" class="landing-product-section py-3 py-lg-5 position-relative" data-name="বই ০২ Showcase" data-snippet="s_single_product_showcase" data-product-template-id="8" data-product-id="24">
                        <div class="container" style="max-width: 1140px;">
                            <div class="landing-product-card shadow-sm border bg-white rounded-4 rounded-lg-5 p-3 p-sm-4 p-lg-5">
                            
                                <!-- PRODUCT HEADER / PILL BADGE -->
                                <div class="d-flex align-items-center justify-content-between mb-3 mb-sm-4 flex-wrap gap-2">
                                    <div class="d-flex align-items-center gap-2">
                                        <span class="badge bg-dark text-white rounded-pill px-3 py-2 fw-bold text-uppercase" style="font-size: 0.75rem;">
                                            বই ০২
                                        </span>
                                        <span class="badge bg-primary-subtle text-primary border border-primary-subtle rounded-pill px-3 py-2 fw-semibold">
                                            WALL STREET JOURNAL BESTSELLER • অর্থ ও সম্পদের সঠিক ব্যবহার
                                        </span>
                                    </div>
                                    <div class="d-flex align-items-center gap-2 small text-muted">
                                        <div class="text-warning">
                                            <i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i>
                                        </div>
                                        <span class="fw-bold text-dark">4.8</span>
                                        <span>(১৪২০+ রিভিউ)</span>
                                    </div>
                                </div>

                                <!-- 2-COLUMN DESKTOP LAYOUT -->
                                <div class="row g-4 g-lg-5 align-items-start">
                                
                                    <!-- LEFT COLUMN: PRODUCT IMAGES -->
                                    <div class="col-12 col-lg-6 landing-slide-left">
                                        <div class="landing-gallery-sticky">
                                            <div class="landing-main-image-container rounded-4 overflow-hidden border bg-white shadow-sm position-relative mb-3">
                                                <img id="main-image-2" 
                                                     src="/theme_multiproduct_landing/static/src/img/book_psychology_money.jpg" 
                                                     alt="The Psychology of Money (সাইকোলজি অব মানি)" 
                                                     class="img-fluid w-100 landing-main-img snippet-display-img" 
                                                     style="max-height: 520px; object-fit: contain; padding: 24px; transition: transform 0.4s ease;"/>
                                                <span class="position-absolute top-0 start-0 m-3 badge bg-white text-dark border shadow-sm px-3 py-2 rounded-pill fw-semibold">
                                                    <i class="fa fa-check text-success me-1"></i> স্টকে আছে • দ্রুত ডেলিভারি
                                                </span>
                                            </div>

                                            <!-- Thumbnails Strip -->
                                            <div class="d-flex gap-2 landing-thumbnails-row">
                                                <button type="button" class="btn p-0 border rounded-3 overflow-hidden landing-thumb-btn active" data-target="main-image-2" data-src="/theme_multiproduct_landing/static/src/img/book_psychology_money.jpg" style="width: 72px; height: 72px;">
                                                    <img src="/theme_multiproduct_landing/static/src/img/book_psychology_money.jpg" alt="Psychology of Money Cover" class="w-100 h-100 object-fit-cover"/>
                                                </button>
                                            </div>
                                        </div>
                                    </div>

                                    <!-- RIGHT COLUMN: PRODUCT INFORMATION -->
                                    <div class="col-12 col-lg-6 landing-slide-right">
                                        <div class="landing-product-info ps-lg-3">
                                            <h2 class="display-6 fw-bolder text-dark mb-2 snippet-display-title">The Psychology of Money (সাইকোলজি অব মানি)</h2>
                                            
                                            <p class="text-primary fw-semibold fs-5 mb-3 snippet-display-tagline">অর্থ, সম্পদ এবং সুখ নিয়ে অনন্য ১৯টি পাঠ</p>

                                            <!-- Pricing Block -->
                                            <div class="d-flex align-items-baseline gap-3 mb-4">
                                                <span class="display-6 fw-bold text-dark">
                                                    ৳<span id="display-price-2" class="snippet-display-price">320.00</span>
                                                </span>
                                                <span class="text-muted text-decoration-line-through fs-5">
                                                    ৳480.00
                                                </span>
                                                <span class="badge bg-danger-subtle text-danger px-3 py-2 rounded-pill fw-bold">
                                                    Save ৳160.00
                                                </span>
                                            </div>

                                            <!-- Description -->
                                            <div class="text-muted mb-4 fs-6 leading-relaxed snippet-display-desc">
                                                মরগান হাউজেলের সর্বকালের অন্যতম জনপ্রিয় ফিনান্সিয়াল বই। কীভাবে মানুষ অর্থ নিয়ে ভাবে, কেন স্মার্ট মানুষেরাও আর্থিক ভুল করে এবং সম্পদ কীভাবে দীর্ঘমেয়াদে ধরে রাখতে হয় তার ব্যবহারিক ও মনস্তাত্ত্বিক রূপরেখা।
                                            </div>

                                            <!-- Key Benefits Checklist -->
                                            <div class="landing-benefits-box mb-4">
                                                <h6 class="text-uppercase fw-bold text-dark small tracking-wider mb-3">বইটির মূল বিষয় ও উপকারিতা</h6>
                                                <div class="row g-2">
                                                    <t t-if="p2 and p2.get_landing_benefits_list()">
                                                        <t t-foreach="p2.get_landing_benefits_list()" t-as="benefit">
                                                            <div class="col-12 col-sm-6">
                                                                <div class="d-flex align-items-center gap-2 small text-dark">
                                                                    <i class="fa fa-check-circle text-success fs-6"></i>
                                                                    <span t-esc="benefit"/>
                                                                </div>
                                                            </div>
                                                        </t>
                                                    </t>
                                                    <t t-else="">
                                                        <div class="col-12 col-sm-6">
                                                            <div class="d-flex align-items-center gap-2 small text-dark">
                                                                <i class="fa fa-check-circle text-success fs-6"></i>
                                                                <span>অর্থ ও বিনিয়োগের মনস্তাত্ত্বিক দিকগুলোর গভীর বিশ্লেষণ</span>
                                                            </div>
                                                        </div>
                                                        <div class="col-12 col-sm-6">
                                                            <div class="d-flex align-items-center gap-2 small text-dark">
                                                                <i class="fa fa-check-circle text-success fs-6"></i>
                                                                <span>ধনী হওয়া বনাম সম্পদ ধরে রাখার পার্থক্য অনুধাবন</span>
                                                            </div>
                                                        </div>
                                                        <div class="col-12 col-sm-6">
                                                            <div class="d-flex align-items-center gap-2 small text-dark">
                                                                <i class="fa fa-check-circle text-success fs-6"></i>
                                                                <span>আর্থিক স্বাধীনতা অর্জনের বাস্তবসম্মত ১৯টি পাঠ</span>
                                                            </div>
                                                        </div>
                                                        <div class="col-12 col-sm-6">
                                                            <div class="d-flex align-items-center gap-2 small text-dark">
                                                                <i class="fa fa-check-circle text-success fs-6"></i>
                                                                <span>৮০ জিএসএম প্রিমিয়াম সুইডিশ ক্রিম পেপার ও দৃষ্টিনন্দন বাঁধাই</span>
                                                            </div>
                                                        </div>
                                                    </t>
                                                </div>
                                            </div>

                                            <!-- Technical Specifications Table -->
                                            <div class="landing-specs-box mb-4 p-3 bg-white rounded-3 border" t-if="p2 and p2.get_landing_specs_list()">
                                                <h6 class="text-uppercase fw-bold text-dark small tracking-wider mb-2">বইয়ের বিবরণ ও স্পেসিফিকেশন</h6>
                                                <div class="table-responsive rounded-2 border overflow-hidden">
                                                    <table class="table table-sm table-bordered mb-0 small align-middle">
                                                        <tbody>
                                                            <t t-foreach="p2.get_landing_specs_list()" t-as="spec">
                                                                <t t-if="spec.get('value') and spec.get('value').strip()">
                                                                    <tr>
                                                                        <td class="text-secondary fw-bold py-2 px-3 bg-light" style="width: 35%;" t-esc="spec['label']"/>
                                                                        <td class="text-dark fw-medium py-2 px-3" t-esc="spec['value']"/>
                                                                    </tr>
                                                                </t>
                                                            </t>
                                                        </tbody>
                                                    </table>
                                                </div>
                                            </div>

                                            <!-- Buy Now Action (Triggers Checkout Popup Modal) -->
                                            <div class="landing-action-box pt-2">
                                                <button type="button" 
                                                        class="btn btn-outline-dark btn-lg w-100 rounded-pill py-3 fw-bold shadow-sm d-flex align-items-center justify-content-center gap-2 mb-3 landing-add-to-cart-btn"
                                                        data-product-index="2"
                                                        data-product-template-id="8"
                                                        data-product-id="24">
                                                    <i class="fa fa-shopping-bag me-1"></i>
                                                    <span class="btn-text">কার্টে যোগ করুন</span>
                                                    <div class="spinner-border spinner-border-sm d-none" role="status"></div>
                                                </button>
                                                <button type="button" 
                                                        class="btn btn-dark btn-lg w-100 rounded-pill py-3 fw-bold shadow-sm d-flex align-items-center justify-content-center gap-2 landing-buy-now-trigger" 
                                                        data-bs-toggle="modal" 
                                                        data-bs-target="#product-2-checkout">
                                                    <i class="fa fa-book me-1"></i>
                                                    <span>বইটি অর্ডার করুন</span>
                                                    <i class="fa fa-arrow-right small ms-1"></i>
                                                </button>
                                                <div class="text-center text-muted small mt-2">
                                                    <i class="fa fa-truck me-1 text-primary"></i> সারা দেশে ক্যাশ অন ডেলিভারি ও ফ্রি হোম ডেলিভারি
                                                </div>
                                            </div>

                                        </div>
                                    </div>
                                </div>

                            </div>
                        </div>
                    </section>

                    <!-- EDITABLE DROPZONE BETWEEN PRODUCT 2 AND 3 -->
                    <div class="oe_structure oe_empty" id="oe_structure_landing_after_p2"/>

                    <!-- POPUP CHECKOUT MODAL FOR PRODUCT 02 -->
                    <div id="product-2-checkout" class="modal fade landing-checkout-modal" tabindex="-1" aria-labelledby="checkoutModalLabel-2" aria-hidden="true" data-bs-backdrop="static">
                        <div class="modal-dialog modal-dialog-centered modal-lg modal-dialog-scrollable">
                            <div class="modal-content rounded-4 border-0 shadow-lg overflow-hidden">
                                
                                <!-- Modal Header -->
                                <div class="modal-header bg-dark text-white p-3 p-lg-4 border-0">
                                    <div class="d-flex align-items-center justify-content-between w-100 me-2">
                                        <div class="d-flex align-items-center gap-3">
                                            <div class="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center flex-shrink-0" style="width: 40px; height: 40px; font-size: 1.1rem;">
                                                <i class="fa fa-shopping-bag"></i>
                                            </div>
                                            <div>
                                                <h5 class="modal-title fw-bold mb-0 text-white" id="checkoutModalLabel-2">
                                                    অর্ডার সম্পন্ন করুন
                                                </h5>
                                                <p class="text-white-50 small mb-0">ক্যাশ অন ডেলিভারিতে অর্ডার সম্পন্ন করতে নিচের তথ্যগুলো পূরণ করুন</p>
                                            </div>
                                        </div>
                                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                                    </div>
                                </div>

                                <!-- Order Form -->
                                <form id="checkout-form-2" class="landing-checkout-form" data-product-index="2">
                                    <input type="hidden" name="csrf_token" t-att-value="request.csrf_token()"/>
                                    
                                    <div class="modal-body p-3 p-lg-4 bg-light">
                                        <div class="row g-4">
                                            
                                            <!-- LEFT COLUMN: CUSTOMER DETAILS -->
                                            <div class="col-12 col-lg-7">
                                                <h6 class="fw-bold text-dark mb-3 d-flex align-items-center gap-2">
                                                    <span class="badge bg-dark rounded-circle" style="width: 24px; height: 24px; font-size: 0.75rem; display: inline-flex; align-items: center; justify-content: center;">1</span>
                                                    <span>আপনার ডেলিভারি তথ্য প্রদান করুন</span>
                                                </h6>

                                                <!-- Full Name -->
                                                <div class="mb-3">
                                                    <label class="form-label small fw-semibold text-dark">নাম <span class="text-danger">*</span></label>
                                                    <div class="input-group">
                                                        <span class="input-group-text bg-white border-end-0 text-muted"><i class="fa fa-user"></i></span>
                                                        <input type="text" name="name" class="form-control border-start-0" placeholder="আপনার নাম লিখুন" required="required"/>
                                                    </div>
                                                </div>

                                                <!-- Mobile Phone -->
                                                <div class="mb-3">
                                                    <label class="form-label small fw-semibold text-dark">মোবাইল নম্বর <span class="text-danger">*</span></label>
                                                    <div class="input-group">
                                                        <span class="input-group-text bg-white border-end-0 text-muted"><i class="fa fa-phone"></i></span>
                                                        <input type="tel" name="phone" class="form-control border-start-0" placeholder="01XXXXXXXXX" required="required"/>
                                                    </div>
                                                    <div class="form-text small">ডেলিভারির সময় এই নম্বরে কল করা হবে।</div>
                                                </div>

                                                <!-- Full Delivery Address -->
                                                <div class="mb-3">
                                                    <label class="form-label small fw-semibold text-dark">সম্পূর্ণ ডেলিভারি ঠিকানা <span class="text-danger">*</span></label>
                                                    <div class="input-group">
                                                        <span class="input-group-text bg-white border-end-0 text-muted"><i class="fa fa-map-marker"></i></span>
                                                        <textarea name="street" rows="2" class="form-control border-start-0" placeholder="বাসা/রোড নম্বর, এলাকা, থানা ও জেলা উল্লেখ করুন" required="required"></textarea>
                                                    </div>
                                                </div>
                                                <input type="hidden" name="city" value="Dhaka"/>

                                                <!-- Delivery Carrier Option -->
                                                <div class="mb-3">
                                                    <label class="form-label small fw-semibold text-dark">ডেলিভারি এরিয়া নির্বাচন করুন <span class="text-danger">*</span></label>
                                                    <div class="d-flex flex-column gap-2">
                                                        <label class="p-2.5 bg-white rounded-3 border border-primary d-flex align-items-center justify-content-between cursor-pointer landing-carrier-option" style="cursor: pointer;">
                                                            <div class="form-check d-flex align-items-center gap-2 mb-0">
                                                                <input class="form-check-input landing-carrier-radio" type="radio" name="carrier_id" value="1" checked="checked" data-price="60.0" data-product-index="2" id="carrier_1_inside_2"/>
                                                                <span class="form-check-label fw-semibold text-dark small" for="carrier_1_inside_2">ঢাকার ভেতরে</span>
                                                            </div>
                                                            <span class="badge bg-primary text-white fw-bold small px-2.5 py-1.5 rounded-pill">৳60</span>
                                                        </label>
                                                        <label class="p-2.5 bg-white rounded-3 border d-flex align-items-center justify-content-between cursor-pointer landing-carrier-option" style="cursor: pointer;">
                                                            <div class="form-check d-flex align-items-center gap-2 mb-0">
                                                                <input class="form-check-input landing-carrier-radio" type="radio" name="carrier_id" value="2" data-price="120.0" data-product-index="2" id="carrier_2_outside_2"/>
                                                                <span class="form-check-label fw-semibold text-dark small" for="carrier_2_outside_2">ঢাকার বাইরে</span>
                                                            </div>
                                                            <span class="badge bg-secondary-subtle text-dark border fw-bold small px-2.5 py-1.5 rounded-pill">৳120</span>
                                                        </label>
                                                    </div>
                                                </div>

                                                <!-- পেমেন্ট পদ্ধতি Section -->
                                                <h6 class="fw-bold text-dark mt-3 mb-2 d-flex align-items-center gap-2">
                                                    <span class="badge bg-dark rounded-circle" style="width: 24px; height: 24px; font-size: 0.75rem; display: inline-flex; align-items: center; justify-content: center;">2</span>
                                                    <span>পেমেন্ট পদ্ধতি</span>
                                                </h6>
                                                <div class="p-3 bg-white rounded-3 border d-flex align-items-center justify-content-between">
                                                    <div class="form-check d-flex align-items-center gap-2 mb-0">
                                                        <input class="form-check-input" type="radio" name="payment_method_2" value="cod" checked="checked" id="codOption-2"/>
                                                        <label class="form-check-label fw-bold text-dark" for="codOption-2">
                                                            ক্যাশ অন ডেলিভারি (পণ্য হাতে পেয়ে মূল্য পরিশোধ)
                                                        </label>
                                                    </div>
                                                    <span class="badge bg-success-subtle text-success border border-success-subtle rounded-pill px-3 py-1 fw-semibold small">
                                                        <i class="fa fa-shield me-1"></i> ক্যাশ অন ডেলিভারি
                                                    </span>
                                                </div>
                                            </div>

                                            <!-- RIGHT COLUMN: ORDER SUMMARY -->
                                            <div class="col-12 col-lg-5">
                                                <div class="bg-white p-3 rounded-4 border shadow-sm">
                                                    <h6 class="fw-bold text-dark mb-3">অর্ডারের সারসংক্ষেপ</h6>

                                                    <!-- Product Summary Card -->
                                                    <div class="d-flex align-items-center gap-3 p-3 bg-light rounded-3 border mb-3">
                                                        <div class="rounded-2 overflow-hidden border bg-white" style="width: 56px; height: 56px; flex-shrink: 0;">
                                                            <img src="/theme_multiproduct_landing/static/src/img/book_psychology_money.jpg" alt="Psychology of Money" class="w-100 h-100 object-fit-cover"/>
                                                        </div>
                                                        <div class="flex-grow-1 overflow-hidden">
                                                            <div class="fw-bold text-dark text-truncate small">The Psychology of Money (সাইকোলজি অব মানি)</div>
                                                            <span id="summary-variant-name-2" class="d-none">The Psychology of Money</span>
                                                            <div class="fw-bold text-primary small mt-1">
                                                                ৳<span id="summary-unit-price-2" data-price="320.00">320.00</span>
                                                            </div>
                                                        </div>
                                                    </div>

                                                    <!-- Hidden Product ID -->
                                                    <input type="hidden" name="product_id" id="input-product-id-2" value="24"/>

                                                    <!-- Quantity Adjuster with Prominent Buttons -->
                                                    <div class="d-flex justify-content-between align-items-center mb-3 p-2 bg-light rounded-3 border">
                                                        <span class="fw-bold text-dark small ps-2">পরিমাণ</span>
                                                        <div class="d-flex align-items-center gap-2">
                                                            <button type="button" class="btn btn-dark btn-sm landing-qty-btn rounded-circle d-flex align-items-center justify-content-center" data-product-index="2" data-action="minus" style="width: 32px; height: 32px; font-size: 1.1rem; line-height: 1; padding: 0;">-</button>
                                                            <input type="number" name="quantity" id="input-qty-2" value="1" min="1" max="99" class="form-control text-center fw-bold landing-qty-input border-0 py-0 bg-transparent fs-6" style="width: 48px;" data-product-index="2"/>
                                                            <button type="button" class="btn btn-dark btn-sm landing-qty-btn rounded-circle d-flex align-items-center justify-content-center" data-product-index="2" data-action="plus" style="width: 32px; height: 32px; font-size: 1.1rem; line-height: 1; padding: 0;">+</button>
                                                        </div>
                                                    </div>

                                                    <!-- Live Cost Breakdown -->
                                                    <div class="landing-cost-breakdown pt-2 border-top">
                                                        <div class="d-flex justify-content-between align-items-center mb-2 small text-muted">
                                                            <span>বইয়ের মূল্য</span>
                                                            <span class="text-dark fw-semibold">
                                                                ৳<span id="calc-subtotal-2">320.00</span>
                                                            </span>
                                                        </div>
                                                        <div class="d-flex justify-content-between align-items-center mb-2 small text-muted">
                                                            <span>ডেলিভারি চার্জ</span>
                                                            <span class="text-primary fw-semibold">৳<span id="calc-shipping-2">60.00</span></span>
                                                        </div>
                                                        <div class="d-flex justify-content-between align-items-center pt-2 border-top fs-5 fw-bold text-dark">
                                                            <span>সর্বমোট মূল্য</span>
                                                            <span class="text-primary">
                                                                ৳<span id="calc-total-2">380.00</span>
                                                            </span>
                                                        </div>
                                                    </div>

                                                </div>
                                            </div>

                                        </div>
                                    </div>

                                    <!-- ALWAYS-VISIBLE MODAL FOOTER -->
                                    <div class="modal-footer bg-white border-top p-2.5 p-sm-3 d-flex flex-row justify-content-between align-items-center gap-2 gap-sm-3">
                                        <div class="d-flex flex-column align-items-start">
                                            <span class="text-muted small fw-medium" style="font-size: 0.72rem; line-height: 1.1;">সর্বমোট প্রদেয়:</span>
                                            <span class="fs-5 fs-sm-4 fw-bolder text-primary lh-1">
                                                ৳<span id="calc-total-footer-2">380.00</span>
                                            </span>
                                        </div>
                                        <button type="submit" id="submit-btn-2" class="btn btn-dark btn-md px-3 px-sm-4 py-2.5 py-sm-3 rounded-pill fw-bold shadow landing-submit-order-btn d-flex align-items-center justify-content-center gap-2 flex-grow-1 flex-sm-grow-0" style="max-width: 260px;">
                                            <i class="fa fa-check-circle"></i>
                                            <span class="btn-text">অর্ডার কনফার্ম করুন</span>
                                            <div class="spinner-border spinner-border-sm d-none" role="status"></div>
                                        </button>
                                    </div>

                                </form>

                            </div>
                        </div>
                    </div>

                    <!-- ==========================================
                         PRODUCT 03: DEEP WORK
                         ========================================== -->
                    <section id="product-3" class="landing-product-section py-3 py-lg-5 position-relative" data-name="বই ০৩ Showcase" data-snippet="s_single_product_showcase" data-product-template-id="11" data-product-id="25">
                        <div class="container" style="max-width: 1140px;">
                            <div class="landing-product-card shadow-sm border bg-white rounded-4 rounded-lg-5 p-3 p-sm-4 p-lg-5">
                            
                                <!-- PRODUCT HEADER / PILL BADGE -->
                                <div class="d-flex align-items-center justify-content-between mb-3 mb-sm-4 flex-wrap gap-2">
                                    <div class="d-flex align-items-center gap-2">
                                        <span class="badge bg-dark text-white rounded-pill px-3 py-2 fw-bold text-uppercase" style="font-size: 0.75rem;">
                                            বই ০৩
                                        </span>
                                        <span class="badge bg-primary-subtle text-primary border border-primary-subtle rounded-pill px-3 py-2 fw-semibold">
                                            PRODUCTIVITY MASTERWORK • প্রোডাক্টিভিটি
                                        </span>
                                    </div>
                                    <div class="d-flex align-items-center gap-2 small text-muted">
                                        <div class="text-warning">
                                            <i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i>
                                        </div>
                                        <span class="fw-bold text-dark">4.9</span>
                                        <span>(1150 reviews)</span>
                                    </div>
                                </div>

                                <!-- 2-COLUMN DESKTOP LAYOUT -->
                                <div class="row g-4 g-lg-5 align-items-start">
                                
                                    <!-- LEFT COLUMN: PRODUCT IMAGES -->
                                    <div class="col-12 col-lg-6 landing-slide-left">
                                        <div class="landing-gallery-sticky">
                                            <div class="landing-main-image-container rounded-4 overflow-hidden border bg-white shadow-sm position-relative mb-3">
                                                <img id="main-image-3" 
                                                     src="/theme_multiproduct_landing/static/src/img/book_deep_work.jpg" 
                                                     alt="Deep Work (ডিপ ওয়ার্ক)" 
                                                     class="img-fluid w-100 landing-main-img snippet-display-img" 
                                                     style="max-height: 520px; object-fit: contain; padding: 24px; transition: transform 0.4s ease;"/>
                                                <span class="position-absolute top-0 start-0 m-3 badge bg-white text-dark border shadow-sm px-3 py-2 rounded-pill fw-semibold">
                                                    <i class="fa fa-check text-success me-1"></i> স্টকে আছে • দ্রুত ডেলিভারি
                                                </span>
                                            </div>

                                            <!-- Thumbnails Strip -->
                                            <div class="d-flex gap-2 landing-thumbnails-row">
                                                <button type="button" class="btn p-0 border rounded-3 overflow-hidden landing-thumb-btn active" data-target="main-image-3" data-src="/theme_multiproduct_landing/static/src/img/book_deep_work.jpg" style="width: 72px; height: 72px;">
                                                    <img src="/theme_multiproduct_landing/static/src/img/book_deep_work.jpg" alt="Deep Work Cover" class="w-100 h-100 object-fit-cover"/>
                                                </button>
                                            </div>
                                        </div>
                                    </div>

                                    <!-- RIGHT COLUMN: PRODUCT INFORMATION -->
                                    <div class="col-12 col-lg-6 landing-slide-right">
                                        <div class="landing-product-info ps-lg-3">
                                            <h2 class="display-6 fw-bolder text-dark mb-2 snippet-display-title">Deep Work (ডিপ ওয়ার্ক)</h2>
                                            
                                            <p class="text-primary fw-semibold fs-5 mb-3 snippet-display-tagline">বিক্ষিপ্ত পৃথিবীতে নিরবচ্ছিন্ন মনোযোগ ও সেরা কাজ করার অনন্য কলাকৌশল।</p>

                                            <!-- Pricing Block -->
                                            <div class="d-flex align-items-baseline gap-3 mb-4">
                                                <span class="display-6 fw-bold text-dark">
                                                    ৳<span id="display-price-3" class="snippet-display-price">360.00</span>
                                                </span>
                                                <span class="text-muted text-decoration-line-through fs-5">
                                                    ৳530.00
                                                </span>
                                                <span class="badge bg-danger-subtle text-danger px-3 py-2 rounded-pill fw-bold">
                                                    Save ৳170.00
                                                </span>
                                            </div>

                                            <!-- Description -->
                                            <div class="text-muted mb-4 fs-6 leading-relaxed snippet-display-desc">
                                                ক্যাল নিউপোর্টের বিখ্যাত বই “ডিপ ওয়ার্ক”। নোটিফিকেশন আর সামাজিক মাধ্যমের এই বিভ্রান্তিকর যুগে কীভাবে যেকোনো কাজে গভীর একাগ্রতা বজায় রাখা যায় এবং অল্প সময়ে সর্বোচ্চ আউটপুট পাওয়া যায়—তার বৈজ্ঞানিক ও পরীক্ষিত ৪টি মূল নিয়ম। প্রফেশনাল ও শিক্ষার্থী সবার জন্যই অবশ্যপাঠ্য।
                                            </div>

                                            <!-- Key Benefits Checklist -->
                                            <div class="landing-benefits-box mb-4">
                                                <h6 class="text-uppercase fw-bold text-dark small tracking-wider mb-3">বইটির মূল বিষয় ও উপকারিতা</h6>
                                                <div class="row g-2">
                                                    <t t-if="p3 and p3.get_landing_benefits_list()">
                                                        <t t-foreach="p3.get_landing_benefits_list()" t-as="benefit">
                                                            <div class="col-12 col-sm-6">
                                                                <div class="d-flex align-items-center gap-2 small text-dark">
                                                                    <i class="fa fa-check-circle text-success fs-6"></i>
                                                                    <span t-esc="benefit"/>
                                                                </div>
                                                            </div>
                                                        </t>
                                                    </t>
                                                    <t t-else="">
                                                        <div class="col-12 col-sm-6">
                                                            <div class="d-flex align-items-center gap-2 small text-dark">
                                                                <i class="fa fa-check-circle text-success fs-6"></i>
                                                                <span>কাজে গভীর মনোযোগ ও ফোকাস ধরে রাখার পরীক্ষিত ৪টি নিয়ম</span>
                                                            </div>
                                                        </div>
                                                        <div class="col-12 col-sm-6">
                                                            <div class="d-flex align-items-center gap-2 small text-dark">
                                                                <i class="fa fa-check-circle text-success fs-6"></i>
                                                                <span>সোশ্যাল মিডিয়া ও মোবাইল বিভ্রান্তি কাটিয়ে প্রোডাক্টিভ হওয়ার উপায়</span>
                                                            </div>
                                                        </div>
                                                        <div class="col-12 col-sm-6">
                                                            <div class="d-flex align-items-center gap-2 small text-dark">
                                                                <i class="fa fa-check-circle text-success fs-6"></i>
                                                                <span>অল্প সময়ে বেশি ও মানসম্মত কাজের আউটপুট তৈরির কৌশল</span>
                                                            </div>
                                                        </div>
                                                        <div class="col-12 col-sm-6">
                                                            <div class="d-flex align-items-center gap-2 small text-dark">
                                                                <i class="fa fa-check-circle text-success fs-6"></i>
                                                                <span>৮০ জিএসএম প্রিমিয়াম সুইডিশ ক্রিম পেপার ও টেকসই নিখুঁত বাইন্ডিং</span>
                                                            </div>
                                                        </div>
                                                    </t>
                                                </div>
                                            </div>

                                            <!-- Technical Specifications Table -->
                                            <div class="landing-specs-box mb-4 p-3 bg-white rounded-3 border" t-if="p3 and p3.get_landing_specs_list()">
                                                <h6 class="text-uppercase fw-bold text-dark small tracking-wider mb-2">বইয়ের বিবরণ ও স্পেসিফিকেশন</h6>
                                                <div class="table-responsive rounded-2 border overflow-hidden">
                                                    <table class="table table-sm table-bordered mb-0 small align-middle">
                                                        <tbody>
                                                            <t t-foreach="p3.get_landing_specs_list()" t-as="spec">
                                                                <t t-if="spec.get('value') and spec.get('value').strip()">
                                                                    <tr>
                                                                        <td class="text-secondary fw-bold py-2 px-3 bg-light" style="width: 35%;" t-esc="spec['label']"/>
                                                                        <td class="text-dark fw-medium py-2 px-3" t-esc="spec['value']"/>
                                                                    </tr>
                                                                </t>
                                                            </t>
                                                        </tbody>
                                                    </table>
                                                </div>
                                            </div>

                                            <!-- Buy Now Action (Triggers Checkout Popup Modal) -->
                                            <div class="landing-action-box pt-2">
                                                <button type="button" 
                                                        class="btn btn-outline-dark btn-lg w-100 rounded-pill py-3 fw-bold shadow-sm d-flex align-items-center justify-content-center gap-2 mb-3 landing-add-to-cart-btn"
                                                        data-product-index="3"
                                                        data-product-template-id="11"
                                                        data-product-id="25">
                                                    <i class="fa fa-shopping-bag me-1"></i>
                                                    <span class="btn-text">কার্টে যোগ করুন</span>
                                                    <div class="spinner-border spinner-border-sm d-none" role="status"></div>
                                                </button>
                                                <button type="button" 
                                                        class="btn btn-dark btn-lg w-100 rounded-pill py-3 fw-bold shadow-sm d-flex align-items-center justify-content-center gap-2 landing-buy-now-trigger" 
                                                        data-bs-toggle="modal" 
                                                        data-bs-target="#product-3-checkout">
                                                    <i class="fa fa-book me-1"></i>
                                                    <span>বইটি অর্ডার করুন</span>
                                                    <i class="fa fa-arrow-right small ms-1"></i>
                                                </button>
                                                <div class="text-center text-muted small mt-2">
                                                    <i class="fa fa-truck me-1 text-primary"></i> সারা দেশে ক্যাশ অন ডেলিভারি ও ফ্রি হোম ডেলিভারি
                                                </div>
                                            </div>

                                        </div>
                                    </div>
                                </div>

                            </div>
                        </div>
                    </section>

                    <!-- POPUP CHECKOUT MODAL FOR PRODUCT 03 -->
                    <div id="product-3-checkout" class="modal fade landing-checkout-modal" tabindex="-1" aria-labelledby="checkoutModalLabel-3" aria-hidden="true" data-bs-backdrop="static">
                        <div class="modal-dialog modal-dialog-centered modal-lg modal-dialog-scrollable">
                            <div class="modal-content rounded-4 border-0 shadow-lg overflow-hidden">
                                
                                <!-- Modal Header -->
                                <div class="modal-header bg-dark text-white p-3 p-lg-4 border-0">
                                    <div class="d-flex align-items-center justify-content-between w-100 me-2">
                                        <div class="d-flex align-items-center gap-3">
                                            <div class="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center flex-shrink-0" style="width: 40px; height: 40px; font-size: 1.1rem;">
                                                <i class="fa fa-shopping-bag"></i>
                                            </div>
                                            <div>
                                                <h5 class="modal-title fw-bold mb-0 text-white" id="checkoutModalLabel-3">
                                                    অর্ডার সম্পন্ন করুন
                                                </h5>
                                                <p class="text-white-50 small mb-0">ক্যাশ অন ডেলিভারিতে অর্ডার সম্পন্ন করতে নিচের তথ্যগুলো পূরণ করুন</p>
                                            </div>
                                        </div>
                                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                                    </div>
                                </div>

                                <!-- Order Form -->
                                <form id="checkout-form-3" class="landing-checkout-form" data-product-index="3">
                                    <input type="hidden" name="csrf_token" t-att-value="request.csrf_token()"/>
                                    
                                    <div class="modal-body p-3 p-lg-4 bg-light">
                                        <div class="row g-4">
                                            
                                            <!-- LEFT COLUMN: CUSTOMER DETAILS -->
                                            <div class="col-12 col-lg-7">
                                                <h6 class="fw-bold text-dark mb-3 d-flex align-items-center gap-2">
                                                    <span class="badge bg-dark rounded-circle" style="width: 24px; height: 24px; font-size: 0.75rem; display: inline-flex; align-items: center; justify-content: center;">1</span>
                                                    <span>আপনার ডেলিভারি তথ্য প্রদান করুন</span>
                                                </h6>

                                                <!-- Full Name -->
                                                <div class="mb-3">
                                                    <label class="form-label small fw-semibold text-dark">নাম <span class="text-danger">*</span></label>
                                                    <div class="input-group">
                                                        <span class="input-group-text bg-white border-end-0 text-muted"><i class="fa fa-user"></i></span>
                                                        <input type="text" name="name" class="form-control border-start-0" placeholder="আপনার নাম লিখুন" required="required"/>
                                                    </div>
                                                </div>

                                                <!-- Mobile Phone -->
                                                <div class="mb-3">
                                                    <label class="form-label small fw-semibold text-dark">মোবাইল নম্বর <span class="text-danger">*</span></label>
                                                    <div class="input-group">
                                                        <span class="input-group-text bg-white border-end-0 text-muted"><i class="fa fa-phone"></i></span>
                                                        <input type="tel" name="phone" class="form-control border-start-0" placeholder="01XXXXXXXXX" required="required"/>
                                                    </div>
                                                    <div class="form-text small">ডেলিভারির সময় এই নম্বরে কল করা হবে।</div>
                                                </div>

                                                <!-- Full Delivery Address -->
                                                <div class="mb-3">
                                                    <label class="form-label small fw-semibold text-dark">সম্পূর্ণ ডেলিভারি ঠিকানা <span class="text-danger">*</span></label>
                                                    <div class="input-group">
                                                        <span class="input-group-text bg-white border-end-0 text-muted"><i class="fa fa-map-marker"></i></span>
                                                        <textarea name="street" rows="2" class="form-control border-start-0" placeholder="বাসা/রোড নম্বর, এলাকা, থানা ও জেলা উল্লেখ করুন" required="required"></textarea>
                                                    </div>
                                                </div>
                                                <input type="hidden" name="city" value="Dhaka"/>

                                                <!-- Delivery Carrier Option -->
                                                <div class="mb-3">
                                                    <label class="form-label small fw-semibold text-dark">ডেলিভারি এরিয়া নির্বাচন করুন <span class="text-danger">*</span></label>
                                                    <div class="d-flex flex-column gap-2">
                                                        <label class="p-2.5 bg-white rounded-3 border border-primary d-flex align-items-center justify-content-between cursor-pointer landing-carrier-option" style="cursor: pointer;">
                                                            <div class="form-check d-flex align-items-center gap-2 mb-0">
                                                                <input class="form-check-input landing-carrier-radio" type="radio" name="carrier_id" value="1" checked="checked" data-price="60.0" data-product-index="3" id="carrier_1_inside_3"/>
                                                                <span class="form-check-label fw-semibold text-dark small" for="carrier_1_inside_3">ঢাকার ভেতরে</span>
                                                            </div>
                                                            <span class="badge bg-primary text-white fw-bold small px-2.5 py-1.5 rounded-pill">৳60</span>
                                                        </label>
                                                        <label class="p-2.5 bg-white rounded-3 border d-flex align-items-center justify-content-between cursor-pointer landing-carrier-option" style="cursor: pointer;">
                                                            <div class="form-check d-flex align-items-center gap-2 mb-0">
                                                                <input class="form-check-input landing-carrier-radio" type="radio" name="carrier_id" value="2" data-price="120.0" data-product-index="3" id="carrier_2_outside_3"/>
                                                                <span class="form-check-label fw-semibold text-dark small" for="carrier_2_outside_3">ঢাকার বাইরে</span>
                                                            </div>
                                                            <span class="badge bg-secondary-subtle text-dark border fw-bold small px-2.5 py-1.5 rounded-pill">৳120</span>
                                                        </label>
                                                    </div>
                                                </div>

                                                <!-- পেমেন্ট পদ্ধতি Section -->
                                                <h6 class="fw-bold text-dark mt-3 mb-2 d-flex align-items-center gap-2">
                                                    <span class="badge bg-dark rounded-circle" style="width: 24px; height: 24px; font-size: 0.75rem; display: inline-flex; align-items: center; justify-content: center;">2</span>
                                                    <span>পেমেন্ট পদ্ধতি</span>
                                                </h6>
                                                <div class="p-3 bg-white rounded-3 border d-flex align-items-center justify-content-between">
                                                    <div class="form-check d-flex align-items-center gap-2 mb-0">
                                                        <input class="form-check-input" type="radio" name="payment_method_3" value="cod" checked="checked" id="codOption-3"/>
                                                        <label class="form-check-label fw-bold text-dark" for="codOption-3">
                                                            ক্যাশ অন ডেলিভারি (পণ্য হাতে পেয়ে মূল্য পরিশোধ)
                                                        </label>
                                                    </div>
                                                    <span class="badge bg-success-subtle text-success border border-success-subtle rounded-pill px-3 py-1 fw-semibold small">
                                                        <i class="fa fa-shield me-1"></i> ক্যাশ অন ডেলিভারি
                                                    </span>
                                                </div>
                                            </div>

                                            <!-- RIGHT COLUMN: ORDER SUMMARY -->
                                            <div class="col-12 col-lg-5">
                                                <div class="bg-white p-3 rounded-4 border shadow-sm">
                                                    <h6 class="fw-bold text-dark mb-3">অর্ডারের সারসংক্ষেপ</h6>

                                                    <!-- Product Summary Card -->
                                                    <div class="d-flex align-items-center gap-3 p-3 bg-light rounded-3 border mb-3">
                                                        <div class="rounded-2 overflow-hidden border bg-white" style="width: 56px; height: 56px; flex-shrink: 0;">
                                                            <img src="/theme_multiproduct_landing/static/src/img/book_deep_work.jpg" alt="Deep Work" class="w-100 h-100 object-fit-cover"/>
                                                        </div>
                                                        <div class="flex-grow-1 overflow-hidden">
                                                            <div class="fw-bold text-dark text-truncate small">Deep Work (ডিপ ওয়ার্ক)</div>
                                                            <span id="summary-variant-name-3" class="d-none">Deep Work</span>
                                                            <div class="fw-bold text-primary small mt-1">
                                                                ৳<span id="summary-unit-price-3" data-price="360.00">360.00</span>
                                                            </div>
                                                        </div>
                                                    </div>

                                                    <!-- Hidden Product ID -->
                                                    <input type="hidden" name="product_id" id="input-product-id-3" value="25"/>

                                                    <!-- Quantity Adjuster with Prominent Buttons -->
                                                    <div class="d-flex justify-content-between align-items-center mb-3 p-2 bg-light rounded-3 border">
                                                        <span class="fw-bold text-dark small ps-2">পরিমাণ</span>
                                                        <div class="d-flex align-items-center gap-2">
                                                            <button type="button" class="btn btn-dark btn-sm landing-qty-btn rounded-circle d-flex align-items-center justify-content-center" data-product-index="3" data-action="minus" style="width: 32px; height: 32px; font-size: 1.1rem; line-height: 1; padding: 0;">-</button>
                                                            <input type="number" name="quantity" id="input-qty-3" value="1" min="1" max="99" class="form-control text-center fw-bold landing-qty-input border-0 py-0 bg-transparent fs-6" style="width: 48px;" data-product-index="3"/>
                                                            <button type="button" class="btn btn-dark btn-sm landing-qty-btn rounded-circle d-flex align-items-center justify-content-center" data-product-index="3" data-action="plus" style="width: 32px; height: 32px; font-size: 1.1rem; line-height: 1; padding: 0;">+</button>
                                                        </div>
                                                    </div>

                                                    <!-- Live Cost Breakdown -->
                                                    <div class="landing-cost-breakdown pt-2 border-top">
                                                        <div class="d-flex justify-content-between align-items-center mb-2 small text-muted">
                                                            <span>বইয়ের মূল্য</span>
                                                            <span class="text-dark fw-semibold">
                                                                ৳<span id="calc-subtotal-3">360.00</span>
                                                            </span>
                                                        </div>
                                                        <div class="d-flex justify-content-between align-items-center mb-2 small text-muted">
                                                            <span>ডেলিভারি চার্জ</span>
                                                            <span class="text-primary fw-semibold">৳<span id="calc-shipping-3">60.00</span></span>
                                                        </div>
                                                        <div class="d-flex justify-content-between align-items-center pt-2 border-top fs-5 fw-bold text-dark">
                                                            <span>সর্বমোট মূল্য</span>
                                                            <span class="text-primary">
                                                                ৳<span id="calc-total-3">420.00</span>
                                                            </span>
                                                        </div>
                                                    </div>

                                                </div>
                                            </div>

                                        </div>
                                    </div>

                                    <!-- ALWAYS-VISIBLE MODAL FOOTER -->
                                    <div class="modal-footer bg-white border-top p-2.5 p-sm-3 d-flex flex-row justify-content-between align-items-center gap-2 gap-sm-3">
                                        <div class="d-flex flex-column align-items-start">
                                            <span class="text-muted small fw-medium" style="font-size: 0.72rem; line-height: 1.1;">সর্বমোট প্রদেয়:</span>
                                            <span class="fs-5 fs-sm-4 fw-bolder text-primary lh-1">
                                                ৳<span id="calc-total-footer-3">420.00</span>
                                            </span>
                                        </div>
                                        <button type="submit" id="submit-btn-3" class="btn btn-dark btn-md px-3 px-sm-4 py-2.5 py-sm-3 rounded-pill fw-bold shadow landing-submit-order-btn d-flex align-items-center justify-content-center gap-2 flex-grow-1 flex-sm-grow-0" style="max-width: 260px;">
                                            <i class="fa fa-check-circle"></i>
                                            <span class="btn-text">অর্ডার কনফার্ম করুন</span>
                                            <div class="spinner-border spinner-border-sm d-none" role="status"></div>
                                        </button>
                                    </div>

                                </form>

                            </div>
                        </div>
                    </div>

                </div>

                <!-- MIDDLE EDITABLE SNIPPET ZONE -->
                <div class="oe_structure oe_empty" id="oe_structure_landing_middle"/>

                <!-- SECTION 07: TRUST & WHY CHOOSE US -->
                <section id="trust-section" class="landing-trust-section py-5 bg-white border-top border-bottom" data-snippet="s_three_columns">
                    <div class="container py-lg-4">
                        <div class="text-center mb-5">
                            <span class="landing-pill-badge">পাঠকদের বিশ্বস্ত ঠিকানা</span>
                            <h2 class="display-6 fw-bold text-dark mt-2 mb-3">কেন পাঠকেরা আমাদের থেকে বই সংগ্রহ করেন</h2>
                            <p class="text-muted mx-auto" style="max-width: 600px;">প্রতিটি বই প্রিমিয়াম কোয়ালিটি পেপারে মুদ্রিত, সুতার নিখুঁত সেলাইয়ে মজবুতভাবে বাঁধাইকৃত এবং সারাদেশে ক্যাশ অন ডেলিভারি সুবিধায় পৌঁছে দেওয়া হয়।</p>
                        </div>
                        <div class="row g-4">
                            <div class="col-12 col-sm-6 col-lg-3">
                                <div class="landing-trust-card p-4 rounded-4 h-100 text-center text-sm-start">
                                    <div class="landing-trust-icon-box mb-3 text-primary">
                                        <i class="fa fa-book fa-2x"></i>
                                    </div>
                                    <h5 class="fw-bold text-dark mb-2">১০০% প্রিমিয়াম প্রিন্ট</h5>
                                    <p class="text-muted small mb-0">৮০ জিএসএম সুইডিশ বুক ক্রিম পেপার ও স্পষ্ট ঝকঝকে ফন্ট, যা দীর্ঘক্ষণ পড়লেও চোখের কোনো ক্লান্তি আনে না।</p>
                                </div>
                            </div>
                            <div class="col-12 col-sm-6 col-lg-3">
                                <div class="landing-trust-card p-4 rounded-4 h-100 text-center text-sm-start">
                                    <div class="landing-trust-icon-box mb-3 text-success">
                                        <i class="fa fa-handshake-o fa-2x"></i>
                                    </div>
                                    <h5 class="fw-bold text-dark mb-2">ক্যাশ অন ডেলিভারি</h5>
                                    <p class="text-muted small mb-0">কোনো অগ্রিম পেমেন্ট ছাড়াই সারা দেশে ক্যাশ অন ডেলিভারি। বই হাতে পেয়ে চেক করে মূল্য পরিশোধ করুন।</p>
                                </div>
                            </div>
                            <div class="col-12 col-sm-6 col-lg-3">
                                <div class="landing-trust-card p-4 rounded-4 h-100 text-center text-sm-start">
                                    <div class="landing-trust-icon-box mb-3 text-warning">
                                        <i class="fa fa-truck fa-2x"></i>
                                    </div>
                                    <h5 class="fw-bold text-dark mb-2">দ্রুত হোম ডেলিভারি</h5>
                                    <p class="text-muted small mb-0">অর্ডার কনফার্মেশনের ২৪ ঘণ্টার মধ্যে ডিসপ্যাচ। ঢাকা সিটিতে ২৪-৪৮ ঘণ্টা এবং সারাদেশে ২-৩ দিনে হোম ডেলিভারি।</p>
                                </div>
                            </div>
                            <div class="col-12 col-sm-6 col-lg-3">
                                <div class="landing-trust-card p-4 rounded-4 h-100 text-center text-sm-start">
                                    <div class="landing-trust-icon-box mb-3 text-info">
                                        <i class="fa fa-refresh fa-2x"></i>
                                    </div>
                                    <h5 class="fw-bold text-dark mb-2">ফ্রি ড্যামেজ রিপ্লেসমেন্ট</h5>
                                    <p class="text-muted small mb-0">বইয়ের বাঁধাই বা প্রিন্টিংয়ে কোনো ত্রুটি পেলে ৩ দিনের মধ্যে সম্পূর্ণ বিনামূল্যে তাৎক্ষণিক রিপ্লেসমেন্ট সুবিধা।</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- SECTION 08: CUSTOMER REVIEWS -->
                <section id="reviews-section" class="landing-reviews-section py-5 bg-light" data-snippet="s_three_columns">
                    <div class="container py-lg-4">
                        <div class="text-center mb-5">
                            <span class="landing-pill-badge">পাঠকদের অভিমত</span>
                            <h2 class="display-6 fw-bold text-dark mt-2 mb-3">১০,০০০+ সন্তুষ্ট পাঠকের ভালোবাসা</h2>
                            <div class="d-flex justify-content-center align-items-center gap-2 text-warning fs-5">
                                <i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i>
                                <span class="text-dark fw-bold ms-2">৪.৯ / ৫.০ রেটিং</span>
                            </div>
                        </div>
                        <div class="row g-4">
                            <div class="col-12 col-md-4">
                                <div class="landing-review-card bg-white p-4 rounded-4 shadow-sm h-100 d-flex flex-column justify-content-between">
                                    <div>
                                        <div class="text-warning mb-2">
                                            <i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i>
                                        </div>
                                        <h6 class="fw-bold text-dark mb-2">“অ্যাটোমিক হ্যাবিটস বইটি আমার রুটিন বদলে দিয়েছে”</h6>
                                        <p class="text-muted small">কাগজের কোয়ালিটি ও প্রিন্টিং সত্যি প্রিমিয়াম। বইটির অনুবাদ এত সাবলীল যে এক বসাতেই অনেকটা পড়া হয়ে যায়। ক্যাশ অন ডেলিভারিতে একদম অক্ষত অবস্থায় পেয়েছি।</p>
                                    </div>
                                    <div class="d-flex align-items-center gap-3 pt-3 border-top">
                                        <div class="rounded-circle bg-dark text-white d-flex align-items-center justify-content-center fw-bold" style="width: 38px; height: 38px; font-size: 0.85rem;">তহ</div>
                                        <div>
                                            <div class="fw-bold text-dark small">তানভীর হাসান</div>
                                            <div class="text-muted" style="font-size: 0.72rem;">ধানমন্ডি, ঢাকা • ভেরিফায়েড ক্রেতা</div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div class="col-12 col-md-4">
                                <div class="landing-review-card bg-white p-4 rounded-4 shadow-sm h-100 d-flex flex-column justify-content-between">
                                    <div>
                                        <div class="text-warning mb-2">
                                            <i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i>
                                        </div>
                                        <h6 class="fw-bold text-dark mb-2">“সাইকোলজি অব মানি প্রত্যেকের পড়া উচিত”</h6>
                                        <p class="text-muted small">অর্থ ব্যবস্থাপনা নিয়ে এত চমৎকার বাস্তবিক বই আগে পড়া হয়নি। বইয়ের ফন্ট সাইজ যথেষ্ট বড় হওয়ায় চোখে চাপ পড়ে না। প্রিমিয়াম বাইন্ডিংয়ের মান অসাধারণ।</p>
                                    </div>
                                    <div class="d-flex align-items-center gap-3 pt-3 border-top">
                                        <div class="rounded-circle bg-dark text-white d-flex align-items-center justify-content-center fw-bold" style="width: 38px; height: 38px; font-size: 0.85rem;">সা</div>
                                        <div>
                                            <div class="fw-bold text-dark small">সাদিয়া আফরিন</div>
                                            <div class="text-muted" style="font-size: 0.72rem;">উত্তরা, ঢাকা • ভেরিফায়েড ক্রেতা</div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div class="col-12 col-md-4">
                                <div class="landing-review-card bg-white p-4 rounded-4 shadow-sm h-100 d-flex flex-column justify-content-between">
                                    <div>
                                        <div class="text-warning mb-2">
                                            <i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i>
                                        </div>
                                        <h6 class="fw-bold text-dark mb-2">“ডিপ ওয়ার্ক—মোবাইল অ্যাডিকশন কাটানোর সেরা ওষুধ”</h6>
                                        <p class="text-muted small">লেখাপড়া এবং কাজের ফাঁকে মনোযোগ ধরে রাখার দুর্দান্ত কৌশল শেখা যায়। মাত্র ২ দিনেই হোম ডেলিভারি পেয়েছি। সার্ভিস ও বইয়ের মান ১০/১০।</p>
                                    </div>
                                    <div class="d-flex align-items-center gap-3 pt-3 border-top">
                                        <div class="rounded-circle bg-dark text-white d-flex align-items-center justify-content-center fw-bold" style="width: 38px; height: 38px; font-size: 0.85rem;">রা</div>
                                        <div>
                                            <div class="fw-bold text-dark small">রাকিবুল ইসলাম</div>
                                            <div class="text-muted" style="font-size: 0.72rem;">জিইসি, চট্টগ্রাম • ভেরিফায়েড ক্রেতা</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- SECTION 09: FAQ ACCORDION -->
                <section id="faq-section" class="landing-faq-section py-5 bg-white border-top" data-snippet="s_accordion">
                    <div class="container py-lg-4" style="max-width: 860px;">
                        <div class="text-center mb-5">
                            <span class="landing-pill-badge">সাধারণ জিজ্ঞাসা</span>
                            <h2 class="display-6 fw-bold text-dark mt-2 mb-3">সচরাচর জিজ্ঞাসিত প্রশ্নাবলি (FAQ)</h2>
                            <p class="text-muted mx-auto" style="max-width: 540px;">আপনার অর্ডার, ডেলিভারি ও বইয়ের মান সম্পর্কিত সব প্রশ্নের পরিষ্কার উত্তর।</p>
                        </div>

                        <div class="accordion" id="landingFaqAccordion">
                            <div class="accordion-item border rounded-3 mb-3 overflow-hidden shadow-sm">
                                <h2 class="accordion-header" id="faqHeading1">
                                    <button class="accordion-button fw-bold text-dark" type="button" data-bs-toggle="collapse" data-bs-target="#faqCollapse1" aria-expanded="true" aria-controls="faqCollapse1">
                                        বইগুলোর কাগজ ও বাঁধাইয়ের মান কেমন?
                                    </button>
                                </h2>
                                <div id="faqCollapse1" class="accordion-collapse collapse show" aria-labelledby="faqHeading1" data-bs-parent="#landingFaqAccordion">
                                    <div class="accordion-body text-muted small">
                                        প্রতিটি বই প্রিমিয়াম ৮০ জিএসএম সুইডিশ বুক ক্রিম পেপারে মুদ্রিত। স্পষ্ট বড় অক্ষরের ফন্ট ব্যবহার করা হয়েছে যেন দীর্ঘ সময় পড়লেও চোখের ক্লান্তি না হয়। বইটি সুতার নিখুঁত সেলাই দিয়ে মজবুতভাবে বাঁধাইকৃত, ফলে বারবার পড়ার পরও পৃষ্ঠা খুলে যাওয়ার কোনো সম্ভাবনা নেই।
                                    </div>
                                </div>
                            </div>

                            <div class="accordion-item border rounded-3 mb-3 overflow-hidden shadow-sm">
                                <h2 class="accordion-header" id="faqHeading2">
                                    <button class="accordion-button collapsed fw-bold text-dark" type="button" data-bs-toggle="collapse" data-bs-target="#faqCollapse2" aria-expanded="false" aria-controls="faqCollapse2">
                                        ডেলিভারি পেতে কতদিন সময় লাগে ও ডেলিভারি চার্জ কত?
                                    </button>
                                </h2>
                                <div id="faqCollapse2" class="accordion-collapse collapse" aria-labelledby="faqHeading2" data-bs-parent="#landingFaqAccordion">
                                    <div class="accordion-body text-muted small">
                                        অর্ডার কনফার্মেশনের ২৪ ঘণ্টার মধ্যে পার্সেল ডিসপ্যাচ করা হয়। ঢাকা সিটিতে ২৪ থেকে ৪৮ ঘণ্টার মধ্যে এবং ঢাকার বাইরে সারা বাংলাদেশে ২ থেকে ৩ কার্যদিবসের মধ্যে হোম ডেলিভারি সম্পন্ন হয়। আজকের স্পেশাল অফারে সারা দেশে ফ্রি ডেলিভারি সুবিধা কার্যকর রয়েছে।
                                    </div>
                                </div>
                            </div>

                            <div class="accordion-item border rounded-3 mb-3 overflow-hidden shadow-sm">
                                <h2 class="accordion-header" id="faqHeading3">
                                    <button class="accordion-button collapsed fw-bold text-dark" type="button" data-bs-toggle="collapse" data-bs-target="#faqCollapse3" aria-expanded="false" aria-controls="faqCollapse3">
                                        ক্যাশ অন ডেলিভারিতে কীভাবে অর্ডার করব?
                                    </button>
                                </h2>
                                <div id="faqCollapse3" class="accordion-collapse collapse" aria-labelledby="faqHeading3" data-bs-parent="#landingFaqAccordion">
                                    <div class="accordion-body text-muted small">
                                        অর্ডার করা অত্যন্ত সহজ। আপনার পছন্দের বইয়ের নিচে "Order Now" বাটনে ক্লিক করে চেকআউট পপআপে আপনার নাম, মোবাইল নম্বর এবং পূর্ণ ঠিকানা দিয়ে "অর্ডার কনফার্ম করুন (Cash on Delivery)" বাটনে ক্লিক করুন। কোনো অগ্রিম টাকা লাগবে না; বই হাতে পেয়ে দেখে ডেলিভারি ম্যানের কাছে মূল্য পরিশোধ করবেন।
                                    </div>
                                </div>
                            </div>

                            <div class="accordion-item border rounded-3 mb-3 overflow-hidden shadow-sm">
                                <h2 class="accordion-header" id="faqHeading4">
                                    <button class="accordion-button collapsed fw-bold text-dark" type="button" data-bs-toggle="collapse" data-bs-target="#faqCollapse4" aria-expanded="false" aria-controls="faqCollapse4">
                                        বইয়ে কোনো ত্রুটি থাকলে কি রিটার্ন বা এক্সচেঞ্জ করা যাবে?
                                    </button>
                                </h2>
                                <div id="faqCollapse4" class="accordion-collapse collapse" aria-labelledby="faqHeading4" data-bs-parent="#landingFaqAccordion">
                                    <div class="accordion-body text-muted small">
                                        অবশ্যই! পার্সেল গ্রহণের পর বইয়ে কোনো প্রিন্টিং ত্রুটি, পাতা উল্টাপাল্টা বা পরিবহনে কোনো ক্ষতি হলে ৩ দিনের মধ্যে আমাদের কাস্টমার কেয়ারে যোগাযোগ করলেই কোনো বাড়তি চার্জ ছাড়াই সম্পূর্ণ বিনামূল্যে নতুন বই দিয়ে পরিবর্তন করে দেওয়া হবে।
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- BOTTOM EDITABLE SNIPPET ZONE -->
                <div class="oe_structure oe_empty" id="oe_structure_landing_bottom"/>

                <!-- SECTION 10: FOOTER -->
                <footer class="landing-footer py-5 bg-dark text-white border-top border-secondary">
                    <div class="container py-lg-4">
                        <div class="row g-4 justify-content-between">
                            <div class="col-12 col-md-4">
                                <div class="d-flex align-items-center mb-3">
                                    <span t-field="website.logo" t-options="{'widget': 'image'}" role="img" t-att-aria-label="'Logo of %s' % website.name" t-att-title="website.name" class="landing-footer-logo-wrap"/>
                                </div>
                                <p class="text-secondary small mb-3">জ্ঞানপিপাসু ও দূরদর্শী পাঠকদের জন্য জীবন পরিবর্তনের সেরা ৩টি মাস্টারপিস বইয়ের বিশেষ কালেকশন। মানসম্মত পেপার, মজবুত বাঁধাই ও সারা দেশে নিরাপদ হোম ডেলিভারি।</p>
                                <div class="d-flex gap-3 text-secondary">
                                    <a href="#" class="text-secondary text-decoration-none"><i class="fa fa-instagram fa-lg"></i></a>
                                    <a href="#" class="text-secondary text-decoration-none"><i class="fa fa-facebook fa-lg"></i></a>
                                    <a href="#" class="text-secondary text-decoration-none"><i class="fa fa-twitter fa-lg"></i></a>
                                </div>
                            </div>
                            <div class="col-6 col-md-2">
                                <h6 class="text-uppercase fw-bold text-white small mb-3">বইসমূহ</h6>
                                <ul class="list-unstyled text-secondary small d-flex flex-column gap-2 mb-0">
                                    <li><a href="#product-1" class="text-secondary text-decoration-none">Atomic Habits</a></li>
                                    <li><a href="#product-2" class="text-secondary text-decoration-none">Psychology of Money</a></li>
                                    <li><a href="#product-3" class="text-secondary text-decoration-none">Deep Work</a></li>
                                    <li><a href="#product-1-checkout" class="text-secondary text-decoration-none">ক্যাশ অন ডেলিভারি</a></li>
                                </ul>
                            </div>
                            <div class="col-6 col-md-2">
                                <h6 class="text-uppercase fw-bold text-white small mb-3">গ্রাহক সেবা</h6>
                                <ul class="list-unstyled text-secondary small d-flex flex-column gap-2 mb-0">
                                    <li><a href="#trust-section" class="text-secondary text-decoration-none">ডেলিভারি পলিসি</a></li>
                                    <li><a href="#trust-section" class="text-secondary text-decoration-none">রিটার্ন ও এক্সচেঞ্জ</a></li>
                                    <li><a href="#reviews-section" class="text-secondary text-decoration-none">পাঠকদের রিভিউ</a></li>
                                    <li><a href="#faq-section" class="text-secondary text-decoration-none">সাধারণ জিজ্ঞাসা</a></li>
                                </ul>
                            </div>
                            <div class="col-12 col-md-3">
                                <h6 class="text-uppercase fw-bold text-white small mb-3">যোগাযোগ</h6>
                                <ul class="list-unstyled text-secondary small d-flex flex-column gap-2 mb-0">
                                    <li class="d-flex align-items-center gap-2"><i class="fa fa-envelope text-primary"></i> support@bookmart.com</li>
                                    <li class="d-flex align-items-center gap-2"><i class="fa fa-phone text-primary"></i> +880 1700-000000</li>
                                    <li class="d-flex align-items-center gap-2"><i class="fa fa-map-marker text-primary"></i> বাংলাবাজার, ঢাকা, বাংলাদেশ</li>
                                </ul>
                            </div>
                        </div>
                        <div class="d-flex flex-column flex-sm-row justify-content-between align-items-center pt-4 mt-4 border-top border-secondary text-secondary small">
                            <div>&amp;copy; 2026 BookMart. সর্বস্বত্ব সংরক্ষিত।</div>
                            <div class="d-flex gap-3 mt-2 mt-sm-0">
                                <span class="badge bg-secondary-subtle text-secondary border">১০০% নিরাপদ চেকআউট</span>
                                <span class="badge bg-secondary-subtle text-secondary border">ক্যাশ অন ডেলিভারি</span>
                            </div>
                        </div>
                    </div>
                </footer>

                <!-- ========================================== -->
                <!-- Multi-Product Cart Checkout Modal         -->
                <!-- ========================================== -->
                <div class="modal fade landing-checkout-modal" id="landingCartCheckoutModal" tabindex="-1" aria-labelledby="cartCheckoutModalLabel" aria-hidden="true" data-bs-backdrop="static">
                    <div class="modal-dialog modal-dialog-centered modal-lg modal-dialog-scrollable">
                        <div class="modal-content rounded-4 border-0 shadow-lg overflow-hidden">
                            
                            <!-- Modal Header -->
                            <div class="modal-header bg-dark text-white p-3 p-lg-4 border-0">
                                <div class="d-flex align-items-center justify-content-between w-100 me-2">
                                    <div class="d-flex align-items-center gap-3">
                                        <div class="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center flex-shrink-0" style="width: 40px; height: 40px; font-size: 1.1rem;">
                                            <i class="fa fa-shopping-cart"></i>
                                        </div>
                                        <div>
                                            <h5 class="modal-title fw-bold mb-0 text-white" id="cartCheckoutModalLabel">
                                                কার্ট চেকআউট
                                            </h5>
                                            <p class="text-white-50 small mb-0">ক্যাশ অন ডেলিভারিতে অর্ডার সম্পন্ন করতে নিচের তথ্যগুলো পূরণ করুন</p>
                                        </div>
                                    </div>
                                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                                </div>
                            </div>

                            <!-- Order Form -->
                            <form id="landingCartCheckoutForm" class="landing-checkout-form">
                                <input type="hidden" name="csrf_token" t-att-value="request.csrf_token()"/>

                                <!-- Modal Body (Scrollable) -->
                                <div class="modal-body p-3 p-lg-4 bg-light">
                                    <div class="row g-4">
                                        <!-- Left Column: Customer & Delivery Info -->
                                        <div class="col-12 col-lg-7">
                                            <div class="bg-white p-3 p-md-4 rounded-3 border border-light-subtle h-100">
                                                <h6 class="fw-bold text-dark mb-3 d-flex align-items-center gap-2">
                                                    <span class="badge bg-dark rounded-circle" style="width: 22px; height: 22px; display: inline-flex; align-items: center; justify-content: center; font-size: 0.75rem;">১</span>
                                                    আপনার ডেলিভারি তথ্য প্রদান করুন
                                                </h6>

                                                <div class="mb-3">
                                                    <label class="form-label small fw-semibold text-secondary">নাম <span class="text-danger">*</span></label>
                                                    <div class="input-group">
                                                        <span class="input-group-text bg-light border-end-0 text-muted"><i class="fa fa-user"></i></span>
                                                        <input type="text" class="form-control landing-input border-start-0 ps-0" name="name" placeholder="আপনার নাম লিখুন" required="required"/>
                                                    </div>
                                                </div>

                                                <div class="mb-3">
                                                    <label class="form-label small fw-semibold text-secondary">মোবাইল নম্বর <span class="text-danger">*</span></label>
                                                    <div class="input-group">
                                                        <span class="input-group-text bg-light border-end-0 text-muted"><i class="fa fa-phone"></i></span>
                                                        <input type="tel" class="form-control landing-input border-start-0 ps-0" name="phone" placeholder="01XXXXXXXXX" required="required"/>
                                                    </div>
                                                    <small class="text-muted" style="font-size: 0.75rem;">ডেলিভারির সময় এই নম্বরে কল করা হবে।</small>
                                                </div>

                                                <div class="mb-3">
                                                    <label class="form-label small fw-semibold text-secondary">সম্পূর্ণ ডেলিভারি ঠিকানা <span class="text-danger">*</span></label>
                                                    <div class="input-group">
                                                        <span class="input-group-text bg-light border-end-0 text-muted"><i class="fa fa-map-marker"></i></span>
                                                        <textarea class="form-control landing-input border-start-0 ps-0" name="street" rows="2" placeholder="বাসা/রোড নম্বর, এলাকা, থানা ও জেলা উল্লেখ করুন" required="required"></textarea>
                                                    </div>
                                                </div>

                                                <div class="mb-3">
                                                    <label class="form-label small fw-semibold text-secondary">ডেলিভারি এরিয়া নির্বাচন করুন <span class="text-danger">*</span></label>
                                                    <div class="d-flex flex-column gap-2">
                                                        <label class="d-flex align-items-center justify-content-between p-2.5 rounded-3 border bg-light-subtle cursor-pointer hover-shadow-sm transition-all" style="cursor: pointer;">
                                                            <div class="d-flex align-items-center gap-2">
                                                                <input type="radio" name="cart_delivery_carrier_id" value="1" data-charge="60" checked="checked" class="form-check-input mt-0 cart-carrier-radio"/>
                                                                <span class="fw-semibold small text-dark">ঢাকার ভেতরে</span>
                                                            </div>
                                                            <span class="badge bg-dark-subtle text-dark fw-bold">৳৬০</span>
                                                        </label>
                                                        <label class="d-flex align-items-center justify-content-between p-2.5 rounded-3 border bg-light-subtle cursor-pointer hover-shadow-sm transition-all" style="cursor: pointer;">
                                                            <div class="d-flex align-items-center gap-2">
                                                                <input type="radio" name="cart_delivery_carrier_id" value="2" data-charge="120" class="form-check-input mt-0 cart-carrier-radio"/>
                                                                <span class="fw-semibold small text-dark">ঢাকার বাইরে</span>
                                                            </div>
                                                            <span class="badge bg-dark-subtle text-dark fw-bold">৳১২০</span>
                                                        </label>
                                                    </div>
                                                </div>

                                                <div class="p-3 bg-light rounded-3 border border-light-subtle mt-3 landing-cod-box">
                                                    <div class="d-flex align-items-center justify-content-between">
                                                        <div class="d-flex align-items-center gap-2">
                                                            <input type="radio" checked="checked" disabled="disabled" class="form-check-input mt-0"/>
                                                            <div>
                                                                <span class="fw-bold small text-dark d-block">ক্যাশ অন ডেলিভারি</span>
                                                                <span class="text-muted" style="font-size: 0.72rem;">পণ্য হাতে পেয়ে মূল্য পরিশোধ</span>
                                                            </div>
                                                        </div>
                                                        <span class="badge bg-success-subtle text-success small"><i class="fa fa-shield"></i> ১০০% নিরাপদ</span>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>

                                        <!-- Right Column: Cart Items & Calculations -->
                                        <div class="col-12 col-lg-5">
                                            <div class="bg-white p-3 p-md-4 rounded-3 border border-light-subtle h-100">
                                                <h6 class="fw-bold text-dark mb-3">অর্ডারের সারসংক্ষেপ</h6>

                                                <!-- Dynamic Cart Items Container -->
                                                <div id="cartModalItemsContainer" class="d-flex flex-column gap-2 mb-3" style="max-height: 240px; overflow-y: auto;">
                                                    <div class="text-center py-4 text-muted small">
                                                        <i class="fa fa-spinner fa-spin fa-2x mb-2 text-secondary"></i>
                                                        <div>কার্ট লোড করা হচ্ছে...</div>
                                                    </div>
                                                </div>

                                                <hr class="my-2"/>

                                                <!-- Pricing Summary -->
                                                <div class="d-flex justify-content-between small text-secondary mb-1.5">
                                                    <span>বইয়ের মোট মূল্য</span>
                                                    <span class="fw-semibold text-dark" id="cartModalSubtotal">৳০.০০</span>
                                                </div>
                                                <div class="d-flex justify-content-between small text-secondary mb-1.5">
                                                    <span>ডেলিভারি চার্জ</span>
                                                    <span class="fw-semibold text-dark" id="cartModalDelivery">৳৬০.০০</span>
                                                </div>
                                                <div class="d-flex justify-content-between align-items-center pt-2 border-top">
                                                    <span class="fw-bold text-dark fs-6">সর্বমোট মূল্য</span>
                                                    <span class="fw-bold text-dark fs-5" id="cartModalGrandTotal">৳০.০০</span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- ALWAYS-VISIBLE PINNED MODAL FOOTER -->
                                <div class="modal-footer bg-white border-top p-2.5 p-sm-3 d-flex flex-row justify-content-between align-items-center gap-2 gap-sm-3">
                                    <div class="d-flex flex-column align-items-start">
                                        <span class="text-muted small fw-medium" style="font-size: 0.72rem; line-height: 1.1;">সর্বমোট প্রদেয়:</span>
                                        <span class="fs-5 fs-sm-4 fw-bolder text-primary lh-1" id="cartModalPayable">
                                            ৳০.০০
                                        </span>
                                    </div>
                                    <button type="submit" id="cartSubmitBtn" class="btn btn-dark btn-md px-3 px-sm-4 py-2.5 py-sm-3 rounded-pill fw-bold shadow d-flex align-items-center justify-content-center gap-2 flex-grow-1 flex-sm-grow-0" style="max-width: 260px;">
                                        <i class="fa fa-check-circle"></i>
                                        <span id="cartSubmitBtnText">অর্ডার কনফার্ম করুন</span>
                                        <div class="spinner-border spinner-border-sm d-none" role="status"></div>
                                    </button>
                                </div>
                            </form>

                        </div>
                    </div>
                </div>

                <!-- ORDER SUCCESS NOTIFICATION MODAL -->
                <div id="landingOrderSuccessModal" class="modal fade" tabindex="-1" aria-hidden="true" data-bs-backdrop="static">
                    <div class="modal-dialog modal-dialog-centered modal-md">
                        <div class="modal-content rounded-4 border-0 shadow-lg overflow-hidden">
                            <div class="modal-header bg-dark text-white p-4 border-0 d-flex justify-content-between align-items-center">
                                <div class="d-flex align-items-center gap-3">
                                    <div class="rounded-circle bg-success text-white d-flex align-items-center justify-content-center" style="width: 48px; height: 48px; font-size: 1.4rem;">
                                        <i class="fa fa-check"></i>
                                    </div>
                                    <div>
                                        <h5 class="modal-title fw-bold text-white mb-0">আপনার অর্ডারটি সফল হয়েছে!</h5>
                                        <p class="text-white-50 small mb-0">আমাদের সাথে থাকার জন্য ধন্যবাদ। আপনার পার্সেল প্রস্তুত করা হচ্ছে।</p>
                                    </div>
                                </div>
                                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body p-4 bg-light">
                                <div class="bg-white p-3 rounded-4 border shadow-sm mb-3">
                                    <div class="row g-3">
                                        <div class="col-6">
                                            <div class="text-muted text-uppercase fw-bold" style="font-size: 0.68rem;">অর্ডার রসিদ</div>
                                            <div class="fw-bold text-dark fs-5 mt-1" id="successOrderRef">S00001</div>
                                            <span class="badge bg-success-subtle text-success mt-1 small">কনফার্মড</span>
                                        </div>
                                        <div class="col-6 border-start ps-3">
                                            <div class="text-muted text-uppercase fw-bold" style="font-size: 0.68rem;">ডেলিভারি তথ্য</div>
                                            <div class="fw-semibold text-dark small mt-1" id="successCustomerName">Customer</div>
                                            <div class="text-muted small" id="successCustomerPhone">01700000000</div>
                                            <div class="text-muted small text-truncate" id="successCustomerAddress">Address</div>
                                        </div>
                                    </div>
                                    <hr class="my-3"/>
                                    <div class="d-flex justify-content-between small text-muted mb-1">
                                        <span>অর্ডারকৃত বই</span>
                                        <span class="fw-semibold text-dark" id="successProductName">Item</span>
                                    </div>
                                    <div class="d-flex justify-content-between small text-muted mb-1">
                                        <span>বইয়ের মূল্য</span>
                                        <span class="fw-semibold text-dark" id="successSubtotal">৳0.00</span>
                                    </div>
                                    <div class="d-flex justify-content-between small text-muted mb-2">
                                        <span>ডেলিভারি চার্জ</span>
                                        <span class="text-success fw-semibold">ফ্রি</span>
                                    </div>
                                    <div class="d-flex justify-content-between fs-5 fw-bold text-dark pt-2 border-top">
                                        <span>সর্বমোট টাকা</span>
                                        <span class="text-primary" id="successTotal">৳0.00</span>
                                    </div>
                                </div>
                                <div class="d-flex flex-column gap-2">
                                    <a href="/my/orders" class="btn btn-outline-dark rounded-pill py-2.5 fw-semibold text-decoration-none text-center">
                                        আমার সব অর্ডার দেখুন
                                    </a>
                                    <button type="button" class="btn btn-dark rounded-pill py-2.5 fw-semibold" data-bs-dismiss="modal">
                                        আরও বই দেখুন
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </t>
    </template>

    <!-- Legacy / reusable template alias -->
    <template id="single_product_block" name="Single Product Showcase and Checkout Block">
        <t t-call="theme_multiproduct_landing.s_single_product_showcase"/>
    </template>
</odoo>
'''

target_path = r'd:\Antigravity\Odoo theme\Landing Page\theme_multiproduct_landing\views\templates.xml'
with open(target_path, 'w', encoding='utf-8') as f:
    f.write(TEMPLATES_XML)

print(f"Generated clean templates.xml at {target_path} (length: {len(TEMPLATES_XML)})")
