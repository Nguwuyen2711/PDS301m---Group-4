import os
import pandas as pd
import matplotlib.pyplot as plt

OUTPUT_DIR = "FinalProject/FinalProject/output/charts"
INPUT_DIR = "FinalProject/FinalProject/data/processed"
os.makedirs(OUTPUT_DIR, exist_ok=True)

sections = pd.read_csv(os.path.join(INPUT_DIR, "sections.csv"))
links = pd.read_csv(os.path.join(INPUT_DIR, "links.csv"))
code = pd.read_csv(os.path.join(INPUT_DIR, "code_examples.csv"))

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
    plt.close()

def chart_code_examples():
    counts = code.groupby("section_title").size()

    plt.figure(figsize=(40,6))

    plt.bar(counts.index, counts.values)

    plt.title("Code Examples by Section")
    plt.xlabel("Section")
    plt.ylabel("Examples")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    plt.savefig(f"{OUTPUT_DIR}/code_examples_by_section.png")
    plt.close()

def chart_link_distribution():
    types = links["link_type"].value_counts()

    plt.figure(figsize=(7,7))

    plt.pie(
        types,
        labels=types.index,
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title("Link Type Distribution")

    plt.savefig(f"{OUTPUT_DIR}/link_distribution.png")
    plt.close()

def chart_code_length_histogram():
    plt.figure(figsize=(10,6))

    plt.hist(
        code["line_count"],
        bins=20
    )

    plt.title("Distribution of Code Example Lengths")
    plt.xlabel("Lines")
    plt.ylabel("Frequency")

    plt.tight_layout()

    plt.savefig(f"{OUTPUT_DIR}/code_length_histogram.png")
    plt.close()

if __name__ == "__main__":
    chart_top10_sections()
    chart_code_examples()
    chart_link_distribution()
    chart_code_length_histogram()