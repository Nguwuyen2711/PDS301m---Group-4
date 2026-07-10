from .collector import download_documentation
from .parser import parse_html
from .extractor import (
    export_links_to_csv,
    export_sections_to_csv,
    extract_link_rows,
    extract_links,
    extract_sections,
    extract_python_code,
    export_examples_to_csv
)

# Feature 1
def download_html():
    download_documentation()
    print

# Feature 2
def html_parser():
    soup = parse_html()
    return soup

soup = html_parser()
sections = extract_sections(soup)
links = extract_links(soup)
link_rows = extract_link_rows(soup)

#function 5
python_code = extract_python_code(soup)

def sections_to_csv():
    export_sections_to_csv(sections, "sections.csv")

def links_to_csv():
    export_links_to_csv(link_rows, "links.csv")

#function 5
def code_samples_to_csv():
    export_examples_to_csv(python_code, "code_examples.csv")