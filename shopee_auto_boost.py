import os
import time
import hmac
import hashlib
import json
import urllib.request
import urllib.parse

def load_env(env_path='.env'):
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    k = key.strip()
                    v = val.strip().strip('"').strip("'")
                    if v and not os.environ.get(k):
                        os.environ[k] = v

class ShopeeBoostAPI:
    """
    Client resmi Shopee Open API v2 untuk fitur 'Naikkan Produk' (Auto Boost Item).
    Shopee mengizinkan maksimal 5 produk dinaikkan secara bersamaan setiap 4 jam sekali.
    """
    def __init__(self, partner_id=None, partner_key=None, shop_id=None, access_token=None):
        load_env()
        self.partner_id = partner_id or os.getenv('SHOPEE_PARTNER_ID', '')
        self.partner_key = partner_key or os.getenv('SHOPEE_PARTNER_KEY', '')
        self.shop_id = shop_id or os.getenv('SHOPEE_SHOP_ID', '')
        self.access_token = access_token or os.getenv('SHOPEE_ACCESS_TOKEN', '')
        self.host = "https://partner.shopeemobile.com"

    def _generate_sign(self, path, timestamp):
        base_string = f"{self.partner_id}{path}{timestamp}{self.access_token}{self.shop_id}"
        sign = hmac.new(
            self.partner_key.encode('utf-8'),
            base_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return sign

    def boost_items(self, item_ids):
        """
        Menaikkan produk ke paling atas hasil pencarian Shopee (Maksimal 5 item ID)
        API Endpoint: /api/v2/product/boost_item
        """
        if not self.partner_id or not self.partner_key or not self.access_token:
            print("[-] Credential Shopee Open API (SHOPEE_PARTNER_ID, SHOPEE_PARTNER_KEY, SHOPEE_ACCESS_TOKEN) belum diset di .env")
            print("[ℹ️] Tambahkan kredensial berikut ke file .env:")
            print("     SHOPEE_PARTNER_ID=123456")
            print("     SHOPEE_PARTNER_KEY=your_partner_key")
            print("     SHOPEE_SHOP_ID=987654")
            print("     SHOPEE_ACCESS_TOKEN=your_access_token")
            return None

        path = "/api/v2/product/boost_item"
        timestamp = int(time.time())
        sign = self._generate_sign(path, timestamp)

        url = f"{self.host}{path}?partner_id={self.partner_id}&timestamp={timestamp}&sign={sign}&access_token={self.access_token}&shop_id={self.shop_id}"
        
        payload = {
            "item_id_list": item_ids[:5]  # Limit 5 items max according to Shopee rules
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )

        try:
            with urllib.request.urlopen(req) as response:
                res = json.loads(response.read().decode('utf-8'))
                if res.get('error') == '':
                    print(f"[✅] Berhasil menaikkan {len(item_ids)} produk via Shopee API!")
                    print("     Detail:", res.get('response', {}))
                    return res
                else:
                    print(f"[-] Gagal menaikkan produk: {res.get('message')} (Error Code: {res.get('error')})")
                    return res
        except Exception as e:
            print(f"[-] Terjadi kesalahan koneksi API Shopee: {str(e)}")
            return None

if __name__ == '__main__':
    print("=== 🚀 Shopee Open API Auto-Boost ('Naikkan Produk') ===")
    api = ShopeeBoostAPI()
    # Contoh item ID produk winning (ganti sesuai item ID di Shopee Seller Centre)
    sample_item_ids = [1000000001, 1000000002, 1000000003]
    api.boost_items(sample_item_ids)
