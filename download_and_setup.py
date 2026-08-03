import os
import re
import json
import urllib.request
import urllib.parse
import time

products_data = [
    {
        "id": 1,
        "folder": "product_01_zipper_bag_custom",
        "title": "Zipper bag custom (minimal 100 pcs) Zipper pouch serbaguna free desain + FREE SABLON KANTONG PLASTIK ZIPPER (100pcs)",
        "price": "Rp4.300",
        "sold": "10RB+ terjual",
        "commission": "80%"
    },
    {
        "id": 2,
        "folder": "product_02_tutup_botol_longneck",
        "title": "50 PCS TUTUP BOTOL LONGNECK",
        "price": "Rp8.500",
        "sold": "83 terjual",
        "commission": "71.5%"
    },
    {
        "id": 3,
        "folder": "product_03_tutup_botol_3cm",
        "title": "Tutup botol Diameter 3cm x 9mm tanpa segel untuk bahan kerajinan",
        "price": "Rp17.999",
        "sold": "6 terjual",
        "commission": "71.5%"
    },
    {
        "id": 4,
        "folder": "product_04_bantal_leher_u",
        "title": "Bantal Leher U Empuk Lembut Dan Ringan Bantal Leher U Anti Pegal Neck Pillow Travel",
        "price": "Rp48.599",
        "sold": "2 terjual",
        "commission": "61.5%"
    },
    {
        "id": 5,
        "folder": "product_05_bantal_travel_sandaran",
        "title": "Bantal Travel Sandaran Leher Nyaman Bantal Leher U Empuk Lembut Dan Ringan",
        "price": "Rp48.599",
        "sold": "1 terjual",
        "commission": "60%"
    },
    {
        "id": 6,
        "folder": "product_06_ring_karet_roda_koper",
        "title": "4pcs Ring/Strip Karet Roda Koper Pengganti - Material Silikon Berkualitas, 5 Variasi Warna",
        "price": "Rp25.000",
        "sold": "7 terjual",
        "commission": "57.5%"
    },
    {
        "id": 7,
        "folder": "product_07_masker_tidur_sutra",
        "title": "Masker Tidur Sutra - Bentuk Kontur Wajah, Tali Elastis Lebar Tidak Mengikat Rambut",
        "price": "Rp26.900",
        "sold": "4 terjual",
        "commission": "57.5%"
    },
    {
        "id": 8,
        "folder": "product_08_pelindung_roda_ganda",
        "title": "Pelindung Roda Ganda: Koper dan Kursi - Cover Silikon 6 Warna, Set Komplit 8PCS",
        "price": "Rp35.900",
        "sold": "1 terjual",
        "commission": "57.5%"
    },
    {
        "id": 9,
        "folder": "product_09_masker_mata_3d",
        "title": "Masker Mata 3D Gelap Total - Memory Foam Lembut, Tali Adjustable Anti Bocor Cahaya",
        "price": "Rp65.000",
        "sold": "3 terjual",
        "commission": "57.5%"
    },
    {
        "id": 10,
        "folder": "product_10_tsa_luggage_key",
        "title": "TSA Luggage Key T002 T007 Master Key Kunci Koper Gembok Presisi 4.9g",
        "price": "Rp60.000",
        "sold": "-",
        "commission": "57.5%"
    },
    {
        "id": 11,
        "folder": "product_11_tas_serut_stringbag",
        "title": "Tas Serut Karet Stringbag Multifungsi Pria Wanita Bahan ringkle Ransel Drawstring",
        "price": "Rp35.556",
        "sold": "-",
        "commission": "55%"
    },
    {
        "id": 12,
        "folder": "product_12_tiket_po_lilmobag",
        "title": "Tiket PO LILMOBAG 4 in 1 duffle",
        "price": "Rp50.000",
        "sold": "-",
        "commission": "50%"
    },
    {
        "id": 13,
        "folder": "product_13_tas_pouch_anak",
        "title": "Tas Pouch Anak Multifungsi Zipper Waterproof / Tempat Pensil dan alat tulis sekolah premium",
        "price": "Rp116.910",
        "sold": "-",
        "commission": "50%"
    },
    {
        "id": 14,
        "folder": "product_14_tas_bahu_wey",
        "title": "Tas Bahu WEY, Tas Selempang Kapasitas Besar Soft Puffy Shoulder Bag",
        "price": "Rp84.000",
        "sold": "-",
        "commission": "49%"
    },
    {
        "id": 15,
        "folder": "product_15_botol_kaca_parfum_10ml",
        "title": "Botol kaca parfum kosong 10ml [ grosir perlusin ] penjualan 12 pcs",
        "price": "Rp32.500",
        "sold": "97 terjual",
        "commission": "46.5%"
    },
    {
        "id": 16,
        "folder": "product_16_botol_parfum_spray_5ml",
        "title": "Botol Parfum Kosong Kaca 5ml Spray – Mini Refill Parfum Praktis Dibawa",
        "price": "Rp2.700",
        "sold": "439 terjual",
        "commission": "46.5%"
    },
    {
        "id": 17,
        "folder": "product_17_botol_parfum_hermes_50ml",
        "title": "botol kosong parfum HERMES ukuran 50ml penjualan satuan",
        "price": "Rp8.000",
        "sold": "2 terjual",
        "commission": "46.5%"
    },
    {
        "id": 18,
        "folder": "product_18_botol_parfum_10ml_refill",
        "title": "Botol parfum kosong, buat isi ulang ,ukuran 10ml harga grosir",
        "price": "Rp2.800",
        "sold": "289 terjual",
        "commission": "46.5%"
    },
    {
        "id": 19,
        "folder": "product_19_botol_casa_30ml",
        "title": "botol casa 30 ml baru murah",
        "price": "Rp4.500",
        "sold": "6 terjual",
        "commission": "45%"
    }
]

