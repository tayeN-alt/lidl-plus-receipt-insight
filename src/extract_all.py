import requests
import json
import warnings
import time
warnings.filterwarnings("ignore")

with open("session.json", "r") as f:
    cookies = json.load(f)

auth_token = cookies.get("authToken")
xsrf_token = cookies.get("XSRF-TOKEN")

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "x-xsrf-token": xsrf_token,
    "Authorization": f"Bearer {auth_token}",
}

# Step 1: fetch all receipt IDs
print("Fetching receipt list...")
all_items = []
page = 1

while True:
    response = requests.get(
        f"https://www.lidl.de/mre/api/v1/tickets?country=DE&page={page}",
        headers=headers,
        cookies=cookies
    )
    if response.status_code != 200:
        print(f"  Page {page} failed: {response.status_code}")
        break
    data = response.json()
    items = data.get("items", [])
    total = data.get("totalCount", 0)
    all_items.extend(items)
    print(f"  Page {page}: {len(all_items)}/{total}")
    if len(all_items) >= total or len(items) == 0:
        break
    page += 1
    time.sleep(0.5)

# Step 2: fetch full detail for each receipt
print(f"\nFetching details for {len(all_items)} receipts...")
all_receipts = []

for i, item in enumerate(all_items):
    receipt_id = item["id"]
    url = f"https://www.lidl.de/mre/api/v1/tickets/{receipt_id}?country=DE&languageCode=de-DE"
    r = requests.get(url, headers=headers, cookies=cookies)
    if r.status_code == 200:
        receipt = r.json()
        all_receipts.append(receipt)
        print(f"  [{i+1}/{len(all_items)}] {item['date'][:10]} - €{item['totalAmount']}")
    else:
        print(f"  [{i+1}/{len(all_items)}] FAILED {r.status_code} - {item['date'][:10]}")
    time.sleep(0.3)

with open("lidl_receipts.json", "w", encoding="utf-8") as f:
    json.dump(all_receipts, f, ensure_ascii=False, indent=2)

print(f"\nDone! Saved {len(all_receipts)} receipts to lidl_receipts.json")
