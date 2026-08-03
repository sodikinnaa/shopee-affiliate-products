import os
import json
import requests

def load_env_file():
    if os.path.exists(".env"):
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    key = k.strip()
                    val = v.strip().strip('"').strip("'")
                    if val and not os.environ.get(key):
                        os.environ[key] = val

def upload_meta_ads():
    load_env_file()

    META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN") or os.getenv("THREADS_ACCESS_TOKEN", "")
    META_AD_ACCOUNT_ID = os.getenv("META_AD_ACCOUNT_ID", "")
    META_PAGE_ID = os.getenv("META_PAGE_ID", "")

    print("==================================================")
    print("🚀 META ADS AUTOMATED API UPLOADER (PAUSED MODE)")
    print("==================================================")

    if not os.path.exists("meta_ads_queue.json"):
        print("[-] File 'meta_ads_queue.json' tidak ditemukan. Jalankan 'meta_ads_builder.py' terlebih dahulu.")
        return

    with open("meta_ads_queue.json", "r", encoding="utf-8") as f:
        queue = json.load(f)

    if not META_ACCESS_TOKEN or not META_AD_ACCOUNT_ID:
        print("\n[ℹ️] META_ACCESS_TOKEN atau META_AD_ACCOUNT_ID belum diset di file '.env'.")
        print(f"[✅] {len(queue)} materi iklan disiapkan di file lokal:")
        print("     1. 📄 Draf JSON Payload : meta_ads_queue.json")
        print("     2. 📊 Bulk Import CSV  : meta_ads_import.csv")
        return

    ad_account = META_AD_ACCOUNT_ID if META_AD_ACCOUNT_ID.startswith("act_") else f"act_{META_AD_ACCOUNT_ID}"
    API_VERSION = "v19.0"

    print(f"[+] Menghubungkan ke Meta Ads Account: {ad_account}...")
    print(f"[+] Target Meta Page ID: {META_PAGE_ID or 'Auto-detect'}\n")

    # Fetch Page Token if PAGE_ID exists
    page_token = None
    if META_PAGE_ID:
        try:
            r_page = requests.get(f"https://graph.facebook.com/{API_VERSION}/{META_PAGE_ID}?fields=access_token&access_token={META_ACCESS_TOKEN}")
            page_data = r_page.json()
            page_token = page_data.get("access_token")
        except Exception as e:
            print(f"[-] Gagal mengambil Page Token: {e}")

    success_count = 0
    dev_mode_warn = False

    for idx, item in enumerate(queue, start=1):
        pid = item["product_id"]
        campaign_name = item["campaign_name"]
        adset_name = item["adset_name"]
        ad_name = item["ad_name"]
        creative = item["creative"]
        targeting = item["targeting"]

        print(f"--- [{idx}/{len(queue)}] Memproses Produk #{pid}: {creative['headline'][:40]} ---")

        # 1. Create Campaign
        url_camp = f"https://graph.facebook.com/{API_VERSION}/{ad_account}/campaigns"
        camp_payload = {
            "name": campaign_name,
            "objective": "OUTCOME_TRAFFIC",
            "status": "PAUSED",
            "special_ad_categories": "[]",
            "is_adset_budget_sharing_enabled": "false",
            "access_token": META_ACCESS_TOKEN
        }

        try:
            r_camp = requests.post(url_camp, data=camp_payload)
            res_camp = r_camp.json()
            if "id" not in res_camp:
                print(f"   [-] Gagal membuat Campaign: {res_camp.get('error', {}).get('message', res_camp)}")
                continue

            camp_id = res_camp["id"]
            print(f"   [✅] Campaign Dibuat (ID: {camp_id}) [STATUS: PAUSED]")

            # 2. Create AdSet
            url_adset = f"https://graph.facebook.com/{API_VERSION}/{ad_account}/adsets"
            adset_payload = {
                "name": adset_name,
                "campaign_id": camp_id,
                "daily_budget": str(item.get("daily_budget_idr", 25000)),
                "billing_event": "IMPRESSIONS",
                "optimization_goal": "LINK_CLICKS",
                "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
                "destination_type": "WEBSITE",
                "targeting": json.dumps({
                    "geo_locations": {"countries": ["ID"]},
                    "age_min": targeting.get("min_age", 18),
                    "age_max": targeting.get("max_age", 45),
                    "targeting_automation": {"advantage_audience": 0}
                }),
                "status": "PAUSED",
                "access_token": META_ACCESS_TOKEN
            }
            r_adset = requests.post(url_adset, data=adset_payload)
            res_adset = r_adset.json()
            if "id" not in res_adset:
                print(f"   [-] Gagal membuat AdSet: {res_adset.get('error', {}).get('message', res_adset)}")
                continue

            adset_id = res_adset["id"]
            print(f"   [✅] AdSet Dibuat (ID: {adset_id}) [STATUS: PAUSED]")

            # 3. Upload Creative / Post
            creative_id = None
            local_img = creative.get("local_image")

            # Upload Image if local file exists
            img_hash = None
            if local_img and os.path.exists(local_img):
                url_img = f"https://graph.facebook.com/{API_VERSION}/{ad_account}/adimages"
                with open(local_img, "rb") as f:
                    r_img = requests.post(url_img, files={"file": f}, data={"access_token": META_ACCESS_TOKEN})
                    res_img = r_img.json()
                    if "images" in res_img:
                        img_hash = list(res_img["images"].values())[0].get("hash")

            if META_PAGE_ID and page_token:
                url_post = f"https://graph.facebook.com/{API_VERSION}/{META_PAGE_ID}/feed"
                post_payload = {
                    "message": f"{creative['headline']}\n\n{creative['primary_text']}",
                    "link": creative["destination_link"],
                    "access_token": page_token
                }
                r_post = requests.post(url_post, data=post_payload)
                res_post = r_post.json()

                if "id" in res_post:
                    post_id = res_post["id"]
                    url_cr = f"https://graph.facebook.com/{API_VERSION}/{ad_account}/adcreatives"
                    cr_payload = {
                        "name": f"Creative - Product #{pid}",
                        "object_story_id": post_id,
                        "access_token": META_ACCESS_TOKEN
                    }
                    r_cr = requests.post(url_cr, data=cr_payload)
                    res_cr = r_cr.json()
                    if "id" in res_cr:
                        creative_id = res_cr["id"]
                    elif res_cr.get("error", {}).get("error_subcode") == 1885183:
                        dev_mode_warn = True

            # 4. Create Ad if creative_id obtained
            if creative_id:
                url_ad = f"https://graph.facebook.com/{API_VERSION}/{ad_account}/ads"
                ad_payload = {
                    "name": ad_name,
                    "adset_id": adset_id,
                    "creative": json.dumps({"creative_id": creative_id}),
                    "status": "PAUSED",
                    "access_token": META_ACCESS_TOKEN
                }
                r_ad = requests.post(url_ad, data=ad_payload)
                res_ad = r_ad.json()
                if "id" in res_ad:
                    print(f"   [✅] Ad Creative & Ad Dibuat (ID: {res_ad['id']}) [STATUS: PAUSED]\n")
                    success_count += 1
                else:
                    print(f"   [ℹ️] Campaign & AdSet berhasil di-upload. Ad creation status: {res_ad.get('error', {}).get('message')}\n")
            else:
                print(f"   [ℹ️] Campaign & AdSet berhasil di-upload ke Meta Ads (Status: PAUSED).\n")
                success_count += 1

        except Exception as e:
            print(f"   [-] Error saat memproses produk #{pid}: {e}\n")

    print("==================================================")
    print(f"🎉 SUKSES! Total {success_count}/{len(queue)} Campaign & AdSets berhasil di-upload ke Meta Ads via API.")
    print("📌 SEMUA CAMPAIGN TERPASANG DALAM STATUS 'PAUSED' (DRAFT / TIDAK AKAN JALAN SEBELUM DI-PUBLISH MANUALLY).")
    print("==================================================")

    if dev_mode_warn:
        print("\n💡 NOTE META API DEVELOPMENT MODE:")
        print("   - Meta App Anda saat ini berada di status 'Development Mode'.")
        print("   - Campaign & Ad Set telah BERHASIL dibuat secara otomatis via API di Meta Ads Manager.")
        print("   - Untuk otomatisasi Ad Creative via API, ubah App Mode ke 'Live' di https://developers.facebook.com, atau gunakan Opsi Import CSV 'meta_ads_import.csv' di Meta Ads Manager.")

if __name__ == "__main__":
    upload_meta_ads()
