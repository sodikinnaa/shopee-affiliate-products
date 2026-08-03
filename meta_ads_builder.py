import json
import os
import csv

def generate_ad_copy(product):
    pid = product['id']
    title = product['title']
    price = product['price']
    sold = product['sold']
    comm = product['commission']
    link = product['affiliate_link']

    # Tailored copy & targeting based on product type
    if pid == 1:
        headline = "📦 Zipper Bag Custom Olshop (Free Desain & Sablon)"
        body = f"Pengen brand fashion / olshop kamu kelihatan se-premium brand mall? 🛍️✨\n\nUpgrade packaging olshop kamu pakai Zipper Bag Custom berlogo brand sendiri!\n✅ FREE Desain Logo & Sablon 1 Warna\n✅ Plastik Zipper Premium Frosted & Durable\n✅ Cetak Minimal Cuma 100 Pcs ({price}/pcs)\n\nBikin pembeli makin percaya dan repeat order terus! Klik Beli Sekarang di Shopee! 👇\n{link}"
        desc = f"🌟 {sold} | Komisi Spesial {comm}"
        interests = "Shopping and fashion, Clothing, Boutique, Small business, E-commerce"
        gender = "ALL"
        min_age, max_age = 21, 45
    elif "botol" in title.lower() and "parfum" in title.lower():
        headline = f"🌸 Botol Refill Parfum Travel Size — {price}"
        body = f"Ribet bawa botol parfum kaca gede pas mau nongkrong atau ngantor? 🎒💨\n\nSolusinya pakai {title[:40]} ini!\n✅ Ukuran saku pas di kantong & tas\n✅ Mudah diisi ulang, anti bocor & anti pecah\n✅ Harga super murah cuma {price}!\n\nTetap wangi seharian tanpa bikin tas berat. Dapatkan sekarang di Shopee! ✨ 👇\n{link}"
        desc = f"🔥 Best Seller Travel Essential | {sold}"
        interests = "Perfume, Fragrance, Cosmetics, Beauty, Travel accessories"
        gender = "ALL"
        min_age, max_age = 18, 40
    elif "koper" in title.lower() or "tsa" in title.lower():
        headline = f"✈️ Aksesoris Travel & Koper Premium — {price}"
        body = f"Travel hacks wajib buat kamu yang sering berpergian! 🧳✨\n\nDapatkan {title[:50]} dengan kualitas terbaik!\n✅ Awet & tahan lama\n✅ Praktis dan mudah digunakan\n✅ Solusi koper aman & nyaman\n\nDapatkan promo khusus hari ini di Shopee! 👇\n{link}"
        desc = f"⭐ Travel Hack Wajib | {sold} di Shopee"
        interests = "Frequent travelers, Air travel, Luggage, Vacation, Tourism"
        gender = "ALL"
        min_age, max_age = 22, 50
    elif "bantal" in title.lower():
        headline = f"🛌 Bantal Travel Leher U Empuk & Anti Pegal — {price}"
        body = f"Sering pegal leher pas perjalanan jauh / perjalanan bisnis? 🚗✈️\n\nGunakan Bantal Leher U Premium ini!\n✅ Busa empuk & lembut tidak gampang kempes\n✅ Menopang leher dengan sempurna\n✅ Ringan dan mudah dibawa kemana-mana\n\nKlik Beli Sekarang di Shopee! 👇\n{link}"
        desc = f"✨ Comfort Travel Gear | Komisi {comm}"
        interests = "Travel, Flight, Public transport, Personal comfort"
        gender = "ALL"
        min_age, max_age = 20, 50
    elif "tas" in title.lower() or "pouch" in title.lower() or "stringbag" in title.lower():
        headline = f"🎒 {title[:45]} — {price}"
        body = f"Lagi cari tas / pouch serbaguna dengan kualitas terbaik & harga terjangkau? 🛍️✨\n\nCek produk {title[:50]} ini!\n✅ Bahan berkualitas, awet & tahan lama\n✅ Desain simpel, stylish & praktis\n✅ Harga hemat cuma {price}\n\nStok terbatas! Buruan order sekarang di Shopee! 👇\n{link}"
        desc = f"🔥 Rekomendasi Shopee | {sold}"
        interests = "Fashion accessories, Backpack, Shopping, Lifestyle"
        gender = "ALL"
        min_age, max_age = 18, 40
    else:
        headline = f"🛍️ Promo Hemat Shopee: {title[:40]}"
        body = f"Dapatkan penawaran terbaik untuk {title[:50]}! 🌟\n\n✅ Kualitas terjamin\n✅ Harga terbaik cuma {price}\n✅ Pengiriman cepat & promo komisi Shopee\n\nKlik Beli Sekarang sebelum kehabisan! 👇\n{link}"
        desc = f"✨ Promo Shopee | {sold}"
        interests = "Online shopping, Shopee, E-commerce, Discount shopping"
        gender = "ALL"
        min_age, max_age = 18, 50

    return {
        "headline": headline,
        "body": body,
        "description": desc,
        "interests": interests,
        "gender": gender,
        "min_age": min_age,
        "max_age": max_age
    }

