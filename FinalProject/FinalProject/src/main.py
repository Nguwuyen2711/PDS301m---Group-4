from pathlib import Path

from collector import download_documentation
from parser import parse_html
from Extractor import (
    export_links_to_csv,
    export_sections_to_csv,
    extract_link_rows,
    extract_links,
    extract_sections,
    extract_python_code,
    export_examples_to_csv
)

download_documentation()

soup = parse_html()
sections = extract_sections(soup)
links = extract_links(soup)
link_rows = extract_link_rows(soup)

#function 5
python_code = extract_python_code(soup)

output_dir = Path("FinalProject/FinalProject/data/processed")
output_dir.mkdir(parents=True, exist_ok=True)

export_sections_to_csv(sections, output_dir / "sections.csv")
export_links_to_csv(link_rows, output_dir / "links.csv")

#function 5
export_examples_to_csv(python_code, output_dir / "code_examples.csv")

print(f"\nExtracted {len(sections)} sections and {len(links)} links.")
print("Sample sections:")
for section in sections[:5]:
    print(f"- {section['section_title']}")
print(f"Saved processed outputs to: {output_dir}")

print("\nFeatures 1, 2, 3, and 4 completed successfully.")