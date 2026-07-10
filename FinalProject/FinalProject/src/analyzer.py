import os
import re
from collections import Counter

import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

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
    print(section_quantity)
    return section_quantity
#Q2
def section_with_longest_count():
    longest_section = df.loc[df["word_count"].idxmax()]
    print(longest_section)
    return longest_section
#Q3
def section_with_most_code_examples():
    most_code_section = df.loc[df["code_block_count"].idxmax()]
    print(most_code_section)
    return most_code_section
#Q4
def section_contains_most_links():
    most_links_section = df.loc[df["link_count"].idxmax()]
    print(most_links_section)
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
    print(top_ten)
    return top_ten
#Q6
def count_internal_and_external_links():
    internal_links = (df2["link_type"] == "internal_anchor").sum()
    external_links = (df2["link_type"] == "external_link").sum()

    print(internal_links)
    print(external_links)
    return internal_links, external_links
#Q7
def count_find_all():
    count = df3["contains_find_all"].sum()
    print(count)
    return count
#Q8
def count_get_text():
    count = df3["contains_get_text"].sum()
    print(count)
    return count
  
#2 additions
#Q9. What is the average, minimum, maximum, and standard deviation of section word counts?
def word_count_statistics():
    words = df["word_count"].to_numpy()

    average = np.mean(words)
    minimum = np.min(words)
    maximum = np.max(words)
    std_dev = np.std(words)

    print("Average:", average)
    print("Minimum:", minimum)
    print("Maximum:", maximum)
    print("Standard deviation:", std_dev)
    return average, minimum, maximum, std_dev

#Q10. Which sections are longer than the average section?
def sections_above_average():
    avg = np.mean(df["word_count"])

    result = df[df["word_count"] > avg]

    print(result[["section_title", "word_count"]])
    return result[["section_title", "word_count"]]


# if __name__ == "__main__":
#     load_data()

#     sections_count()
#     section_with_longest_count()
#     section_with_most_code_examples()
#     section_contains_most_links()
#     top_ten_technical_keyword()
#     count_internal_and_external_links()
#     count_find_all()
#     count_get_text()
#     word_count_statistics()
#     sections_above_average()
