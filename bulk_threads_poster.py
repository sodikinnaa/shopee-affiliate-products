import os
import json
from threads_poster import ThreadsAPI

def generate_threads_posts():
    if not os.path.exists('products.json'):
        print("[-] products.json tidak ditemukan.")
        return []

    with open('products.json', 'r', encoding='utf-8') as f:
        products = json.load(f)

    # Filter winning & high-commission products
    winning_ids = [1, 2, 6, 16, 18]
    posts = []

    for p in products:
        if p['id'] in winning_ids:
            title = p['title']
            price = p['price']
            sold = p['sold']
            comm = p['commission']
            link = p['affiliate_link']

            if p['id'] == 1:
                hook = "✨ Packaging olshop kamu masih biasa aja? Upgrade ke Zipper Bag Custom berlogo sendiri modal Rp4.300-an aja! Gratis desain & sablon 1 warna! 🔥"
            elif p['id'] == 2:
                hook = "🥤 Solusi kemasan minuman rumahan / herbal anti bocor! Paket 50 Pcs Tutup Botol Longneck segel tamper-evident harga Rp8.500 aja! 🔒"
            elif p['id'] == 6:
                hook = "✈️ Roda koper sering bising atau aus saat ditarik di bandara? Pasang Ring Silikon Roda Koper ini, langsung senyap & awet! Cuma 25rb dapet 4pcs 🔇"
            elif p['id'] == 16:
                hook = "🎒 Ribet bawa botol parfum gede di tas? Pindahin ke Botol Refill Spray 5ml ini, praktis dibawa ke mana-mana cuma Rp2.700! 🌸"
            elif p['id'] == 18:
                hook = "💧 Punya parfum favorit dan sering bepergian? Simpan cadangan di Botol Kaca Refill 10ml Fine Mist ini. Harga grosir mulai Rp2.800! ✨"
            else:
                hook = f"🛍️ Rekomendasi produk Shopee pilihan: {title[:50]}..."

            content = f"{hook}\n\n💰 Harga: {price} ({sold})\n🎁 Komisi Affiliate: {comm}\n\n👉 Cek & Beli di Shopee:\n{link}\n\n#ShopeeAffiliate #ShopeeFinds #RacunShopee #PromoShopee"
            
            posts.append({
                "product_id": p['id'],
                "title": title,
                "post_content": content,
                "affiliate_link": link
            })

    return posts

def main():
    print("=== Shopee Affiliate Threads Post Generator & Auto-Poster ===")
    posts = generate_threads_posts()

    print(f"[+] Berhasil membuat {len(posts)} draf postingan Threads untuk produk Winning.\n")

    # Save to threads_queue.json
    with open('threads_queue.json', 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)

    print("[+] File 'threads_queue.json' telah tersimpan.")

    # Check Threads API Token
    api = ThreadsAPI()
    is_valid, info = api.verify_token()

    if is_valid:
        print("\n[🚀] Inisialisasi pengiriman otomatis ke Threads...")
        for idx, post in enumerate(posts, 1):
            print(f"\n[{idx}/{len(posts)}] Posting Produk #{post['product_id']}: {post['title'][:30]}...")
            res = api.post_text(post['post_content'])
            if res:
                print(f"    ✅ Berhasil dipublikasikan ID: {res}")
            else:
                print("    ❌ Gagal mempublikasikan.")
    else:
        print("\n[ℹ️] Posting otomatis dilewati karena THREADS_ACCESS_TOKEN belum diset di .env")
        print("[ℹ️] Anda bisa melihat draf postingan yang siap pakai di file 'threads_queue.json' atau menyalinnya langsung ke Threads app.")

if __name__ == '__main__':
    main()
