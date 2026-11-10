# Theme Threadcraft Garments (Odoo 19.0)

**Enterprise-Grade 3D Garments Manufacturing & Apparel Export Website Theme with Native Drag-and-Drop Website Builder Snippets**

---

## 1. Overview & Architectural Philosophy

`theme_threadcraft_garments` is a native Odoo 19.0 website theme module converted directly from the high-performance Threadcraft Garments web platform. It transforms every section into an independent, reusable, movable, duplicable, and editable snippet compatible with the Odoo Website Builder.

### Key Highlights
- **100% Native Odoo 19 Addon**: Built with standard QWeb XML templates, native asset bundles, SCSS design tokens, and modular ES6 `publicWidget` scripts.
- **Dedicated Website Builder Drawer**: Registers a dedicated `"Threadcraft Garments"` block drawer in Odoo's Website Builder containing custom SVG thumbnails for every block.
- **Parametric 3D WebGL Digital Twin Engine**: Embedded Three.js viewport for realtime 3D garment inspection (T-Shirts, Hoodies, Polos), CAD wireframe inspection, and custom pantone colorway switching with zero-latency fallback.
- **True Drag-and-Drop Compatibility**: Drag, drop, duplicate, reorder, and delete any snippet across any page without DOM conflicts or memory leaks.
- **Ready-to-Deploy Multi-Page Architecture**: Pre-configured editable templates for Homepage (`/`), About (`/about`), Manufacturing Capabilities (`/manufacturing`), Products (`/products`), Sustainability & ESG (`/sustainability`), and Contact & RFQ Desk (`/contact`).
- **Odoo eCommerce Ready**: Compatible with native Odoo Website and optional `website_sale` eCommerce catalogs without hardcoded dependencies.

---

## 2. Snippet Library (`Threadcraft` Category)

Every section is available as an independent building block in Odoo's Website Builder Blocks panel:

| Snippet Identifier | Block Name | Description | Key Features |
|---|---|---|---|
| `s_tc_hero` | **Threadcraft 3D Hero** | High-impact hero section with interactive 3D WebGL viewport | Three.js garment viewport, CAD wireframe toggle, silhouette selector, colorway swatches |
| `s_tc_3d_garment` | **3D Garment Inspector** | Standalone 3D garment digital twin showcase | Orbit controls, GSM fabric spec sheet, pantone picker, sample kit request |
| `s_tc_stats` | **Manufacturing Stats** | Animated performance telemetry counters | `IntersectionObserver` animated counters, compliance badge ribbon |
| `s_tc_products` | **Product Categories** | Core garment silhouette catalog | Interactive category filter tabs (Tees, Hoodies, Polos, Outerwear) |
| `s_tc_manufacturing_story` | **Manufacturing Journey** | 6-stage end-to-end production pipeline | Interactive timeline stepper (Fiber, Knitting, Cut, Sewing, QC, Dispatch) |
| `s_tc_factory` | **Factory Digital Twin** | Smart facility campus telemetry | Interactive sector hotspot switcher (SEC-01 through SEC-05), live capacity specs |
| `s_tc_quality` | **Quality Standards** | AQL 1.5 inspection protocols | 4-pillar quality assurance, in-house ISO 17025 testing scope |
| `s_tc_sustainability` | **Sustainability & ESG** | Circular environmental stewardship | Zero Liquid Discharge (ZLD) water recycling, 2.4 MW solar microgrid, waste reclamation |
| `s_tc_global_reach` | **Global Export Network** | Global logistics and trade routes | Port transit times, ocean freight schedules, customs clearance telemetry |
| `s_tc_partners` | **B2B Partnership Models** | Commercial engagement structures | 3 modular partnership cards: OEM Contract, ODM Full-Package, DTC Capsule |
| `s_tc_cta` | **B2B Conversion Banner** | High-conversion quotation callout | Bold typography, 24-hour RFQ turnaround guarantee, mutual NDA indicator |
| `s_tc_contact` | **RFQ & Contact Desk** | Multi-office global directory & RFQ form | Native Odoo form submission, global regional offices (HQ, NYC, London) |

---

## 3. Directory Structure

