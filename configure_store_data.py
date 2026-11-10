import psycopg2
import json

conn = psycopg2.connect(dbname='Testdata', user='odoo', password='odoopwd', host='localhost')
cur = conn.cursor()

# 1. Update Product 6
cur.execute("""
    UPDATE product_template
    SET landing_featured = true,
        landing_sequence = 1,
        landing_badge = 'BEST SELLER • SIGNATURE',
        landing_tagline = 'Milled from 320GSM heavy twill cotton with reinforced twin-needle stitching.',
        landing_headline = 'Rugged Utility Meets Tailored Sophistication',
        landing_original_price = 119.00,
        landing_rating = 4.9,
        landing_reviews_count = 184,
        landing_benefits = 'Heavy 320GSM Long-Staple Cotton Twill\nReinforced Dual Chest Pockets with Flaps\nSolid Antique Brass Riveted Buttons\nPre-Shrunk & Enzyme Washed for Softness\nWater & Stain-Resistant Protective Coating',
        landing_specs = 'Material: 100% Ring-Spun Cotton Twill\nWeight: 320GSM Heavyweight\nHardware: Antique Brass Riveted Buttons\nStitching: Twin-Needle Heavy Thread\nFit: Modern Tailored Utility Cut\nCare: Cold Machine Wash / Hang Dry'
    WHERE id = 6;
""")

# 2. Update Product 8
cur.execute("""
    UPDATE product_template
    SET landing_featured = true,
        landing_sequence = 2,
        landing_badge = 'FLAGSHIP EDITION • LIMITED',
        landing_tagline = 'Custom-milled 500GSM loopback French terry with double-layered structural hood.',
        landing_headline = 'The Ultimate Benchmark in Architectural Fleece',
        landing_original_price = 135.00,
        landing_rating = 5.0,
        landing_reviews_count = 216,
        landing_benefits = 'Custom-Milled 500GSM 100% Cotton Fleece\nSculpted Double-Layered Geometric Hood\nSeamless Kangaroo Pouch Pocket\nRibbed Side Panels for Unrestricted Motion\nAnti-Pilling & Zero-Shrink Treatment',
        landing_specs = 'Material: 100% Combed Loopback French Terry\nWeight: 500GSM Ultra-Heavyweight\nCuffs: 2x2 Heavy Spandex Ribbed Knit\nHood: Double Layer Self-Fabric Hood\nOrigin: Milled in Wakayama, Japan\nWarranty: 5-Year Seam Integrity'
    WHERE id = 8;
""")

# 3. Update Product 11
cur.execute("""
    UPDATE product_template
    SET landing_featured = true,
        landing_sequence = 3,
        landing_badge = 'HERITAGE LUXURY • MASTERWORK',
        landing_tagline = 'Double-breasted outerwear crafted from Australian merino and Mongolian cashmere.',
        landing_headline = 'Unrivaled Elegance Engineered for Modern Elements',
        landing_original_price = 340.00,
        landing_rating = 4.9,
        landing_reviews_count = 94,
        landing_benefits = '70% Australian Merino Wool & 30% Grade-A Cashmere\nWind-Blocking & Hydrophobic Micro-Finish\nNatural Hand-Carved Horn Buttons\nFull Interior Bemberg Cupro Satin Lining\nDeep Welt Pockets & Storm Throat Latch',
        landing_specs = 'Fabric: 70% Merino Wool, 30% Mongolian Cashmere\nLining: 100% Bemberg Cupro Breathable Silk\nHardware: Genuine Buffalo Horn Buttons\nLength: Below-Knee Classic Overcoat Silhouette\nTemperature: Rated Down to -5°C (23°F)\nCare: Specialist Dry Clean Only'
    WHERE id = 11;
""")

# 4. Link on Website 1
cur.execute("""
    UPDATE website
    SET landing_product_1_id = 6,
        landing_product_2_id = 8,
        landing_product_3_id = 11,
        landing_hero_badge = 'Curated Signature Collection',
        landing_hero_title = 'Three Masterpieces. One Elevated Experience.',
        landing_hero_subtitle = 'Explore three masterfully crafted products designed for uncompromising quality, timeless aesthetics, and everyday performance. Experience each creation below and order directly from this single page.',
        landing_announcement = '★ Free Worldwide Express Shipping & Cash On Delivery Available Today Only'
    WHERE id = 1;
""")

conn.commit()
print("Products & Website landing configuration successfully updated!")

# Verify
cur.execute("SELECT id, name->>'en_US', landing_badge, landing_sequence, landing_original_price FROM product_template WHERE id IN (6, 8, 11);")
for row in cur.fetchall():
    print("Product:", row)

conn.close()

