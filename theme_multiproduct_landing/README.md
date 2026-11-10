# Odoo 19 Single Page Multi-Product Landing Page

A modern, premium, high-converting Single Page Multi-Product eCommerce Landing Page built natively for Odoo 19 Website and eCommerce.

---

## 🌟 Key Features

1. **True Single Page Architecture**:
   - Exactly 3 featured flagship products displayed in a vertical scrolling presentation.
   - Smooth anchor navigation across all products and sections on a single URL (`/` and `/landing`).
   - Sticky navigation header with frosted glass backdrop blur, live cart quantity badge, and instant "Order Now" anchor jumps.

2. **Dedicated Product Showcase**:
   - **Product 01**: Full image gallery, title, hook, benefits checklist, technical specs grid, real Odoo variant chips, pricing, and savings badge.
   - **Product 02**: Dedicated presentation for the second flagship product with unique images, specs, variants, and benefits.
   - **Product 03**: Dedicated presentation for the third flagship product with luxury specifications and variant options.

3. **Inline Instant Checkout on Each Product**:
   - Immediate checkout form placed directly below each product's details.
   - Live variant selection and interactive quantity adjuster (`-` / `+`).
   - Real-time subtotal, shipping fee, and grand total calculations.
   - Customer information collection: Full Name, Phone, Email, Delivery Street Address, City / Area, and Delivery Notes.
   - Seamless support for **Cash on Delivery (COD)** and delivery methods.
   - Creates a **REAL Odoo Sales Order (`sale.order`)** and customer contact (`res.partner`) inside Odoo ERP.
   - Instant Order Confirmation modal receipt with live Order Reference number (e.g. `S00002`).

4. **Trust & Social Proof Sections**:
   - **Trust Pillars**: 100% Authentic Quality, Secure COD, Tracked Express Delivery, Dedicated Concierge.
   - **Customer Reviews**: Testimonial cards with star ratings and verified buyer badges.
   - **Interactive FAQ**: Accordion answering ordering, shipping, COD, and 30-day returns.
   - **Executive Footer**: Brand statement, navigation links, contact details, and policies.

5. **Backend Admin Management**:
   - Dedicated **"Single Page Landing"** tab on the Product Template form view in Odoo ERP backend (`Sales > Products` or `Website > eCommerce > Products`).
   - Administrators can:
     - Toggle feature on landing page (`landing_featured`).
     - Set display sequence (1, 2, 3) (`landing_sequence`).
     - Customize badges (e.g. "Best Seller", "Flagship Edition").
     - Edit taglines, headlines, benefits, specifications, and compare prices.
     - Manage product variants and inventory in standard Odoo backend.
     - View and fulfill orders directly in `Sales > Orders`.

---

## 📁 Module Structure

```text
theme_multiproduct_landing/
├── __init__.py
├── __manifest__.py
├── install_or_upgrade.bat
├── models/
│   ├── __init__.py
│   ├── product_template.py      # Extended landing fields & variant helpers
│   └── website.py               # Website landing configurations & product getters
├── controllers/
│   ├── __init__.py
│   └── main.py                  # HTTP & JSON-RPC routes: /landing, /landing/submit_order, /landing/calculate_summary
├── views/
│   ├── product_views.xml        # Admin backend product form tab
│   └── templates.xml            # Single Page Landing master layout & product showcase blocks
├── static/
│   └── src/
│       ├── css/landing.css      # Apple/Shopify-inspired minimal, responsive stylesheet
│       └── js/landing.js        # Smooth scrolling, variant switcher, live calculations & AJAX order processing
└── data/
    └── landing_data.xml         # Default data
```

---

## 🚀 Live Access URLs

- **Store Homepage**: `http://localhost:8069/?db=Testdata`
- **Direct Landing URL**: `http://localhost:8069/landing?db=Testdata`
- **Odoo ERP Backend (Sales & Orders)**: `http://localhost:8069/web?db=Testdata`

