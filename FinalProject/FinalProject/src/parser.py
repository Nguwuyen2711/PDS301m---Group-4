from bs4 import BeautifulSoup

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

HTML_PATH = RAW_DIR / "beautifulsoup_doc.html"

def _read_html_text(path):
    with open(path, "rb") as file:
        raw_bytes = file.read()

    try:
        return raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return raw_bytes.decode("latin-1")

def parse_html(verbose=True):
    if verbose:
        print("\n" + "=" * 50)
        print("FEATURE 2 - HTML PARSER")
        print("=" * 50)

    html = _read_html_text(HTML_PATH)

    soup = BeautifulSoup(html, "html.parser")

    if verbose:
        print("HTML parsed successfully.")

    return soup