AFFILIATE_LINK = "https://s.shopee.co.id/5ArO3tWgWH"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def search_image_urls(query, count=4):
    encoded = urllib.parse.quote(f"{query} shopee")
    url = f"https://www.bing.com/images/search?q={encoded}"
    req = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(req, timeout=12).read().decode('utf-8', errors='ignore')
        murls = re.findall(r'&quot;murl&quot;:&quot;(.*?)&quot;', html)
        shopee = [m for m in murls if 'susercontent.com' in m or 'shopee' in m]
        others = [m for m in murls if m not in shopee]
        combined = []
        for u in shopee + others:
            if u not in combined and (u.endswith('.jpg') or u.endswith('.jpeg') or u.endswith('.png') or 'susercontent.com' in u):
                combined.append(u)
        return combined[:count]
    except Exception as e:
        print(f"Error searching for '{query}': {e}")
        return []

def download_image(url, save_path):
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            if len(data) > 3000: # filter out tiny empty tracking pixels
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
    
    print(f"[{item['id']}/19] Fetching images for: {item['title'][:40]}...")
    img_urls = search_image_urls(item['title'], count=5)
    
    downloaded_files = []
    idx = 1
    for url in img_urls:
        ext = '.jpg'
        if '.png' in url.lower():
            ext = '.png'
        file_name = f"image_{idx}{ext}"
        full_path = os.path.join(folder_path, file_name)
        if download_image(url, full_path):
            downloaded_files.append(f"products/{item['folder']}/{file_name}")
            idx += 1
            if idx > 3: # Keep top 3 images per product
                break
        time.sleep(0.3)
        
    item['local_images'] = downloaded_files
    downloaded_products.append(item)

# Save JSON metadata
with open('products.json', 'w', encoding='utf-8') as f:
    json.dump(downloaded_products, f, indent=2, ensure_ascii=False)

# Generate README.md
readme_content = f"""# 🛍️ Shopee Affiliate Products Catalog

Koleksi produk Shopee Affiliate beserta aset gambar produk berkualitas tinggi.

🔗 **Link Affiliate Utama**: [{AFFILIATE_LINK}]({AFFILIATE_LINK})

---

## 📌 Daftar Produk ({len(downloaded_products)} Produk)

"""

for p in downloaded_products:
    readme_content += f"""### {p['id']}. {p['title']}
- **Harga**: `{p['price']}`
- **Penjualan**: `{p['sold']}`
- **Komisi**: `{p['commission']}`
- **Link Pembelian**: [{AFFILIATE_LINK}]({AFFILIATE_LINK})

**Galeri Gambar**:
"""
    if p['local_images']:
        for img in p['local_images']:
            readme_content += f"![{p['title']}]({img}) "
        readme_content += "\n\n"
    else:
        readme_content += "_Gambar sedang diperbarui_\n\n"

    readme_content += "---\n\n"

readme_content += """
## 📁 Struktur Direktori
```
.
├── products/
│   ├── product_01_zipper_bag_custom/
│   ├── product_02_tutup_botol_longneck/
│   └── ...
├── products.json
└── README.md
```
"""

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(readme_content)

print("Finished processing all products and generated README.md & products.json!")
