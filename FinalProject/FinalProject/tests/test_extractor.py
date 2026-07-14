import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from extractor import (
    _normalize_text,
    extract_link_rows,
    extract_links,
    extract_sections,
    export_links_to_csv,
    export_sections_to_csv,
)


def test_extract_sections_and_links():
    html = """
    <html>
      <body>
        <h1>Welcome</h1>
        <p>Intro text</p>
        <section id='intro'>
          <h2>Intro</h2>
          <p>Section content</p>
        </section>
        <section id='details'>
          <h2>Details</h2>
          <p>More content</p>
        </section>
        <div>
          <a href='https://example.com'>Example</a>
          <a href='/docs'>Docs</a>
        </div>
      </body>
    </html>
    """

    sections = extract_sections(html)
    links = extract_links(html)

    assert len(sections) == 2
    assert sections[0]["section_title"] == "Intro"
    assert sections[0]["section_text"].strip() == "Section content"
    assert links == ["https://example.com", "/docs"]


def test_normalize_text_decodes_mojibake():
    assert _normalize_text("Beautiful Soup Documentation Â¶") == "Beautiful Soup Documentation"


def test_csv_export_matches_required_columns(tmp_path):
    html = """
    <html>
      <body>
        <section id='intro'>
          <h2>Intro</h2>
          <p>Section content with <a href='#details'>details</a></p>
          <pre><code>print('hi')</code></pre>
        </section>
        <section id='details'>
          <h3>Details</h3>
          <p>More content</p>
          <a href='https://example.com'>Example</a>
        </section>
      </body>
    </html>
    """

    sections = extract_sections(html)
    section_path = tmp_path / "sections.csv"
    export_sections_to_csv(sections, section_path)

    link_rows = extract_link_rows(html)
    link_path = tmp_path / "links.csv"
    export_links_to_csv(link_rows, link_path)

    sections_df = pd.read_csv(section_path)
    links_df = pd.read_csv(link_path)

    assert list(sections_df.columns) == [
        "section_id",
        "section_level",
        "section_title",
        "section_text",
        "word_count",
        "code_block_count",
        "link_count",
    ]
    assert list(links_df.columns) == ["link_text", "href", "link_type", "section_title"]
    assert links_df.loc[0, "link_type"] == "internal_anchor"
    assert links_df.loc[1, "link_type"] == "external_link"
