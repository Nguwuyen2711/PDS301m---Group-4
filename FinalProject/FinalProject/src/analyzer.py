import os
from pathlib import Path
import re
from collections import Counter

import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXCEL_OUTPUT_DIR = PROJECT_ROOT / "output" 
os.makedirs(EXCEL_OUTPUT_DIR, exist_ok=True)

STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "is", "are", "was", "were", "be",
    "been", "being", "to", "of", "in", "on", "at", "by", "for", "with",
    "about", "as", "into", "this", "that", "these", "those", "it", "its",
    "you", "your", "we", "our", "can", "will", "not", "no", "do", "does",
    "did", "has", "have", "had", "so", "than", "then", "if", "from", "up",
    "down", "out", "over", "when", "which", "who", "what", "how", "all",
    "any", "each", "other", "some", "such", "only", "also", "just", "more",
    "most", "used", "use", "using",
}


def load_data():
    global df, df2, df3
    df = pd.read_csv(os.path.join(PROCESSED_DIR, "sections.csv"), keep_default_na=False)
    df2 = pd.read_csv(os.path.join(PROCESSED_DIR, "links.csv"), keep_default_na=False)
    df3 = pd.read_csv(os.path.join(PROCESSED_DIR, "code_examples.csv"), keep_default_na=False)

    df = df.drop_duplicates()
    df2 = df2.drop_duplicates()
    df3 = df3.drop_duplicates()


#how many sections
#Q1
def sections_count():
    section_quantity = df["section_id"].count()
    return section_quantity
#Q2
def section_with_longest_count():
    longest_section = df.loc[df["word_count"].idxmax()]
    return longest_section
#Q3
def section_with_most_code_examples():
    most_code_section = df.loc[df["code_block_count"].idxmax()]
    return most_code_section
#Q4
def section_contains_most_links():
    most_links_section = df.loc[df["link_count"].idxmax()]
    return most_links_section
#Q5
def top_ten_technical_keyword():
    word_count = Counter()
    for text in df["section_text"]:
        words = re.findall(r"[a-z]+", text.lower())
        for word in words:
            if len(word) > 2 and word not in STOPWORDS:
                word_count[word] += 1

    top_ten = word_count.most_common(10)
    return top_ten
#Q6
def count_internal_and_external_links():
    internal_links = (df2["link_type"] == "internal_anchor").sum()
    external_links = (df2["link_type"] == "external_link").sum()

    return internal_links, external_links
#Q7
def count_find_all():
    count = df3["contains_find_all"].sum()
    return count
#Q8
def count_get_text():
    count = df3["contains_get_text"].sum()
    return count
  
#2 additions
#Q9. What is the average, minimum, maximum, and standard deviation of section word counts?
def word_count_statistics():
    words = df["word_count"].to_numpy()

    average = np.mean(words)
    minimum = np.min(words)
    maximum = np.max(words)
    std_dev = np.std(words)

    return average, minimum, maximum, std_dev

#Q10. Which sections are longer than the average section?
def sections_above_average():
    avg = np.mean(df["word_count"])

    result = df[df["word_count"] > avg]

    return result[["section_title", "word_count"]]

def export_to_excel():
    output_dir = EXCEL_OUTPUT_DIR
    output_file = output_dir / "analysis_results.xlsx"

    q1 = pd.DataFrame({
        "section_count": [sections_count()]
    })

    q2 = section_with_longest_count().to_frame().T
    q3 = section_with_most_code_examples().to_frame().T
    q4 = section_contains_most_links().to_frame().T

    q5 = pd.DataFrame(
        top_ten_technical_keyword(),
        columns=["keyword", "frequency"]
    )

    internal_links, external_links = count_internal_and_external_links()

    q6 = pd.DataFrame({
        "link_type": ["Internal", "External"],
        "count": [internal_links, external_links]
    })

    q7 = pd.DataFrame({
        "contains_find_all_count": [count_find_all()]
    })

    q8 = pd.DataFrame({
        "contains_get_text_count": [count_get_text()]
    })

    average, minimum, maximum, std_dev = word_count_statistics()

    q9 = pd.DataFrame({
        "statistic": [
            "Average",
            "Minimum",
            "Maximum",
            "Standard Deviation"
        ],
        "value": [
            average,
            minimum,
            maximum,
            std_dev
        ]
    })

    q10 = sections_above_average()

    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        q1.to_excel(writer, sheet_name="Q1 Section Count", index=False)
        q2.to_excel(writer, sheet_name="Q2 Longest Section", index=False)
        q3.to_excel(writer, sheet_name="Q3 Most Code", index=False)
        q4.to_excel(writer, sheet_name="Q4 Most Links", index=False)
        q5.to_excel(writer, sheet_name="Q5 Top Keywords", index=False)
        q6.to_excel(writer, sheet_name="Q6 Link Counts", index=False)
        q7.to_excel(writer, sheet_name="Q7 Find All", index=False)
        q8.to_excel(writer, sheet_name="Q8 Get Text", index=False)
        q9.to_excel(writer, sheet_name="Q9 Word Statistics", index=False)
        q10.to_excel(writer, sheet_name="Q10 Above Average", index=False)

    print(f"Excel file exported successfully: {output_file}")
   
if __name__ == "__main__":
    load_data()
    export_to_excel()
    sections_count()
    section_with_longest_count()
    section_with_most_code_examples()
    section_contains_most_links()
    top_ten_technical_keyword()
    count_internal_and_external_links()
    count_find_all()
    count_get_text()
    word_count_statistics()
    sections_above_average()