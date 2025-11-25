#!/usr/bin/env python3
"""
Single-article ingestion script for blog publishing.
Processes one article at a time from blog/new-articles/ folder.

Usage:
    python3 blog/add_article.py --category personal-journey
    python3 blog/add_article.py  # Interactive category selection
    python3 blog/add_article.py --category ai-agents --dry-run
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
import urllib.request
import shutil

# Category definitions
CATEGORIES = {
    'ai-agents': {'name': 'AI Agents', 'icon': '🤖'},
    'ai-philosophy': {'name': 'AI Philosophy', 'icon': '🧠'},
    'gtm-strategy': {'name': 'GTM Strategy', 'icon': '🎯'},
    'industry-research': {'name': 'Industry Research', 'icon': '🏭'},
    'personal-journey': {'name': 'Personal Journey', 'icon': '🚀'},
    'practical-applications': {'name': 'Practical Applications', 'icon': '💡'},
    'technical-analysis': {'name': 'Technical Analysis', 'icon': '⚙️'},
    'tools-platforms': {'name': 'Tools & Platforms', 'icon': '🛠️'}
}

def find_article_in_inbox():
    """Find the single HTML file in blog/new-articles/."""
    # Get script directory and work relative to project root
    script_dir = Path(__file__).parent.parent  # blog/add_article.py -> project root
    inbox_dir = script_dir / 'blog' / 'new-articles'
    html_files = list(inbox_dir.glob('*.html'))

    if len(html_files) == 0:
        print("❌ Error: No article found in blog/new-articles/")
        print("   Please add an HTML file to blog/new-articles/")
        sys.exit(1)

    if len(html_files) > 1:
        print(f"❌ Error: Found {len(html_files)} files in blog/new-articles/")
        print("   Please process one article at a time.")
        print("\n   Files found:")
        for f in html_files:
            print(f"   - {f.name}")
        sys.exit(1)

    return html_files[0]

def extract_metadata(file_path):
    """Extract metadata from the console-generated HTML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Extract title
    title_tag = soup.find('h1')
    title = title_tag.text.strip() if title_tag else "Untitled"

    # Extract date
    time_tag = soup.find('time')
    date_str = time_tag.text.strip() if time_tag else datetime.now().strftime('%B %d, %Y')

    # Parse date
    try:
        date_obj = datetime.strptime(date_str, '%B %d, %Y')
    except:
        date_obj = datetime.now()

    # Extract author
    author_tag = soup.find('span', class_='author')
    author = author_tag.text.strip() if author_tag else "Vikram Ekambaram"

    # Extract cover image URL
    cover_img_tag = soup.find('img', class_='cover-image')
    cover_img_url = cover_img_tag['src'] if cover_img_tag else None

    # Extract content (everything after header)
    article_tag = soup.find('article')
    if article_tag:
        # Remove the header
        header_tag = article_tag.find('header')
        if header_tag:
            header_tag.decompose()

        # Get remaining content
        content_html = str(article_tag).replace('<article>', '').replace('</article>', '').strip()
    else:
        content_html = ""

    # Calculate read time
    text_content = soup.get_text()
    word_count = len(text_content.split())
    read_time = max(1, round(word_count / 200))

    return {
        'title': title,
        'date': date_obj,
        'author': author,
        'cover_image_url': cover_img_url,
        'content_html': content_html,
        'word_count': word_count,
        'read_time': read_time
    }

