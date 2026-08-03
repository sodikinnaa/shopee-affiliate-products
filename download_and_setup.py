import os
import json
import urllib.request

products_data = [
    {
        "id": 1,
        "folder": "product_01_zipper_bag_custom",
        "title": "zipper bag custom (minimal 100 pcs)Zipper pouch se… pond ZIPPER cetak 1 warna plastik ZIPPER STORAGE",
        "image_url": "https://down-ws-id.img.susercontent.com/id-11134207-82252-mh7ui2tt7t3h9f.webp",
        "affiliate_link": "https://s.shopee.co.id/8fRGG2Smxy",
        "price": "Rp4.300",
        "sold": "10RB+ terjual",
        "commission": "80%"
    },
    {
        "id": 2,
        "folder": "product_02_tutup_botol_longneck",
        "title": "50 PCS TUTUP BOTOL LONGNECK",
        "image_url": "https://down-ws-id.img.susercontent.com/id-11134207-7rasj-m2m2357c2ohe21.webp",
        "affiliate_link": "https://s.shopee.co.id/19Hw7Epyt",
        "price": "Rp8.500",
        "sold": "83 terjual",
        "commission": "71.5%"
    },
    {
        "id": 3,
        "folder": "product_03_tutup_botol_3cm",
        "title": "Tutup botol Diameter 3cm x 9mm tanpa segel untuk bahan kerajinan",
        "image_url": "https://down-ws-id.img.susercontent.com/id-11134207-7rasm-m29uularhzgj74.webp",
        "affiliate_link": "https://s.shopee.co.id/9pdDeBox53",
        "price": "Rp17.999",
        "sold": "6 terjual",
        "commission": "71.5%"
    },
    {
        "id": 4,
        "folder": "product_04_bantal_leher_u",
        "title": "Bantal Leher U Empuk Lembut Dan Ringan Bantal Lehe…l Neck Pillow Travel Bantal Sandaran Leher Nyaman",
        "image_url": "https://down-ws-id.img.susercontent.com/id-11134207-7rbka-mazf75hv517v3f.webp",
        "affiliate_link": "https://s.shopee.co.id/8pkgSM6AFE",
        "price": "Rp48.599",
        "sold": "2 terjual",
        "commission": "61.5%"
    },
    {
        "id": 5,
        "folder": "product_05_bantal_travel_sandaran",
        "title": "Bantal Travel Sandaran Leher Nyaman Bantal Leher U… Dan Ringan Bantal Leher U Anti Pegal Neck Pillow",
        "image_url": "https://down-ws-id.img.susercontent.com/id-11134207-7ra0l-mb3ieu6qojncb8.webp",
        "affiliate_link": "https://s.shopee.co.id/6pzc4gR2ui",
        "price": "Rp48.599",
        "sold": "1 terjual",
        "commission": "60%"
    },
    {
        "id": 6,
        "folder": "product_06_ring_karet_roda_koper",
        "title": "4pcs Ring/Strip Karet Roda Koper Pengganti - Mater…(Single/Double) - Replacement Luggage Wheel Rings",
        "image_url": "https://down-ws-id.img.susercontent.com/id-11134207-822wj-mnxq4kdcxkw0ee.webp",
        "affiliate_link": "https://s.shopee.co.id/3qM0VApFm2",
        "price": "Rp25.000",
        "sold": "7 terjual",
        "commission": "57.5%"
    },
    {
        "id": 7,
        "folder": "product_07_masker_tidur_sutra",
        "title": "Masker Tidur Sutra - Bentuk Kontur Wajah, Tali Ela…Design Wide Elastic Strap No Hair Marks 20.5x10cm",
        "image_url": "https://down-ws-id.img.susercontent.com/sg-11134201-823q1-mp33mu93fev426.webp",
        "affiliate_link": "https://s.shopee.co.id/1Vy5itBkQu",
        "price": "Rp26.900",
        "sold": "4 terjual",
        "commission": "57.5%"
    },
    {
        "id": 8,
        "folder": "product_08_pelindung_roda_ganda",
        "title": "Pelindung Roda Ganda: Koper dan Kursi - Cover Sili…ip & Shock Absorption - Dual Purpose Wheel Covers",
        "image_url": "https://down-ws-id.img.susercontent.com/id-11134207-822wu-mnxq4kd8k9ac4f.webp",
        "affiliate_link": "https://s.shopee.co.id/6VMlg55IGw",
        "price": "Rp35.900",
        "sold": "1 terjual",
        "commission": "57.5%"
    },
    {
        "id": 9,
        "folder": "product_09_masker_mata_3d",
        "title": "Masker Mata 3D Gelap Total - Memory Foam Lembut, T…avel, Anti Bocor Cahaya - 3D Contoured Sleep Mask",
        "image_url": "https://down-ws-id.img.susercontent.com/id-11134207-822wr-mmh7gy33wg04a5.webp",
        "affiliate_link": "https://s.shopee.co.id/19Hw8jEQ9",
        "price": "Rp65.000",
        "sold": "3 terjual",
        "commission": "57.5%"
    },
    {
        "id": 10,
        "folder": "product_10_tsa_luggage_key",
        "title": "TSA Luggage Key T002 T007 Master Key Kunci Koper G…n Anti Karat Travel Bagasi Cadangan TSA Spare Key",
        "image_url": "https://down-ws-id.img.susercontent.com/sg-11134201-8259o-mr8j7gdrkzk592.webp",
        "affiliate_link": "https://s.shopee.co.id/8AUzf9Ui2L",
        "price": "Rp60.000",
        "sold": "-",
        "commission": "57.5%"
    },
    {
        "id": 11,
        "folder": "product_11_tas_serut_stringbag",
        "title": "Tas Serut Karet Stringbag Multifungsi Pria Wanita …remium tas futsal olahraga kuliah || Kiiyoomii ||",
        "image_url": "https://down-ws-id.img.susercontent.com/id-11134207-822ws-mpa5a7r1o45qc0.webp",
        "affiliate_link": "https://s.shopee.co.id/5VUEUFsg9g",
        "price": "Rp35.556",
        "sold": "-",
        "commission": "55%"
    },
    {
        "id": 12,
        "folder": "product_12_tiket_po_lilmobag",
        "title": "Tiket PO LILMOBAG 4 in 1 duffle",
        "image_url": "https://down-ws-id.img.susercontent.com/id-11134207-7r98q-m01jaokitbgn95.webp",
        "affiliate_link": "https://s.shopee.co.id/3g2aItBpI6",
        "price": "Rp50.000",
        "sold": "-",
        "commission": "50%"
    },
    {
        "id": 13,
        "folder": "product_13_tas_pouch_anak",
        "title": "Tas Pouch Anak Multifungsi Zipper Waterproof / Tem… Air Travel Friendly Bisa Diwarnai Berulang-ulang",
        "image_url": "https://down-ws-id.img.susercontent.com/id-11134207-822wr-mplqr2q20c9a1d.webp",
        "affiliate_link": "https://s.shopee.co.id/qiOvgibx3",
        "price": "Rp116.910",
        "sold": "-",
        "commission": "50%"
    },
    {
        "id": 14,
        "folder": "product_14_tas_bahu_wey",
        "title": "Tas Bahu WEY, Tas Selempang Kapasitas Besar yang D…s meseger/ Shoulder Bag/ Tas Selempang / Tas Bahu",
        "image_url": "https://down-ws-id.img.susercontent.com/id-11134207-822wu-mpgi72d4fuha8e.webp",
        "affiliate_link": "https://s.shopee.co.id/2LXCiRyLir",
        "price": "Rp84.000",
        "sold": "-",
        "commission": "49%"
    },
    {
        "id": 15,
        "folder": "product_15_botol_kaca_parfum_10ml",
        "title": "Botol kaca parfum kosong 10ml [ grosir perlusin ] penjualan 12 pcs.",
        "image_url": "https://down-ws-id.img.susercontent.com/id-11134207-7ra0i-mcdl6mo4work69.webp",
        "affiliate_link": "https://s.shopee.co.id/1gHVvEE9gb",
        "price": "Rp32.500",
        "sold": "97 terjual",
        "commission": "46.5%"
    },
    {
        "id": 16,
        "folder": "product_16_botol_parfum_spray_5ml",
        "title": "Botol Parfum Kosong Kaca 5ml Spray – Mini Refill Parfum Praktis Dibawa",
        "image_url": "https://down-ws-id.img.susercontent.com/id-11134207-822wm-mlkmv6g8evprf7.webp",
        "affiliate_link": "https://s.shopee.co.id/6fgBsQ8aw7",
        "price": "Rp2.700",
        "sold": "439 terjual",
        "commission": "46.5%"
    },
    {
        "id": 17,
        "folder": "product_17_botol_parfum_hermes_50ml",
        "title": "botol kosong parfum HERMES ukuran 50ml penjualan satuan",
        "image_url": "https://down-ws-id.img.susercontent.com/id-11134207-81ztn-mfb5byvrponh22.webp",
        "affiliate_link": "https://s.shopee.co.id/AAG42rHGkM",
        "price": "Rp8.000",
        "sold": "2 terjual",
        "commission": "46.5%"
    },
    {
        "id": 18,
        "folder": "product_18_botol_parfum_10ml_refill",
        "title": "Botol parfum kosong, buat isi ulang ,ukuran 10ml harga grosir bila pengambilan banyak",
        "image_url": "https://down-ws-id.img.susercontent.com/id-11134207-8224z-mfurl1p8nf2g12.webp",
        "affiliate_link": "https://s.shopee.co.id/7fYj4GmzWC",
        "price": "Rp2.800",
        "sold": "289 terjual",
        "commission": "46.5%"
    },
    {
        "id": 19,
        "folder": "product_19_botol_casa_30ml",
        "title": "botol casa 30 ml baru murah",
        "image_url": "https://down-ws-id.img.susercontent.com/id-11134207-7rbk4-m8ublj3rx8k23a.webp",
        "affiliate_link": "https://s.shopee.co.id/9Kgx3KuG3e",
        "price": "Rp4.500",
        "sold": "6 terjual",
        "commission": "45%"
    }
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def download_image(url, save_path):
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            if len(data) > 1000:
                with open(save_path, 'wb') as f:
                    f.write(data)
                return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
    return False

os.makedirs('products', exist_ok=True)
downloaded_products = []

for item in products_data:
    folder_path = os.path.join('products', item['folder'])
    os.makedirs(folder_path, exist_ok=True)

    img_filename = "main_image.jpg"
    if ".webp" in item['image_url']:
        img_filename = "main_image.webp"
    elif ".png" in item['image_url']:
        img_filename = "main_image.png"

    full_path = os.path.join(folder_path, img_filename)
    local_rel = f"products/{item['folder']}/{img_filename}"
    
    if os.path.exists(full_path):
        item['local_images'] = [local_rel]
    else:
        print(f"[{item['id']}/19] Fetching image for: {item['title'][:40]}...")
        if download_image(item['image_url'], full_path):
            item['local_images'] = [local_rel]
        else:
            item['local_images'] = []
            
    downloaded_products.append(item)

# Save JSON metadata
with open('products.json', 'w', encoding='utf-8') as f:
    json.dump(downloaded_products, f, indent=2, ensure_ascii=False)

# Root README.md
categories = {
    "📦 Custom Packaging & Business Supplies": [1, 2, 3],
    "✈️ Travel Gear & Problem Solvers": [4, 5, 6, 7, 8, 9, 10, 11, 12],
    "🛍️ Tas & Pouch Organizers": [13, 14],
    "🧴 Botol Parfum Kosong & Refill": [15, 16, 17, 18, 19]
}

winning_products = [
    {
        "id": 1,
        "badge": "🏆 SUPER WINNING (BEST SELLER & KOMISI 80%)",
        "folder": "product_01_zipper_bag_custom",
        "title": "Zipper Bag Custom Sablon (Free Desain)",
        "price": "Rp4.300",
        "sold": "10RB+ terjual",
        "commission": "80%",
        "affiliate_link": "https://s.shopee.co.id/8fRGG2Smxy",
        "target": "Pemilik Olshop, Brand Fashion, Hijab, Shoe Care, Packaging UMKM",
        "angle": "Meningkatkan nilai jual brand olshop dengan packaging zipper bag premium berlogo custom modal hanya 4 ribuan.",
        "hook": "✨ 'Mau packaging olshop kamu kelihatan se-premium brand mall cuma modal 4 ribuan? Pakai zipper bag custom ini, gratis desain dan sablon kantong plastic zipper!'"
    },
    {
        "id": 16,
        "badge": "⚡ IMPULSE BUY WINNING (PENJUALAN TINGGI)",
        "folder": "product_16_botol_parfum_spray_5ml",
        "title": "Botol Parfum Kosong Kaca 5ml Spray",
        "price": "Rp2.700",
        "sold": "439 terjual",
        "commission": "46.5%",
        "affiliate_link": "https://s.shopee.co.id/6fgBsQ8aw7",
        "target": "Mahasiswa, Pekerja Kantoran, Traveler, Pecinta Parfum",
        "angle": "Solusi praktis bawa parfum favorit ukuran saku tanpa ribet bawa botol kaca besar yang berat.",
        "hook": "🎒 'Stop bawa botol parfum segede gaban yang bikin tas berat! Pindahin ke botol refill spray 5ml harga 2 ribuan ini, praktis & anti bocor.'"
    },
    {
        "id": 18,
        "badge": "⚡ IMPULSE BUY WINNING (GROSIR REFILL)",
        "folder": "product_18_botol_parfum_10ml_refill",
        "title": "Botol Parfum Kosong 10ml Refill Grosir",
        "price": "Rp2.800",
        "sold": "289 terjual",
        "commission": "46.5%",
        "affiliate_link": "https://s.shopee.co.id/7fYj4GmzWC",
        "target": "Penjual Parfum Refill, Penggemar Travel Size, Hobi Koleksi Parfum",
        "angle": "Botol refill hemat grosir, gampang diisi ulang dan cocok untuk sampel atau travel bag.",
        "hook": "💧 'Sering kehabisan parfum saat bepergian? Simpan cadangan parfum favoritmu di botol 10ml ini. Harga grosir mulai 2 ribuan aja!'"
    },
    {
        "id": 2,
        "badge": "🔥 HIGH COMMISSION WINNING (KOMISI 71.5%)",
        "folder": "product_02_tutup_botol_longneck",
        "title": "50 Pcs Tutup Botol Longneck",
        "price": "Rp8.500",
        "sold": "83 terjual",
        "commission": "71.5%",
        "affiliate_link": "https://s.shopee.co.id/19Hw7Epyt",
        "target": "Produsen Minuman Rumahan, Herbal, Kopi Literan, UMKM Botol Plastik",
        "angle": "Supplies pengemas minuman ramah kantong dengan segel rapat dan komisi jualan affiliate super gurih (71.5%).",
        "hook": "🥤 'Usaha minuman literan atau herbalmu butuh tutup botol rapat dan presisi? Dapatkan 50 pcs tutup longneck harga 8 ribuan ini!'"
    },
    {
        "id": 6,
        "badge": "🧳 PROBLEM SOLVER TRAVEL WINNING",
        "folder": "product_06_ring_karet_roda_koper",
        "title": "4pcs Ring Silikon Roda Koper Pengganti",
        "price": "Rp25.000",
        "sold": "7 terjual",
        "commission": "57.5%",
        "affiliate_link": "https://s.shopee.co.id/3qM0VApFm2",
        "target": "Traveler, Frequent Flyer, Pekerja Dinas, Liburan Keluarga",
        "angle": "Melindungi roda koper mahal dari aus/pecah dan meredam suara bising saat ditarik di jalanan kasar.",
        "hook": "✈️ 'Trik biar roda koper enggak berisik dan enggak cepet rusak saat travelling! Pasang karet silikon roda koper ini, langsung senyap & estetik!'"
    }
]

readme_root = f"""# 🛍️ Shopee Affiliate Winning Ads Toolkit & Strategy

Rekomendasi **Produk Winning Siap Iklan** (Dilengkapi Hook Video TikTok/Reels, Target Audiens, dan Strategi Promosi) hasil analisa otomatis AI.

---

## 🏆 PRODUK WINNING RECOMMENDED (SIAP IKLAN & PROMOSI)

Berikut adalah produk pilihan rekomendasi AI dengan angka penjualan terbaik, komisi terbesar (hingga **80%**), serta potensi konversi iklan yang sangat tinggi:

"""

for w in winning_products:
    readme_root += f"""### {w['badge']}
**{w['title']}**
- 📂 **Folder Direktori**: [`products/{w['folder']}`](./products/{w['folder']})
- 💰 **Harga**: `{w['price']}` | 📈 **Penjualan**: `{w['sold']}` | 🎁 **Komisi**: `{w['commission']}`
- 🔗 **Link Pembelian**: [{w['affiliate_link']}]({w['affiliate_link']})
- 🎯 **Target Audiens**: {w['target']}
- 💡 **Angle / Sudut Pandang Iklan**: {w['angle']}
- 🎬 **Skrip Hook Content (TikTok / Reels / Ads)**:
  > {w['hook']}

---

"""

readme_root += """## 💡 STRATEGI IKLAN & KONTEN AFFILIATE

1. **Untuk Produk B2B (Zipper Bag & Tutup Botol)**:
   - Gunakan platform **TikTok, Instagram Reels, dan FB Ads**.
   - Buat konten berformat *Problem & Solution* atau *Packing Order / Unboxing Branding*.
   - Sertakan kata kunci: *"Packaging Olshop Premium", "Grosir Packaging Murah", "Cara Olshop Terlihat Mahal"*.

2. **Untuk Produk Travel & Problem Solver (Ring Karet Koper & Masker 3D)**:
   - Gunakan format video *Life Hacks / Travel Hacks*.
   - Tunjukkan perbandingan *Before vs After* (Suara koper bising tanpa ring vs Senyap dengan ring silikon).

3. **Untuk Produk Impulse Buy (Botol Parfum Refill 5ml & 10ml)**:
   - Targetkan anak muda, wanita, dan pekerja kantor.
   - Buat video *What's In My Bag* (WIMB) atau tutorial memindahkan parfum kesayangan ke botol travel size.

---

## 📂 KATALOG & DAFTAR PRODUK LENGKAP

Seluruh daftar produk dan folder aset gambar berada di dalam direktori **`products/`**.

👉 **[Buka Catalog & List Produk Lengkap di Folder Products](./products/README.md)**

```
.
├── products/
│   ├── README.md (Daftar & Galeri Produk Lengkap)
│   ├── product_01_zipper_bag_custom/
│   ├── product_02_tutup_botol_longneck/
│   └── ... (19 folder produk)
├── products.json
├── download_and_setup.py
└── README.md
```
"""

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(readme_root)

# Generate products/README.md
prod_by_id = {p['id']: p for p in downloaded_products}

readme_products = f"""# 📦 Katalog & Daftar Produk Lengkap

Semua aset gambar tersimpan rapi di dalam masing-masing sub-folder direktori `products/`. Setiap produk dilengkapi dengan link affiliate khusus.

---

## 📂 DAFTAR PRODUK PER KATEGORI

"""

for cat_name, ids in categories.items():
    readme_products += f"### {cat_name}\n\n"
    readme_products += "| No | Folder Direktori | Nama Produk | Harga | Penjualan | Komisi | Link Affiliate |\n"
    readme_products += "|---|---|---|---|---|---|---|\n"
    for pid in ids:
        p = prod_by_id[pid]
        readme_products += f"| {p['id']} | [`{p['folder']}`](./{p['folder']}) | {p['title']} | `{p['price']}` | `{p['sold']}` | **{p['commission']}** | [{p['affiliate_link']}]({p['affiliate_link']}) |\n"
    readme_products += "\n"

readme_products += "---\n\n## 📸 RINCIAN GALERI & DETIL PRODUK PER FOLDER\n\n"

for p in downloaded_products:
    readme_products += f"""### {p['id']}. {p['title']}
- 📂 **Lokasi Folder**: [`{p['folder']}`](./{p['folder']})
- 💰 **Harga**: `{p['price']}`
- 📈 **Penjualan**: `{p['sold']}`
- 🎁 **Komisi**: `{p['commission']}`
- 🔗 **Link Pembelian Affiliate**: [{p['affiliate_link']}]({p['affiliate_link']})

**Gambar Produk**:
"""
    if p['local_images']:
        for img in p['local_images']:
            rel_img = img.replace('products/', './')
            readme_products += f"![{p['title']}]({rel_img})\n"
        readme_products += "\n"
    else:
        readme_products += "_Gambar sedang diperbarui_\n\n"

    readme_products += "---\n\n"

with open('products/README.md', 'w', encoding='utf-8') as f:
    f.write(readme_products)

print("Finished processing all products and updated README.md, products/README.md, and products.json!")
