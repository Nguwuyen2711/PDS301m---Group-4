from pathlib import Path

import pandas as pd
from pandas.api.types import is_object_dtype, is_string_dtype
from bs4 import BeautifulSoup

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "processed" 
RAW_DIR.mkdir(parents=True, exist_ok=True)

def _normalize_text(value):
    text = value
    if value is None:
        return ""
    if isinstance(value, str):
        if "Â" in text or "â" in text:
            try:
                text = text.encode("latin-1").decode("utf-8")
            except UnicodeError:
                pass
        return text.replace("Â¶", "").replace("â¶", "").replace("¶", "").strip()
    else:
        text = str(value).replace("¶", "").strip()
    return text


def _ensure_soup(html_or_soup):
    if isinstance(html_or_soup, BeautifulSoup):
        return html_or_soup

    if isinstance(html_or_soup, str):
        return BeautifulSoup(html_or_soup, "html.parser")

    if html_or_soup is None:
        raise ValueError("No HTML content provided.")

    raise TypeError("Expected a string or BeautifulSoup object.")


def extract_sections(html_or_soup):
    # Extract meaningful sections from HTML content.
    soup = _ensure_soup(html_or_soup)
    sections = []

    for section in soup.find_all("section"):
        title = None
        section_level = None

        for heading in section.find_all(["h1", "h2", "h3", "h4", "h5", "h6"], recursive=True):
            text = heading.get_text(" ", strip=True)
            if text:
                title = text
                section_level = int(heading.name[1])
                break

        section_copy = BeautifulSoup(str(section), "html.parser")
        for heading in section_copy.find_all(["h1", "h2", "h3", "h4", "h5", "h6"], recursive=True):
            heading.decompose()

        content = section_copy.get_text(" ", strip=True)
        if content:
            sections.append(
                {
                    "section_id": section.get("id") or "",
                    "section_level": section_level or 0,
                    "section_title": title or "Untitled section",
                    "section_text": content,
                    "word_count": len(content.split()),
                    "code_block_count": len(section_copy.find_all("code")) + len(section_copy.find_all("pre")),
                    "link_count": len(section_copy.find_all("a")),
                }
            )

    return sections


def extract_links(html_or_soup):
    # Extract all hyperlink targets from HTML content.
    soup = _ensure_soup(html_or_soup)
    links = []

    for anchor in soup.find_all("a"):
        href = anchor.get("href")
        if href:
            links.append(href)

    return links


def extract_link_rows(html_or_soup):
    # Extract hyperlink rows with link text, href, type, and containing section title.
    soup = _ensure_soup(html_or_soup)
    rows = []

    for anchor in soup.find_all("a"):
        href = anchor.get("href")
        if not href:
            link_type = "empty_or_invalid"
        elif href.startswith("#"):
            link_type = "internal_anchor"
        elif href.startswith("http") or href.startswith("https"):
            link_type = "external_link"
        elif href.startswith("/") or href.startswith("./") or href.startswith("../"):
            link_type = "documentation_link"
        elif anchor.find("img") is not None:
            link_type = "image_link"
        else:
            link_type = "documentation_link"

        section = anchor.find_parent("section")
        section_title = ""
        if section is not None:
            heading = section.find(["h1", "h2", "h3", "h4", "h5", "h6"])
            if heading is not None:
                section_title = heading.get_text(" ", strip=True)

        rows.append(
            {
                "link_text": anchor.get_text(" ", strip=True),
                "href": href,
                "link_type": link_type,
                "section_title": section_title,
            }
        )

    return rows


def export_sections_to_csv(sections, filename):
    # Write extracted sections to a CSV file with the required schema.

    df = pd.DataFrame(sections)
    for column in df.columns:
        if is_object_dtype(df[column]) or is_string_dtype(df[column]):
            df[column] = df[column].apply(_normalize_text)
    expected_columns = [
        "section_id",
        "section_level",
        "section_title",
        "section_text",
        "word_count",
        "code_block_count",
        "link_count",
    ]
    for column in expected_columns:
        if column not in df.columns:
            df[column] = ""
    df = df[expected_columns]
    output_path = RAW_DIR / filename
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"File written to {output_path}")


def export_links_to_csv(link_rows, filename):
    # Write extracted links to a CSV file with the required schema.

    df = pd.DataFrame(link_rows)

    for column in df.columns:
        if is_object_dtype(df[column]) or is_string_dtype(df[column]):
            df[column] = df[column].apply(_normalize_text)
            
    expected_columns = ["link_text", "href", "link_type", "section_title"]
    for column in expected_columns:
        if column not in df.columns:
            df[column] = ""
    df = df[expected_columns]
    output_path = RAW_DIR / filename
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"File written to {output_path}")

def extract_python_code(html_or_soup):
    soup = _ensure_soup(html_or_soup)
    python_code = []
    example_id = 0

    for pre in soup.find_all("pre"):
        code = pre.get_text().strip()

        if not code:
            continue

        example_id += 1
        section = pre.find_parent("section")
        section_title = ""
        if section:
            heading = section.find(["h1", "h2", "h3", "h4", "h5", "h6"])
            if heading:
                section_title = heading.get_text(" ", strip=True)
        python_code.append({
            "example_id": example_id,
            "section_title": section_title,
            "code_text": code, 
            "line_count": len(code.splitlines()), 
            "contains_find_all": "find_all(" in code, 
            "contains_find": "find(" in code, 
            "contains_select": "select(" in code, 
            "contains_get_text": "get_text(" in code, 
             "contains_requests": "requests" in code, })
    return python_code

def export_examples_to_csv(sections, filename):
    # Write examples sections to a CSV file with the required schema.

    df = pd.DataFrame(sections)
    for column in df.columns:
        if is_object_dtype(df[column]) or is_string_dtype(df[column]):
            df[column] = df[column].apply(_normalize_text)
    expected_columns = [
        "example_id",
        "section_title",
        "code_text",
        "line_count",
        "contains_find_all",
        "contains_find",
        "contains_select",
        "contains_get_text",
        "contains_requests"
    ]
    for column in expected_columns:
        if column not in df.columns:
            df[column] = ""
    df = df[expected_columns]
    output_path = RAW_DIR / filename
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"File written to {output_path}")