def create_slug(filename):
    """Generate slug from filename (already created by console script)."""
    # Remove .html extension
    slug = filename.replace('.html', '')
    # Clean up any remaining issues
    slug = re.sub(r'[^\w\s-]', '', slug.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug[:80]

def select_category(cli_category=None):
    """Select category interactively or from CLI."""
    if cli_category:
        if cli_category not in CATEGORIES:
            print(f"❌ Error: Unknown category '{cli_category}'")
            print("\n   Valid categories:")
            for slug, info in CATEGORIES.items():
                print(f"   - {slug}: {info['icon']} {info['name']}")
            sys.exit(1)
        return cli_category

    # Interactive selection
    print("\n? Select category:")
    categories_list = list(CATEGORIES.items())
    for i, (slug, info) in enumerate(categories_list, 1):
        print(f"  {i}. {info['icon']} {info['name']}")

    while True:
        try:
            choice = input("\nEnter number (1-8): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(categories_list):
                return categories_list[idx][0]
            else:
                print("Invalid choice. Please enter 1-8.")
        except (ValueError, KeyboardInterrupt):
            print("\n❌ Cancelled")
            sys.exit(1)

def download_image(url, output_path, skip_download=False):
    """Download hero image from LinkedIn CDN."""
    if skip_download:
        print(f"⏭️  Skipped image download (--skip-image)")
        return False

    if not url:
        print(f"⚠️  Warning: No cover image found in article")
        return False

    try:
        # Create directory if needed
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Download image
        urllib.request.urlretrieve(url, output_path)
        return True
    except Exception as e:
        print(f"⚠️  Warning: Failed to download image: {e}")
        print(f"   You can manually add it to: {output_path}")
        return False

def generate_article_html(metadata, slug, category, template):
    """Generate article HTML from template."""
    date_str = metadata['date'].strftime('%B %d, %Y')
    category_name = CATEGORIES[category]['name']

    # Create meta description from content
    soup = BeautifulSoup(metadata['content_html'], 'html.parser')
    text_content = soup.get_text()
    first_para = ' '.join(text_content.split()[:30])
    meta_description = first_para[:155] + "..." if len(first_para) > 155 else first_para

    # Replace template variables
    html = template
    html = html.replace('{{TITLE}}', metadata['title'])
    html = html.replace('{{DATE}}', date_str)
    html = html.replace('{{CATEGORY}}', category_name)
    html = html.replace('{{CATEGORY_SLUG}}', category)
    html = html.replace('{{READ_TIME}}', str(metadata['read_time']))
    html = html.replace('{{CONTENT}}', metadata['content_html'])
    html = html.replace('{{META_DESCRIPTION}}', meta_description)
    html = html.replace('{{SLUG}}', slug)

    return html

def update_converted_articles(metadata, slug, category):
    """Add new article to converted-articles.json."""
    json_path = Path('blog/converted-articles.json')

    # Load existing
    with open(json_path, 'r') as f:
        articles = json.load(f)

    # Add new article
    new_article = {
        'title': metadata['title'],
        'slug': slug,
        'category': category,
        'category_name': CATEGORIES[category]['name'],
        'date': metadata['date'].strftime('%Y-%m-%d %H:%M:%S'),
        'read_time': metadata['read_time'],
        'path': f"blog/{category}/{slug}.html"
    }

    articles.insert(0, new_article)  # Add to beginning

    # Save
    with open(json_path, 'w') as f:
        json.dump(articles, f, indent=2)

    return len(articles)

def update_metadata_json(metadata, slug, category, source_filename):
    """Add to articles-metadata.json."""
    json_path = Path('blog/articles-metadata.json')

    # Load existing
    with open(json_path, 'r') as f:
        metadata_list = json.load(f)

    # Add new entry
    new_entry = {
        'title': metadata['title'],
        'date': metadata['date'].isoformat(),
        'category': category,
        'read_time': metadata['read_time'],
        'word_count': metadata['word_count'],
        'source_file': source_filename
    }

    metadata_list.insert(0, new_entry)

    # Save
    with open(json_path, 'w') as f:
        json.dump(metadata_list, f, indent=2)

def regenerate_category_index(category):
    """Regenerate the category index page."""
    # This is a simplified version - just updates the count
    # The full index regeneration can be done separately
    index_path = Path(f'blog/{category}/index.html')

    # Count articles in category
    with open('blog/converted-articles.json', 'r') as f:
        articles = json.load(f)

    cat_articles = [a for a in articles if a['category'] == category]
    count = len(cat_articles)

    # Re-run the category index generator
    import subprocess
    try:
        subprocess.run(['python3', 'blog/create_category_indexes.py'],
                      capture_output=True, check=True)
        return count
    except:
        # Fallback: just return count
        return count

def update_blog_homepage(metadata, slug, category):
    """Automatically update blog.html with new article."""
    from bs4 import BeautifulSoup

    blog_html_path = Path('blog.html')

    # Read current blog.html
    with open(blog_html_path, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Find the grid div
    grid_div = soup.find('div', class_='grid grid-2')
    if not grid_div:
        return False

    # Get category name
    category_name = CATEGORIES[category]['name']
    date_str = metadata['date'].strftime('%B %d, %Y')

    # Create new article card HTML
    new_card_html = f'''<div class="card">
          <div class="card-image-wrapper">
            <img src="images/article-images/{slug}.jpg" alt="{metadata['title']}" onerror="this.parentElement.style.display='none'">
          </div>
          <span class="badge badge-outline" style="margin-bottom: 1rem;">{category_name}</span>
          <span style="color: var(--color-gray); font-size: 0.875rem; display: block; margin-bottom: 1rem;">{date_str}</span>
          <h3>{metadata['title']}</h3>
          <div style="margin-top: 1.5rem; color: var(--color-gray); font-size: 0.875rem;">
            <p>📖 {metadata['read_time']} min read</p>
          </div>
          <a href="blog/{category}/{slug}.html" class="btn btn-outline" style="margin-top: 1.5rem;">Read Article →</a>
        </div>'''

    # Parse the new card
    new_card = BeautifulSoup(new_card_html, 'html.parser')

    # Insert at the beginning of the grid (before first child)
    first_card = grid_div.find('div', class_='card')
    if first_card:
        first_card.insert_before(new_card)
    else:
        grid_div.append(new_card)

    # Keep only the first 6 cards (featured articles)
    all_cards = grid_div.find_all('div', class_='card')
    if len(all_cards) > 6:
        # Remove cards beyond 6
        for card in all_cards[6:]:
            card.decompose()

    # Write updated HTML
    with open(blog_html_path, 'w') as f:
        f.write(str(soup))

    return True

def main():
    parser = argparse.ArgumentParser(description='Add a new blog article')
    parser.add_argument('--category', type=str, help='Category slug (e.g., ai-agents)')
    parser.add_argument('--dry-run', action='store_true', help='Preview without making changes')
    parser.add_argument('--skip-image', action='store_true', help='Skip image download')
    args = parser.parse_args()

    # Change to project root directory
    script_dir = Path(__file__).parent.parent
    os.chdir(script_dir)

    print("🔍 Checking blog/new-articles/ for article...")

    # Find article
    article_file = find_article_in_inbox()
    print(f"✓ Found: {article_file.name}\n")

    # Extract metadata
    print("📄 Parsing article...")
    metadata = extract_metadata(article_file)
    slug = create_slug(article_file.name)

    print(f"✓ Title: \"{metadata['title']}\"")
    print(f"✓ Date: {metadata['date'].strftime('%B %d, %Y')}")
    print(f"✓ Author: {metadata['author']}")
    print(f"✓ Words: {metadata['word_count']}")
    print(f"✓ Read time: {metadata['read_time']} min")
    print(f"✓ Slug: {slug}\n")

    # Select category
    category = select_category(args.category)
    print(f"📁 Category: {CATEGORIES[category]['icon']} {CATEGORIES[category]['name']}")
    if args.category:
        print(f"   (from --category flag)\n")
    else:
        print()

    if args.dry_run:
        print("🏃 DRY RUN MODE - No changes will be made\n")
        print("Would perform:")
        print(f"  - Download image to: images/article-images/{slug}.jpg")
        print(f"  - Create article: blog/{category}/{slug}.html")
        print(f"  - Update: blog/converted-articles.json")
        print(f"  - Update: blog/articles-metadata.json")
        print(f"  - Regenerate: blog/{category}/index.html")
        print(f"  - Update: blog.html (add to latest articles)")
        print(f"  - Delete: blog/new-articles/{article_file.name}")
        return

    # Download image
    print("📥 Downloading hero image...")
    image_path = Path(f"images/article-images/{slug}.jpg")
    if download_image(metadata['cover_image_url'], image_path, args.skip_image):
        print(f"✓ Saved to: {image_path}\n")
    else:
        print()

    # Load template
    with open('blog/article-template.html', 'r') as f:
        template = f.read()

    # Generate article HTML
    print("📝 Generating article page...")
    article_html = generate_article_html(metadata, slug, category, template)

    # Save article
    article_path = Path(f"blog/{category}/{slug}.html")
    article_path.parent.mkdir(parents=True, exist_ok=True)
    with open(article_path, 'w') as f:
        f.write(article_html)
    print(f"✓ Created: {article_path}\n")

    # Update indexes
    print("📊 Updating indexes...")
    total_articles = update_converted_articles(metadata, slug, category)
    print(f"✓ Updated: blog/converted-articles.json ({total_articles} total articles)")

    update_metadata_json(metadata, slug, category, article_file.name)
    print(f"✓ Updated: blog/articles-metadata.json")

    cat_count = regenerate_category_index(category)
    print(f"✓ Regenerated: blog/{category}/index.html ({cat_count} articles)")

    if update_blog_homepage(metadata, slug, category):
        print(f"✓ Updated: blog.html (latest articles)\n")
    else:
        print(f"⚠️  Could not update blog.html (check manually)\n")

    # Cleanup
    print("🗑️  Cleaning up...")
    article_file.unlink()
    print(f"✓ Deleted: {article_file}")
    print(f"✓ Folder blog/new-articles/ is ready for next article\n")

    # Success
    print("✅ Article published successfully!\n")

    # Next steps
    print("📋 Next Steps:")
    print(f"1. Review article: {article_path}")
    print(f"2. Commit to git:")
    print(f"   git add blog/{category}/")
    print(f"   git add blog.html")
    print(f"   git add images/article-images/{slug}.jpg")
    print(f"   git add blog/converted-articles.json")
    print(f"   git add blog/articles-metadata.json")
    print(f"   git commit -m \"Add article: {metadata['title'][:50]}...\"")
    print(f"   git push")

if __name__ == "__main__":
    main()
