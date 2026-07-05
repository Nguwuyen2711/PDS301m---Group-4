from collector import download_documentation
from parser import parse_html

download_documentation()

soup = parse_html()

print("\nFeatures 1 and 2 completed successfully.")