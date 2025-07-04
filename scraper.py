import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import os
from urllib.parse import urljoin, urlparse

BASE_URL = "https://sap.github.io/wdio-qmate-service/doc/"
OUTPUT_DIR = "qmate_docs"
visited = set()

os.makedirs(OUTPUT_DIR, exist_ok=True)

def is_valid_url(href):
    return href and href.startswith("/wdio-qmate-service/doc") and not href.endswith((".js", ".css", ".png", ".svg"))

def fetch_and_save(url):
    if url in visited:
        return
    visited.add(url)
    try:
        print(f"🔍 Fetching {url} ...")
        res = requests.get(url)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        content_div = soup.find("main") or soup.body
        if content_div:
            md_text = md(str(content_div))
            parsed = urlparse(url)
            path = parsed.path.replace("/wdio-qmate-service/doc/", "").strip("/")
            if not path:
                filename = "index.md"
            else:
                filename = path.replace("/", "_") + ".md"
            file_path = os.path.join(OUTPUT_DIR, filename)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(md_text)
            print(f"✅ Saved: {file_path}")
        else:
            print(f"⚠️ No content found in {url}")

        # Recursively follow internal links
        for a in soup.find_all("a"):
            href = a.get("href")
            if is_valid_url(href):
                full_url = urljoin(BASE_URL, href)
                fetch_and_save(full_url)

    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")

# Start scraping from home page
fetch_and_save(BASE_URL)
