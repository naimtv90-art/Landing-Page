import sys
import os
import urllib.request
import base64
from PIL import Image, ImageDraw, ImageFont
import io

sys.path.append(r'C:\Program Files\Odoo 19.0.20260902\server')
import odoo
from odoo.tools import config
config.parse_config(['-c', r'C:\Program Files\Odoo 19.0.20260902\server\odoo.conf', '-d', 'Testdata'])
from odoo.modules.registry import Registry
from odoo import api, SUPERUSER_ID

img_dir = os.path.abspath(r'theme_multiproduct_landing\static\src\img')
os.makedirs(img_dir, exist_ok=True)

# Helper to fetch or create book cover
def get_book_cover(url, title, author, bg_color, text_color, filename):
    filepath = os.path.join(img_dir, filename)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    downloaded = False
    if url:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
                img = Image.open(io.BytesIO(data))
                img = img.convert('RGB')
                # Resize keeping ratio to around 600x900
                img.thumbnail((600, 900), Image.Resampling.LANCZOS)
                img.save(filepath, format='JPEG', quality=95)
                print(f"Downloaded cover for {title} from {url}")
                downloaded = True
        except Exception as e:
            print(f"Could not download {url}: {e}, generating custom cover...")

    if not downloaded:
        # Create a professional elegant book cover
        img = Image.new('RGB', (600, 900), color=bg_color)
        draw = ImageDraw.Draw(img)
        
        # Border
        draw.rectangle([(20, 20), (580, 880)], outline=text_color, width=3)
        draw.rectangle([(28, 28), (572, 872)], outline=text_color, width=1)
        
        # Spine shadow effect
        for i in range(25):
            alpha_color = tuple(max(0, c - int(25 - i) * 3) for c in bg_color)
            draw.line([(20 + i, 20), (20 + i, 880)], fill=alpha_color, width=1)

        # Title and author
        draw.text((300, 150), "#1 INTERNATIONAL BESTSELLER", fill=text_color, anchor="mm")
        draw.line([(150, 180), (450, 180)], fill=text_color, width=2)
        
        # Split title
        words = title.split(' ')
        y = 350
        for w in words:
            draw.text((300, y), w.upper(), fill=text_color, anchor="mm")
            y += 50
            
        draw.line([(200, y + 40), (400, y + 40)], fill=text_color, width=2)
        draw.text((300, y + 80), f"BY {author.upper()}", fill=text_color, anchor="mm")
        draw.text((300, 800), "PREMIUM COLLECTOR'S EDITION", fill=text_color, anchor="mm")
        
        img.save(filepath, format='JPEG', quality=95)
        print(f"Generated custom cover for {title}")

    with open(filepath, 'rb') as f:
        return base64.b64encode(f.read())

print("Setting up books...")
cover1 = get_book_cover(
    "https://jamesclear.com/wp-content/uploads/2023/05/retina-atomic-habits-full.png",
    "Atomic Habits", "James Clear",
    (245, 243, 238), (20, 20, 20), "book_atomic_habits.jpg"
)

cover2 = get_book_cover(
    "https://m.media-amazon.com/images/S/compressed.photo.goodreads.com/books/1581527774i/41881472.jpg",
    "The Psychology of Money", "Morgan Housel",
    (248, 245, 240), (10, 40, 90), "book_psychology_money.jpg"
)

cover3 = get_book_cover(
    "https://m.media-amazon.com/images/S/compressed.photo.goodreads.com/books/1451409702i/28383248.jpg",
    "Deep Work", "Cal Newport",
    (240, 244, 248), (180, 20, 20), "book_deep_work.jpg"
)

