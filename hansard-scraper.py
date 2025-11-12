import requests
import os
import time
import urllib3

from datetime import date, timedelta

# Disable SSL warnings (safe here since we're downloading public PDFs)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

base_url = "https://www.parlimen.gov.my/files/hindex/pdf"
output_dir = "hansard_pdfs"

start_date = date(1959, 11, 9)
end_date = date(2025, 8, 30)

# === Setup ===
os.makedirs(output_dir, exist_ok=True)
session = requests.Session()
session.headers.update({
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.parlimen.gov.my/hansard-dewan-rakyat.html",
})

# === Loop through each date ===
current = start_date
while current <= end_date:
    filename = f"DR-{current.strftime('%d%m%Y')}.pdf"
    url = f"{base_url}/{filename}"
    local_path = os.path.join(output_dir, filename)

    print(f"Checking {filename}...", end=" ")

    try:
        # HEAD may fail on some servers, so we skip directly to GET
        response = session.get(url, verify=False, timeout=30)
        if response.status_code == 200 and response.headers.get("content-type", "").startswith("application/pdf"):
            with open(local_path, "wb") as f:
                f.write(response.content)
            print("downloaded ✅")
        else:
            print(f"not found ({response.status_code})")
    except requests.RequestException as e:
        print(f"error: {e}")

    current += timedelta(days=1)
    time.sleep(0.5)  # be polite to the server

print("\n✅ Done! PDFs saved in:", os.path.abspath(output_dir))