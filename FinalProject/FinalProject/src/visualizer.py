import os
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path

BASE_DIR = None
INPUT_DIR = None
OUTPUT_DIR = None

sections = None
links = None
code = None

def initializer():
    global BASE_DIR, INPUT_DIR, OUTPUT_DIR, sections, links, code
    BASE_DIR = Path(__file__).resolve().parent.parent
    INPUT_DIR = BASE_DIR / "data" / "processed"
    OUTPUT_DIR = BASE_DIR / "output" / "charts"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    sections = pd.read_csv(INPUT_DIR / "sections.csv")
    links = pd.read_csv(INPUT_DIR / "links.csv")
    code = pd.read_csv(INPUT_DIR / "code_examples.csv")

def chart_top10_sections():
    top10 = sections.sort_values(by="word_count",ascending=False).head(10)

    plt.figure(figsize=(12,6))

    plt.bar(top10["section_title"], top10["word_count"])

    plt.title("Top 10 Sections by Word Count")
    plt.xlabel("Section")
    plt.ylabel("Words")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    plt.savefig(f"{OUTPUT_DIR}/top10_sections.png")
    plt.show()

def chart_code_examples():
    counts = code.groupby("section_title").size()

    plt.figure(figsize=(60,8))

    plt.bar(counts.index, counts.values)

    plt.title("Code Examples by Section")
    plt.xlabel("Section")
    plt.ylabel("Examples")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    plt.savefig(f"{OUTPUT_DIR}/code_examples_by_section.png")
    plt.show()

def chart_link_distribution():
    types = links["link_type"].value_counts()
    plt.figure(figsize=(7,7))
    wedges, texts, autotexts = plt.pie(
        types,
        autopct=lambda p: f"{p:.1f}%" if p >= 1 else "",
        startangle=90
    )

    plt.legend(
        wedges,
        ["Internal", "External", "Documentation"],
        title="Link Type",
        loc="center left",
        bbox_to_anchor=(1, 0.5)
    )

    plt.tight_layout()
    plt.title("Link Type Distribution")

    plt.savefig(f"{OUTPUT_DIR}/link_distribution.png")
    plt.show()

def chart_code_length_histogram():
    plt.figure(figsize=(10,15))

    plt.hist(
        code["line_count"],
        bins=20
    )

    plt.title("Distribution of Code Example Lengths")
    plt.xlabel("Lines")
    plt.ylabel("Frequency")

    plt.tight_layout()

    plt.savefig(f"{OUTPUT_DIR}/code_length_histogram.png")
    plt.show()

if __name__ == "__main__":
    initializer()
    chart_top10_sections()
    chart_code_examples()
    chart_link_distribution()
    chart_code_length_histogram()