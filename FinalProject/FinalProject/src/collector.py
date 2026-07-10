import os
import requests
from pathlib import Path

URL = "https://www.crummy.com/software/BeautifulSoup/bs4/doc/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

HTML_PATH = RAW_DIR / "beautifulsoup_doc.html"

def download_documentation():

    os.makedirs("data/raw", exist_ok=True)

    print("=" * 50)
    print("FEATURE 1 - WEB PAGE COLLECTOR")
    print("=" * 50)

    try:

        response = requests.get(URL)

        print("HTTP Status Code:", response.status_code)

        if response.status_code == 200:
            response.encoding = response.apparent_encoding or "utf-8"
            content = response.text

            with open(HTML_PATH, "w", encoding="utf-8") as file:
                file.write(content)

            print("Download completed.")
            print("Saved to:", HTML_PATH)

        else:

            print("Download failed.")

    except Exception as error:

        print("Error:", error)