registry = Registry('Testdata')
with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    website = env['website'].browse(1)
    
    # 1. Update Website Branding
    website.write({
        'landing_hero_badge': '★ সেরা ৩টি কালজয়ী বই • স্পেশাল রিডার্স প্যাকেজ',
        'landing_hero_title': 'জীবন বদলে দেওয়ার ৩টি মাস্টারপিস বই। এক পেজে সম্পূর্ণ সংগ্রহ।',
        'landing_hero_subtitle': 'অভ্যাস গঠন, আর্থিক প্রজ্ঞা এবং গভীর মনোযোগের শ্রেষ্ঠ ৩টি কালজয়ী বই। প্রতিটি বইয়ের বিস্তারিত দেখুন, আপনার পছন্দের সাইজ বা সংস্করণ বেছে নিন এবং সরাসরি এই পেজ থেকেই ক্যাশ অন ডেলিভারিতে অর্ডার করুন।',
        'landing_announcement': '★ সারাদেশে ক্যাশ অন ডেলিভারি ও দ্রুত হোম ডেলিভারি সুবিধা | প্রিমিয়াম প্রিন্ট ও মজবুত বাইন্ডিং',
    })
    
    # Company Name
    website.company_id.write({
        'name': 'BOOXTREE • গ্রন্থবিলাস',
        'email': 'orders@booxtree.com',
        'phone': '+880 1712-345678',
    })

    # 2. Configure Books
    books_data = [
        {
            'id': 6,
            'name': 'Atomic Habits (অ্যাটোমিক হ্যাবিটস)',
            'sequence': 1,
            'badge': 'GLOBAL #1 BESTSELLER • অভ্যাস গঠন',
            'tagline': 'সহজে ভালো অভ্যাস গড়ে তোলার এবং খারাপ অভ্যাস দূর করার প্রমাণিত কৌশল।',
            'headline': 'প্রতিদিন মাত্র ১% উন্নতি আপনার জীবনে আনবে অবিশ্বাস্য রূপান্তর',
            'list_price': 350.0,
            'original_price': 520.0,
            'rating': 4.9,
            'reviews_count': 1840,
            'description': 'জেমস ক্লিয়ারের "অ্যাটোমিক হ্যাবিটস" বিশ্বজুড়ে কোটি পাঠকের জীবন বদলে দেওয়া এক বৈপ্লবিক বই। ছোট ছোট ক্ষুদ্র অভ্যাস কীভাবে বিশাল ফলাফলে রূপান্তরিত হয় এবং খারাপ অভ্যাসগুলো কীভাবে চিরতরে দূর করা যায়—তা অত্যন্ত সহজবোধ্য ও বৈজ্ঞানিক উপায়ে ব্যাখ্যা করা হয়েছে। ৮০ জিএসএম সুইডিশ প্রিমিয়াম ক্রিম পেপারে মুদ্রিত এবং মজবুত সেলাই বাঁধাই।',
            'benefits': (
                "চার স্তরের প্রমাণিত অভ্যাস কাঠামো (সংকেত, আকঙ্ক্ষা, প্রতিক্রিয়া ও পুরস্কার)\n"
                "খারাপ অভ্যাস চিরতরে বর্জনের সহজ মনস্তাত্ত্বিক পদ্ধতি\n"
                "প্রতিদিন মাত্র ১% ইতিবাচক পরিবর্তনের মাধ্যমে অভূতপূর্ব সাফল্য\n"
                "স্বাস্থ্যকর রুটিন ও ডিসিপ্লিন ধরে রাখার প্র্যাকটিক্যাল গাইডলাইন\n"
                "৮০ জিএসএম আই-ফ্রেন্ডলি ক্রিম পেপার ও স্পষ্ট বড় ফন্ট"
            ),
            'specs': (
                "মূল লেখক: জেমস ক্লিয়ার (James Clear)\n"
                "প্রকাশনা: প্রিমিয়াম পাবলিকেশন্স (রয়েল এডিশন)\n"
                "পৃষ্ঠা সংখ্যা: ৩২০ পৃষ্ঠা\n"
                "কাগজের মান: ৮০ জিএসএম সুইডিশ প্রিমিয়াম ক্রিম পেপার\n"
                "বাঁধাই: সুতার নিখুঁত সেলাই ও শক্ত বাইন্ডিং (পৃষ্ঠা খোলার ভয় নেই)\n"
                "ভাষা: প্রাঞ্জল ও আকর্ষণীয় বাংলা অনুবাদ"
            ),
            'cover': cover1,
            'extra_m': 150.0, # Medium: 350 + 150 = 500
            'extra_l': 300.0, # Large: 350 + 300 = 650
        },
        {
            'id': 8,
            'name': 'The Psychology of Money (সাইকোলজি অব মানি)',
            'sequence': 2,
            'badge': 'ALL-TIME BESTSELLER • অর্থ ও বিনিয়োগ',
            'tagline': 'সম্পদ, অর্থব্যবস্থাপনা, লোভ ও সুখের কালজয়ী ১৯টি পরম শিক্ষা।',
            'headline': 'অর্থ উপার্জনের চেয়েও বড় বিষয় হলো কীভাবে আপনি অর্থের সাথে আচরণ করেন',
            'list_price': 380.0,
            'original_price': 550.0,
            'rating': 5.0,
            'reviews_count': 1420,
            'description': 'মরগান হাউজেলের লেখা আধুনিক ক্লাসিক বই "সাইকোলজি অব মানি"। অর্থব্যবস্থাপনায় ডিগ্রি বা গাণিতিক দক্ষতার চেয়ে মানুষের মনস্তত্ত্ব ও আচরণ কীভাবে সবচেয়ে গুরুত্বপূর্ণ ভূমিকা রাখে, তা ১৯টি চমৎকার গল্পের মাধ্যমে তুলে ধরা হয়েছে। সম্পদ রক্ষা করা এবং আর্থিক স্বাধীনতা অর্জনের বাস্তবসম্মত দিকনির্দেশনা।',
            'benefits': (
                "অর্থ, সম্পদ ও সুখ নিয়ে বাস্তবমুখী এবং কালজয়ী ১৯টি অনুধাবনযোগ্য অধ্যায়\n"
                "কীভাবে কম্পাউন্ডিং (Compounding) ব্যবহারের মাধ্যমে আর্থিক সমৃদ্ধি নিশ্চিত করবেন\n"
                "লোভ ও ভয় নিয়ন্ত্রণ করে সঠিক ইনভেস্টমেন্ট ও সেভিংস সিদ্ধান্ত নেওয়ার কৌশল\n"
                "টাকা থাকা এবং প্রকৃত ধনী হওয়ার মৌলিক পার্থক্যের বিশ্লেষণ\n"
                "চোখবান্ধব প্রিমিয়াম অফ-হোয়াইট প্রিন্ট ও প্রিমিয়াম আর্টকার্ড কভার"
            ),
            'specs': (
                "মূল লেখক: মরগান হাউজেল (Morgan Housel)\n"
                "প্রকাশনা: প্রিমিয়াম পাবলিকেশন্স (রয়েল এডিশন)\n"
                "পৃষ্ঠা সংখ্যা: ২৮০ পৃষ্ঠা\n"
                "কাগজের মান: ৮০ জিএসএম হাই-কোয়ালিটি সুইডিশ ক্রিম পেপার\n"
                "বাঁধাই: ডাবল গ্লু ও নিখুঁত থ্রেড স্টিচ বাঁধাই\n"
                "ভাষা: প্রাঞ্জল বাংলা অনুবাদ"
            ),
            'cover': cover2,
            'extra_m': 170.0, # Medium: 380 + 170 = 550
            'extra_l': 340.0, # Large: 380 + 340 = 720
        },
        {
            'id': 11,
            'name': 'Deep Work (ডিপ ওয়ার্ক)',
            'sequence': 3,
            'badge': 'PRODUCTIVITY MASTERWORK • প্রডাক্টিভিটি',
            'tagline': 'বিক্ষিপ্ত পৃথিবীতে নিরবচ্ছিন্ন মনোযোগ ও সেরা কাজ করার অনন্য কলাকৌশল।',
            'headline': 'সোশ্যাল মিডিয়ার কোলাহলমুক্ত নিবিড় মনোযোগের শক্তিতে আকাশছোঁয়া সাফল্য',
            'list_price': 360.0,
            'original_price': 530.0,
            'rating': 4.9,
            'reviews_count': 1150,
            'description': 'ক্যাল নিউপোর্টের বিখ্যাত বই "ডিপ ওয়ার্ক"। নোটিফিকেশন আর সামাজিক মাধ্যমের এই বিভ্রান্তিকর যুগে কীভাবে যেকোনো কাজে গভীর একাগ্রতা বজায় রাখা যায় এবং অল্প সময়ে সর্বোচ্চ আউটপুট পাওয়া যায়—তার বৈজ্ঞানিক ও পরীক্ষিত ৪টি মূল নিয়ম। প্রফেশনাল ও শিক্ষার্থী সবার জন্যই অবশ্যপাঠ্য।',
            'benefits': (
                "সোশ্যাল মিডিয়ার আসক্তি কাটিয়ে গভীর কাজের সুপারপাওয়ার অর্জনের ৪টি মূল সূত্র\n"
                "জটিল কাজ অল্প সময়ে শতভাগ নিখুঁতভাবে শেষ করার বৈজ্ঞানিক পদ্ধতি\n"
                "শ্যালো ওয়ার্ক (অপ্রয়োজনীয় ব্যস্ততা) কমিয়ে প্রোডাক্টিভিটি ৩ গুণ বৃদ্ধির ফর্মুলা\n"
                "ক্লান্তিহীন ফোকাস ধরে রাখার জন্য ডেইলি শিডিউলিং ফ্রেমওয়ার্ক\n"
                "প্রিমিয়াম ফিনিশিং ও শক্ত বাঁধাই"
            ),
            'specs': (
                "মূল লেখক: ক্যাল নিউপোর্ট (Cal Newport)\n"
                "প্রকাশনা: প্রিমিয়াম পাবলিকেশন্স (রয়েল এডিশন)\n"
                "পৃষ্ঠা সংখ্যা: ৩২০ পৃষ্ঠা\n"
                "কাগজের মান: ৮০ জিএসএম সুইডিশ বুক পেপার\n"
                "বাঁধাই: প্রিমিয়াম থ্রেড স্টিচ বাইন্ডিং\n"
                "ভাষা: সহজ ও প্রাঞ্জল বাংলা অনুবাদ"
            ),
            'cover': cover3,
            'extra_m': 160.0, # Medium: 360 + 160 = 520
            'extra_l': 320.0, # Large: 360 + 320 = 680
        }
    ]

    for b in books_data:
        tmpl = env['product.template'].browse(b['id'])
        tmpl.write({
            'name': b['name'],
            'landing_sequence': b['sequence'],
            'landing_featured': True,
            'landing_badge': b['badge'],
            'landing_tagline': b['tagline'],
            'landing_headline': b['headline'],
            'list_price': b['list_price'],
            'landing_original_price': b['original_price'],
            'landing_rating': b['rating'],
            'landing_reviews_count': b['reviews_count'],
            'description_sale': b['description'],
            'landing_benefits': b['benefits'],
            'landing_specs': b['specs'],
            'image_1920': b['cover'],
            'is_storable': True,
        })
        print(f"Updated product template {tmpl.id}: {b['name']}")

        # 3. Setup DIFFERENT PRICES for Small, Medium, Large variants
        for ptal in tmpl.attribute_line_ids:
            for ptav in ptal.product_template_value_ids:
                if 'Small' in ptav.name:
                    ptav.write({'price_extra': 0.0})
                    print(f"  {tmpl.name} -> Small (S): Extra = 0.0 (Total: {tmpl.list_price})")
                elif 'Medium' in ptav.name:
                    ptav.write({'price_extra': b['extra_m']})
                    print(f"  {tmpl.name} -> Medium (M): Extra = {b['extra_m']} (Total: {tmpl.list_price + b['extra_m']})")
                elif 'Large' in ptav.name:
                    ptav.write({'price_extra': b['extra_l']})
                    print(f"  {tmpl.name} -> Large (L): Extra = {b['extra_l']} (Total: {tmpl.list_price + b['extra_l']})")

    # 4. Warehouse Stock Verification
    warehouse = env['stock.warehouse'].search([('company_id', '=', website.company_id.id)], limit=1)
    if not warehouse:
        warehouse = env['stock.warehouse'].search([], limit=1)
    stock_loc = warehouse.lot_stock_id

    for b in books_data:
        tmpl = env['product.template'].browse(b['id'])
        for v in tmpl.product_variant_ids:
            if v.qty_available < 50:
                diff = 100.0 - v.qty_available
                env['stock.quant']._update_available_quantity(v, stock_loc, diff)
            print(f"  Variant {v.display_name} (ID {v.id}): Price={v.list_price}, Stock={v.qty_available}")

    cr.commit()
    print("\nAll 3 Books successfully created with distinct variant prices and stock!")

