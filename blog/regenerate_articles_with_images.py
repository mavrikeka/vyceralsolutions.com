#!/usr/bin/env python3
"""
Regenerate all blog articles using the template with hero images.
"""

import json
import re
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime

# Load article metadata
with open('blog/converted-articles.json', 'r') as f:
    articles = json.load(f)

# Load template
with open('blog/article-template.html', 'r') as f:
    template = f.read()

def extract_content_from_raw(raw_file_path):
    """Extract article content from raw HTML file."""
    with open(raw_file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Find the main article content
    article = soup.find('article')
    if not article:
        # Try finding div with class containing 'article' or 'content'
        article = soup.find('div', class_=re.compile(r'(article|content|post)', re.I))

    if article:
        return str(article)

    # Fallback: return body content
    body = soup.find('body')
    if body:
        return str(body)

    return html

def generate_article(article_data):
    """Generate an article HTML file from template and data."""

    # Get the raw file path
    raw_path = Path('blog/articles-raw')

    # Try multiple matching strategies
    # 1. Try exact slug match
    raw_files = list(raw_path.glob(f"*{article_data['slug']}*.html"))

    # 2. Try simplified slug (remove common words)
    if not raw_files:
        simplified = article_data['slug'].replace('-in-', '-').replace('-and-', '-').replace('-with-', '-').replace('-the-', '-').replace('-a-', '-').replace('-for-', '-')
        raw_files = list(raw_path.glob(f"*{simplified}*.html"))

    # 3. Try even more simplified (first few words)
    if not raw_files:
        words = article_data['slug'].split('-')[:5]
        pattern = '*' + '*'.join(words) + '*.html'
        raw_files = list(raw_path.glob(pattern))

    if not raw_files:
        print(f"⚠️  No raw file found for: {article_data['slug']}")
        return False

    raw_file = raw_files[0]

    # Extract content
    content = extract_content_from_raw(raw_file)

    # Format date
    date_obj = datetime.fromisoformat(article_data['date'])
    formatted_date = date_obj.strftime('%B %d, %Y')

    # Replace template variables
    html = template
    html = html.replace('{{TITLE}}', article_data['title'])
    html = html.replace('{{SLUG}}', article_data['slug'])
    html = html.replace('{{CATEGORY}}', article_data['category_name'])
    html = html.replace('{{CATEGORY_SLUG}}', article_data['category'])
    html = html.replace('{{DATE}}', formatted_date)
    html = html.replace('{{READ_TIME}}', str(article_data['read_time']))
    html = html.replace('{{CONTENT}}', content)

    # Write to file
    output_path = Path(article_data['path'])
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    return True

# Process all articles
success_count = 0
fail_count = 0

for article in articles:
    if generate_article(article):
        success_count += 1
        print(f"✓ Generated: {article['path']}")
    else:
        fail_count += 1

print(f"\n{'='*60}")
print(f"Articles regenerated: {success_count}")
print(f"Failed: {fail_count}")
print(f"Total: {len(articles)}")
print(f"{'='*60}")
