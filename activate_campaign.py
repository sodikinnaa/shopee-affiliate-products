import time
import requests

META_ACCESS_TOKEN = "EAA9IEfwzHwUBSGU5fOZCBaEURO6ZB2wVZB34Ypil2gElvRJSe3LtqOtba0khxr2zPmS6mULGSDRccvd0wvQMWQCSCA4dvHAJfwZCYkvg6nKvXTEzOvZBp0qA3xJZAuar0grVT4ny9Ol6lnTleulWV0t7QOUAJ6xpCGg6RZBjoYYtSPnBTzyfu2T8tZBkNnXa"
CAMPAIGN_ID = "52578456400588"
ADSET_ID = "52578456406388"

print("🚀 ACTIVATING PRODUCT #01 WINNING CAMPAIGN ON META ADS...")

# 1. Update AdSet status and daily budget (15,000 IDR)
for attempt in range(1, 10):
    url_adset = f"https://graph.facebook.com/v19.0/{ADSET_ID}"
    res_adset = requests.post(url_adset, data={
        "status": "ACTIVE",
        "daily_budget": "15000",
        "access_token": META_ACCESS_TOKEN
    }).json()

    if "success" in res_adset or res_adset.get("id"):
        print(f"[✅] AdSet {ADSET_ID} berhasil diaktifkan dengan Budget Rp 15.000/hari!")
        break
    else:
        print(f"[-] Wait API limit (attempt {attempt})... {res_adset}")
        time.sleep(3)

# 2. Update Campaign status to ACTIVE
for attempt in range(1, 10):
    url_camp = f"https://graph.facebook.com/v19.0/{CAMPAIGN_ID}"
    res_camp = requests.post(url_camp, data={
        "status": "ACTIVE",
        "access_token": META_ACCESS_TOKEN
    }).json()

    if "success" in res_camp or res_camp.get("id"):
        print(f"[✅] Campaign Product #01 {CAMPAIGN_ID} BERHASIL DIAKTIFKAN (STATUS: ACTIVE)!")
        break
    else:
        print(f"[-] Wait API limit (attempt {attempt})... {res_camp}")
        time.sleep(3)

print("==================================================")
print("🎉 IKLAN WINNING PRODUCT #01 RESMI BERJALAN LIVE!")
print("==================================================")
