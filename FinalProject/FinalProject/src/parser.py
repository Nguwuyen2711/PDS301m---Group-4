from bs4 import BeautifulSoup


HTML_PATH = "data/raw/beautifulsoup_doc.html"


def parse_html():

    print("\n" + "=" * 50)
    print("FEATURE 2 - HTML PARSER")
    print("=" * 50)

    with open(HTML_PATH, "r", encoding="utf-8") as file:

        html = file.read()

    soup = BeautifulSoup(html, "html.parser")

    print("HTML parsed successfully.")

    return soup