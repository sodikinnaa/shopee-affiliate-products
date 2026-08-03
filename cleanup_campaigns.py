import os
import requests

META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN", "EAA9IEfwzHwUBSGU5fOZCBaEURO6ZB2wVZB34Ypil2gElvRJSe3LtqOtba0khxr2zPmS6mULGSDRccvd0wvQMWQCSCA4dvHAJfwZCYkvg6nKvXTEzOvZBp0qA3xJZAuar0grVT4ny9Ol6lnTleulWV0t7QOUAJ6xpCGg6RZBjoYYtSPnBTzyfu2T8tZBkNnXa")
AD_ACCOUNT = "act_1704618464287234"

KEEP_IDS = {
    "52578456400588", # Product #01 Winning Campaign
    "52578421238788", # Baru Lalu Lintas Kunjungan Kampanye (Manual)
    "52578226832988", # Mempromosikan Wak Dondin (Manual)
    "52571306905788", # Iklan-Ads (Manual)
    "52571309201188", # Testing-adsensess (Manual)
}

url = f"https://graph.facebook.com/v19.0/{AD_ACCOUNT}/campaigns?limit=100&fields=id,name&access_token={META_ACCESS_TOKEN}"
res = requests.get(url).json()

deleted_count = 0
kept_count = 0

for item in res.get("data", []):
    cid = item["id"]
    name = item["name"]
    if cid in KEEP_IDS:
        print(f"[KEEP] Kampanye disimpan: {name} (ID: {cid})")
        kept_count += 1
    else:
        del_url = f"https://graph.facebook.com/v19.0/{cid}?access_token={META_ACCESS_TOKEN}"
        r_del = requests.delete(del_url)
        if r_del.json().get("success"):
            print(f"[DELETED] Kampanye berhasil dihapus: {name} (ID: {cid})")
            deleted_count += 1
        else:
            print(f"[-] Gagal menghapus {name} (ID: {cid}): {r_del.text}")

print(f"\n✅ SELESAI! Dihapus: {deleted_count} Kampanye | Disimpan: {kept_count} Kampanye.")
