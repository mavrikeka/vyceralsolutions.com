#!/usr/bin/env python3
"""
Create a mapping of article slugs to raw HTML files.
"""

import json
from pathlib import Path
import re

# Load article metadata
with open('blog/converted-articles.json', 'r') as f:
    articles = json.load(f)

# Get all raw files
raw_path = Path('blog/articles-raw')
raw_files = list(raw_path.glob('*.html'))

# Create mapping
mapping = {}

for article in articles:
    slug = article['slug']
    title = article['title'].lower()

    # Remove common words for better matching
    title_words = title.replace(' - ', ' ').replace(': ', ' ').split()
    title_words = [w for w in title_words if w not in ['a', 'the', 'and', 'or', 'in', 'on', 'with', 'for', 'to', 'of', 'is', 'it', 'that', 'this']]

    best_match = None
    best_score = 0

    for raw_file in raw_files:
        filename = raw_file.stem.lower()

        # Count matching words
        score = sum(1 for word in title_words if len(word) > 3 and word in filename)

        if score > best_score:
            best_score = score
            best_match = raw_file.name

    if best_match and best_score >= 3:  # At least 3 matching words
        mapping[slug] = best_match
        print(f"✓ {slug} -> {best_match} (score: {best_score})")
    else:
        print(f"⚠️  No match for: {slug} (best score: {best_score})")

# Save mapping
with open('blog/article_raw_mapping.json', 'w') as f:
    json.dump(mapping, f, indent=2)

print(f"\n{'='*60}")
print(f"Mapped: {len(mapping)}/{len(articles)}")
print(f"{'='*60}")