```
theme_threadcraft_garments/
├── __init__.py                               # Addon initialization
├── __manifest__.py                           # Odoo 19 module manifest and asset bundles
├── README.md                                 # Technical documentation
├── data/
│   └── theme_data.xml                        # Theme configuration records
├── views/
│   ├── layouts/
│   │   ├── header.xml                        # Threadcraft branded header template
│   │   └── footer.xml                        # Threadcraft corporate footer with compliance badges
│   ├── snippets/
│   │   ├── snippets.xml                      # Website Builder block registry & category drawer
│   │   ├── s_tc_hero.xml                     # 3D Hero snippet
│   │   ├── s_tc_3d_garment.xml               # Standalone 3D garment snippet
│   │   ├── s_tc_stats.xml                    # Animated counters snippet
│   │   ├── s_tc_products.xml                 # Products catalog snippet
│   │   ├── s_tc_manufacturing_story.xml      # 6-Stage production journey snippet
│   │   ├── s_tc_factory.xml                  # Factory digital twin snippet
│   │   ├── s_tc_quality.xml                  # Quality assurance snippet
│   │   ├── s_tc_sustainability.xml          # Circular ESG snippet
│   │   ├── s_tc_global_reach.xml             # Global trade network snippet
│   │   ├── s_tc_partners.xml                 # B2B partnership models snippet
│   │   ├── s_tc_cta.xml                      # RFQ conversion banner snippet
│   │   └── s_tc_contact.xml                  # Contact directory & RFQ form snippet
│   ├── options.xml                           # Website Builder customization options
│   └── pages/
│       ├── home.xml                          # Modular homepage drop zone
│       ├── about.xml                         # Company heritage & about page
│       ├── manufacturing.xml                 # Enterprise capabilities page
│       ├── products.xml                      # Apparel silhouettes page
│       ├── sustainability.xml               # ESG & environmental page
│       └── contact.xml                       # RFQ & contact desk page
└── static/
    ├── description/
    │   ├── icon.png                          # Odoo Apps module icon (128x128)
    │   ├── theme_screenshot.png              # Theme preview screenshot (800x500)
    │   └── index.html                        # Odoo Apps marketplace presentation page
    └── src/
        ├── lib/
        │   └── three.min.js                  # Standalone Three.js WebGL library
        ├── img/
        │   └── wbuilder/                     # 12 Custom SVG thumbnails for Builder drawer
        │       ├── s_tc_hero.svg
        │       ├── s_tc_3d_garment.svg
        │       ├── s_tc_stats.svg
        │       ├── s_tc_products.svg
        │       ├── s_tc_manufacturing_story.svg
        │       ├── s_tc_factory.svg
        │       ├── s_tc_quality.svg
        │       ├── s_tc_sustainability.svg
        │       ├── s_tc_global_reach.svg
        │       ├── s_tc_partners.svg
        │       ├── s_tc_cta.svg
        │       └── s_tc_contact.svg
        ├── scss/
        │   ├── primary_variables.scss        # Odoo theme color tokens & typography mapping
        │   ├── theme.scss                    # Global typography, buttons, glassmorphism
        │   └── snippets.scss                 # Dedicated styling for all 12 snippet blocks
        └── js/
            ├── three_scene.js                # Parametric Three.js WebGL rendering engine
            ├── animations.js                 # Scroll reveal & micro-animation controller
            ├── website_builder/
            │   └── snippet_options.js        # Website builder options widget
            └── snippets/
                ├── s_tc_hero.js              # Hero 3D interaction controller
                ├── s_tc_3d_garment.js        # Standalone 3D garment controller
                ├── s_tc_stats.js             # Animated counter observer
                ├── s_tc_products.js          # Product category filter controller
                ├── s_tc_manufacturing_story.js # 6-stage journey stepper
                ├── s_tc_factory.js           # Factory sector hotspot switcher
                └── s_tc_global_reach.js      # Global destination telemetry switcher
```

---

## 4. Installation & Deployment Guide

### Prerequisites
- Odoo 19.0 (Community or Enterprise)
- Python 3.10+ / 3.12+
- PostgreSQL 14+

### Step 1: Copy Addon into Odoo Addons Path
Copy or symlink `theme_threadcraft_garments` into your custom Odoo addons directory:
```bash
# Example on Linux / macOS:
cp -r theme_threadcraft_garments /path/to/odoo/custom_addons/

# Example on Windows:
xcopy /E /I theme_threadcraft_garments C:\odoo\custom_addons\theme_threadcraft_garments
```

Ensure `custom_addons` is included in your `odoo.conf` file:
```ini
[options]
addons_path = /path/to/odoo/addons,/path/to/odoo/odoo/addons,/path/to/odoo/custom_addons
```

### Step 2: Install via CLI or Odoo Web Interface

#### Option A: Command Line Installation
```bash
odoo-bin -c odoo.conf -d your_database_name -i theme_threadcraft_garments
```

To upgrade after making changes:
```bash
odoo-bin -c odoo.conf -d your_database_name -u theme_threadcraft_garments
```

#### Option B: Odoo Web UI
1. Log in to your Odoo backend as an Administrator.
2. Enable Developer Mode (**Settings > Activate the developer mode**).
3. Navigate to **Apps > Update Apps List** and click **Update**.
4. Search for `Theme Threadcraft Garments`.
5. Click **Activate / Install**.
6. Navigate to **Website > Configuration > Settings**, select **Threadcraft Garments** as your active website theme.

---

## 5. Website Builder User Guide

### How to Add & Edit Sections
1. Open your website in a browser and navigate to any page (e.g., `/` or `/manufacturing`).
2. Click the **Edit** button in the top right to open the Website Builder.
3. In the sidebar Blocks drawer, locate the **Threadcraft Garments** section.
4. Drag any block (e.g., `Threadcraft 3D Hero` or `Manufacturing Stats`) onto the page.
5. Click on any text, heading, or badge to edit inline.
6. Click on images or buttons to adjust links or destination pages.
7. Use the up/down arrows in the snippet toolbar to reorder blocks, or click duplicate / delete.
8. Click **Save** in the top bar. All changes persist automatically.

---

## 6. Technical Specifications & Compliance

- **Brand Colors**:
  - Light Natural: `#F5F3EE`
  - Charcoal Dark: `#171717`
  - Volt Accent: `#C7F36B`
  - Off-Black: `#111317`
- **Typography**:
  - Display Headings: `Syne` (Weights 700/800)
  - Body Text: `Plus Jakarta Sans` (Weights 400/500/600)
  - Technical Badges & Data: `JetBrains Mono`
- **Quality Assurance**:
  - 100% Valid XML syntax checked across all 23 QWeb templates.
  - ES6 module standard adherence (`@odoo-module`).
  - Zero external npm build step required at Odoo runtime—all assets pre-bundled.

---

**Developed for THREADCRAFT Apparel Manufacturing Ltd.**  
*License: LGPL-3.0*
