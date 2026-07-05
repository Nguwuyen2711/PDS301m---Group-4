from bs4 import BeautifulSoup


HTML_PATH = "data/raw/beautifulsoup_doc.html"


def _read_html_text(path):
    with open(path, "rb") as file:
        raw_bytes = file.read()

    try:
        return raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return raw_bytes.decode("latin-1")


def parse_html():

    print("\n" + "=" * 50)
    print("FEATURE 2 - HTML PARSER")
    print("=" * 50)

    html = _read_html_text(HTML_PATH)

    soup = BeautifulSoup(html, "html.parser")

    print("HTML parsed successfully.")

    return soup