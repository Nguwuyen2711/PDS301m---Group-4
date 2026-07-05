import os
import requests


URL = "https://www.crummy.com/software/BeautifulSoup/bs4/doc/"

SAVE_PATH = "data/raw/beautifulsoup_doc.html"


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

            with open(SAVE_PATH, "w", encoding="utf-8") as file:
                file.write(content)

            print("Download completed.")
            print("Saved to:", SAVE_PATH)

        else:

            print("Download failed.")

    except Exception as error:

        print("Error:", error)