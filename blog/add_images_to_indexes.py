#!/usr/bin/env python3
"""
Add article images to blog index pages (main blog page and category pages).
"""

import json
from datetime import datetime
from pathlib import Path

# Load article metadata
with open('blog/converted-articles.json', 'r') as f:
    articles = json.load(f)

def format_article_card_with_image(article, is_category_page=False):
    """Generate article card HTML with image."""
    date_val = article.get('date')
    if not date_val:
        print(f"⚠️  No date for article: {article.get('title', 'Unknown')}")
        date_str = "Unknown Date"
    elif isinstance(date_val, str):
        # Handle both 'YYYY-MM-DD HH:MM:SS' and ISO format
        try:
            date_obj = datetime.strptime(date_val, '%Y-%m-%d %H:%M:%S')
            date_str = date_obj.strftime('%B %d, %Y')
        except ValueError:
            print(f"⚠️  Invalid date format for: {article.get('title', 'Unknown')} - {date_val}")
            date_str = "Unknown Date"
    else:
        date_obj = date_val
        date_str = date_obj.strftime('%B %d, %Y')

    # Determine image path based on page location
    if is_category_page:
        image_path = f"../../images/article-images/{article['slug']}.jpg"
        article_path = f"{article['slug']}.html"
    else:
        image_path = f"images/article-images/{article['slug']}.jpg"
        article_path = article['path']

    return f'''        <div class="card">
          <div class="card-image-wrapper">
            <img src="{image_path}" alt="{article['title']}" onerror="this.parentElement.style.display='none'">
          </div>
          <span class="badge badge-outline" style="margin-bottom: 1rem;">{article['category_name']}</span>
          <span style="color: var(--color-gray); font-size: 0.875rem; display: block; margin-bottom: 1rem;">{date_str}</span>
          <h3>{article['title']}</h3>
          <div style="margin-top: 1.5rem; color: var(--color-gray); font-size: 0.875rem;">
            <p>📖 {article['read_time']} min read</p>
          </div>
          <a href="{article_path}" class="btn btn-outline" style="margin-top: 1.5rem;">Read Article →</a>
        </div>'''

# Update category index pages
categories = {}
for article in articles:
    cat = article['category']
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(article)

for category_slug, cat_articles in categories.items():
    index_file = Path(f"blog/{category_slug}/index.html")
    if not index_file.exists():
        print(f"⚠️  Category index not found: {index_file}")
        continue

    # Read the current file
    with open(index_file, 'r', encoding='utf-8') as f:
        html = f.read()

    # Generate article cards for this category
    cards_html = '\n'.join([format_article_card_with_image(article, is_category_page=True)
                             for article in cat_articles])

    # Replace the grid content
    # Find the grid div and replace its contents
    import re
    pattern = r'(<div class="grid grid-[23]">)(.*?)(</div>\s*</div>\s*</section>)'
    replacement = r'\1\n' + cards_html + r'\n      \3'
    new_html = re.sub(pattern, replacement, html, flags=re.DOTALL)

    # Write back
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(new_html)

    print(f"✓ Updated: {index_file} ({len(cat_articles)} articles)")

# Update main blog page
blog_file = Path("blog.html")
if blog_file.exists():
    with open(blog_file, 'r', encoding='utf-8') as f:
        html = f.read()

    # Get featured articles (first 6 most recent)
    featured = articles[:6]
    cards_html = '\n'.join([format_article_card_with_image(article, is_category_page=False)
                             for article in featured])

    # Replace the featured articles grid
    import re
    pattern = r'(<div class="grid grid-[23]">)(.*?)(</div>\s*</div>\s*</section>)'
    new_html = re.sub(pattern, r'\1\n' + cards_html + r'\n      \3', html, count=1, flags=re.DOTALL)

    with open(blog_file, 'w', encoding='utf-8') as f:
        f.write(new_html)

    print(f"✓ Updated: blog.html (6 featured articles)")

print("\n✓ All blog index pages updated with article images!")