def main():
    if not os.path.exists('products.json'):
        print("[-] File products.json tidak ditemukan.")
        return

    with open('products.json', 'r', encoding='utf-8') as f:
        products = json.load(f)

    queue = []
    csv_rows = []

    # CSV Header for Facebook Ads Manager Bulk Import
    csv_header = [
        "Campaign Name", "Campaign Status", "Buying Type", "Objective",
        "Ad Set Name", "Ad Set Daily Budget", "Ad Set Status", "Min Age", "Max Age", "Gender", "Interests",
        "Ad Name", "Ad Status", "Title", "Body", "Link Description", "Link", "Call to Action"
    ]

    for p in products:
        pid = p['id']
        title = p['title']
        price = p['price']
        link = p['affiliate_link']
        image_url = p.get('image_url', '')
        local_images = p.get('local_images', [])
        image_path = local_images[0] if local_images else ''

        copy = generate_ad_copy(p)

        campaign_name = f"[AFF] Campaign - Product #{pid:02d} ({p['folder']})"
        adset_name = f"AdSet - Audience Target - Product #{pid:02d}"
        ad_name = f"Ad Creative - Product #{pid:02d}"

        # DRAFT / PAUSED STATUS (NEVER ACTIVE UNTIL USER TURNS IT ON)
        status = "PAUSED"

        ad_data = {
            "product_id": pid,
            "folder": p['folder'],
            "campaign_name": campaign_name,
            "campaign_status": status,
            "objective": "OUTBOUND_CLICKS", # Traffic / Link clicks
            "adset_name": adset_name,
            "adset_status": status,
            "daily_budget_idr": 25000,
            "targeting": {
                "min_age": copy['min_age'],
                "max_age": copy['max_age'],
                "gender": copy['gender'],
                "interests": copy['interests']
            },
            "ad_name": ad_name,
            "ad_status": status,
            "creative": {
                "headline": copy['headline'],
                "primary_text": copy['body'],
                "description": copy['description'],
                "call_to_action": "SHOP_NOW",
                "destination_link": link,
                "image_url": image_url,
                "local_image": image_path
            }
        }
        queue.append(ad_data)

        # CSV row for Meta Ads Manager import
        csv_rows.append([
            campaign_name, status, "AUCTION", "OUTBOUND_CLICKS",
            adset_name, 25000, status, copy['min_age'], copy['max_age'], copy['gender'], copy['interests'],
            ad_name, status, copy['headline'], copy['body'].replace('\n', ' '), copy['description'], link, "SHOP_NOW"
        ])

    # Save meta_ads_queue.json
    with open('meta_ads_queue.json', 'w', encoding='utf-8') as f:
        json.dump(queue, f, indent=2, ensure_ascii=False)
    print(f"[+] Successfully generated {len(queue)} Meta Ads configs in 'meta_ads_queue.json' (STATUS: PAUSED).")

    # Save meta_ads_import.csv
    with open('meta_ads_import.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(csv_header)
        writer.writerows(csv_rows)
    print(f"[+] Successfully generated Meta Ads Bulk Import CSV in 'meta_ads_import.csv' (STATUS: PAUSED).")

if __name__ == '__main__':
    main()
