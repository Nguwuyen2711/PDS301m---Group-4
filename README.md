# PDS301m---Group-4
Final Project 
# BeautifulSoup Documentation Analytics

## Project Overview

This project collects and analyzes the official Beautiful Soup documentation using Python.

The system downloads the documentation webpage, parses the HTML, extracts useful information, performs data analysis using Pandas and NumPy, generates charts using Matplotlib, and produces a final analytical report.


## Team Members

- Lê Vương Khải Hoàn
- Thái Anh Minh
- Phan Phúc Nguyên
- Nguyễn Hữu Lê Duy

---

## Technologies Used

- Python 
- Requests
- BeautifulSoup4
- Pandas
- NumPy
- Matplotlib

---

## Features

### Feature 1 – Web Page Collector

- Downloads the Beautiful Soup documentation.
- Saves the raw HTML into `data/raw/beautifulsoup_doc.html`.

### Feature 2 – HTML Parser

- Parses the downloaded HTML using BeautifulSoup.

### Feature 3 – Section Extractor

- Extracts all documentation sections.
- Generates `sections.csv`.

### Feature 4 – Link Extractor

- Extracts and classifies hyperlinks.
- Generates `links.csv`.

### Feature 5 – Code Example Extractor

- Extracts Python code examples.
- Generates `code_examples.csv`.

### Feature 6 – Documentation Analytics

Answers analytical questions using Pandas and NumPy.

### Feature 7 – Data Visualization

Generates charts summarizing the extracted data.

### Feature 8 – Final Report Generator

Produces the final analytical report.

---

## Output Files

### Raw Data

- `data/raw/beautifulsoup_doc.html`

### Processed Data

- `sections.csv`
- `links.csv`
- `code_examples.csv`

### Analysis

- `analysis_report.csv`

### Charts

- Top 10 Sections by Word Count
- Code Examples by Section
- Link Type Distribution
- Code Example Line Count Distribution

### Final Report

- `final_report.pdf`

---

## Data Source

Official Beautiful Soup Documentation

https://www.crummy.com/software/BeautifulSoup/bs4/doc/

---

## License

This project is developed for educational purposes as part of the PDS301 course.