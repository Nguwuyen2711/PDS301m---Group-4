from .collector import download_documentation
from .parser import parse_html as parse_html_document
from .extractor import (
    export_links_to_csv,
    export_sections_to_csv,
    extract_link_rows,
    extract_links,
    extract_sections,
    extract_python_code,
    export_examples_to_csv,
)

soup = None
sections = None
links = None
link_rows = None
python_code = None

def download_html():
    download_documentation()

def _ensure_parsed(verbose):
    global soup, sections, links, link_rows, python_code

    if soup is None:
        soup = parse_html_document(verbose)
        sections = extract_sections(soup)
        links = extract_links(soup)
        link_rows = extract_link_rows(soup)
        python_code = extract_python_code(soup)

    return soup

def parse_html(verbose):
    return _ensure_parsed(verbose)

def sections_to_csv():
    _ensure_parsed(False)
    export_sections_to_csv(sections, "sections.csv")

def links_to_csv():
    _ensure_parsed(False)
    export_links_to_csv(link_rows, "links.csv")

def code_samples_to_csv():
    _ensure_parsed(False)
    export_examples_to_csv(python_code, "code_examples.csv")