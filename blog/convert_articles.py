#!/usr/bin/env python3
"""
Script to convert LinkedIn articles to Vyceral website blog format.
Analyzes GenAI in GTM newsletter articles, selects top 50, categorizes them,
and converts to website-compatible HTML.
"""

import os
import re
from bs4 import BeautifulSoup
from pathlib import Path
import json
from datetime import datetime
import shutil

# Configuration
SOURCE_DIR = Path("blog/articles-raw")
OUTPUT_DIR = Path("blog")
CATEGORIES = {
    'gtm-automation': 'GTM Automation',
    'ai-agents': 'AI Agents & Platforms',
    'use-cases': 'Use Cases & Tutorials',
    'strategy': 'Strategy & Insights',
    'technical': 'Technical Deep-Dives'
}

def extract_article_metadata(file_path):
    """Extract metadata from LinkedIn article HTML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Extract title
    title_tag = soup.find('title')
    title = title_tag.text if title_tag else "Untitled"

    # Extract h1 title (often better formatted)
    h1_tag = soup.find('h1')
    if h1_tag:
        h1_link = h1_tag.find('a')
        if h1_link:
            title = h1_link.text

    # Extract dates
    created = None
    published = None
    created_tag = soup.find('p', class_='created')
    published_tag = soup.find('p', class_='published')

    if published_tag:
        date_text = published_tag.text.replace('Published on', '').strip()
        try:
            published = datetime.strptime(date_text, '%Y-%m-%d %H:%M')
        except:
            pass

    if created_tag and not published:
        date_text = created_tag.text.replace('Created on', '').strip()
        try:
            created = datetime.strptime(date_text, '%Y-%m-%d %H:%M')
        except:
            pass

    # Extract content
    # Find the main content div FIRST before removing anything
    body_content = soup.find('body')
    content_html = ""

    if body_content:
        # Find the main div with article content (it's usually the last div)
        all_divs = body_content.find_all('div', recursive=False)
        content_div = all_divs[-1] if all_divs else None

        if content_div:
            # Get the content from the div
            content_html = content_div.decode_contents()
        else:
            # Fallback: try to find any div
            content_div = body_content.find('div')
            if content_div:
                content_html = content_div.decode_contents()
            else:
                # Last resort: get all paragraphs after the h1
                h1 = body_content.find('h1')
                if h1:
                    # Get all siblings after h1
                    content_parts = []
                    for sibling in h1.find_next_siblings():
                        if sibling.name:
                            content_parts.append(str(sibling))
                    content_html = '\n'.join(content_parts)

    # Categorize based on title and content keywords
    category = categorize_article(title, content_html)

    # Calculate read time (rough estimate: 200 words per minute)
    text_content = soup.get_text()
    word_count = len(text_content.split())
    read_time = max(1, round(word_count / 200))

    return {
        'title': title,
        'date': published or created,
        'category': category,
        'read_time': read_time,
        'content_html': content_html,
        'word_count': word_count,
        'file_name': file_path.name
    }

def categorize_article(title, content):
    """Categorize article using agent.ai API based on title and content preview."""
    import requests

    # Get text preview (first 2000 chars of content)
    soup = BeautifulSoup(content, 'html.parser')
    text_preview = soup.get_text()[:2000]

    # Define categories and descriptions
    categories_desc = """
    - gtm-automation: Articles about go-to-market strategies, sales processes, account planning, CRM, pipeline management, customer success, outbound strategies, prospecting
    - ai-agents: Articles about AI agents, autonomous agents, agentic systems, specific platforms (Anthropic, Claude, MindStudio, AnyQuest), digital workers
    - use-cases: Practical tutorials, how-to guides, step-by-step examples, "Can GenAI do X?", "Using GenAI for Y", specific implementations
    - strategy: Business strategy, organizational transformation, AI adoption, future trends, industry analysis, thought leadership, innovation
    - technical: Technical implementations, architecture, APIs, coding, prompt engineering, MCP, functions, workflows, technical deep-dives
    """

    instructions = f"""Categorize this article into ONE of these categories based on its title and content preview:

{categories_desc}

Article Title: {title}

Content Preview:
{text_preview}

Respond with ONLY the category slug (gtm-automation, ai-agents, use-cases, strategy, or technical). No explanation needed."""

    try:
        # API key has been deleted - use fallback categorization
        print(f"   Using keyword fallback for: {title[:50]}...")
        return categorize_article_fallback(title, content)

    except Exception as e:
        print(f"   Error categorizing {title[:50]}: {e}")
        print(f"   Using keyword fallback...")
        return categorize_article_fallback(title, content)


def categorize_article_fallback(title, content):
    """Fallback keyword-based categorization if API fails."""
    title_lower = title.lower()
    content_lower = content.lower()

    # GTM Automation keywords
    gtm_keywords = ['gtm', 'go-to-market', 'sales', 'account planning', 'outbound',
                    'prospect', 'crm', 'pipeline', 'customer success', 'case study']

    # AI Agents keywords
    agent_keywords = ['agent', 'autonomous', 'agentic', 'anthropic', 'claude',
                      'mindstudio', 'anyquest', 'digital worker']

    # Use Cases keywords
    usecase_keywords = ['how i', 'using genai', 'tutorial', 'step-by-step',
                        'example', 'can genai', 'cookbook']

    # Strategy keywords
    strategy_keywords = ['strategy', 'future', 'organization', 'adoption',
                         'transformation', 'hype', 'journey']

    # Technical keywords
    technical_keywords = ['architecture', 'prompt', 'function', 'workflow',
                          'mcp', 'api', 'code', 'vibe coding']

    # Score each category
    scores = {
        'gtm-automation': sum(1 for kw in gtm_keywords if kw in title_lower or kw in content_lower[:1000]),
        'ai-agents': sum(1 for kw in agent_keywords if kw in title_lower or kw in content_lower[:1000]),
        'use-cases': sum(1 for kw in usecase_keywords if kw in title_lower or kw in content_lower[:1000]),
        'strategy': sum(1 for kw in strategy_keywords if kw in title_lower or kw in content_lower[:1000]),
        'technical': sum(1 for kw in technical_keywords if kw in title_lower or kw in content_lower[:1000])
    }

    # Return category with highest score, default to strategy
    max_category = max(scores.items(), key=lambda x: x[1])
    return max_category[0] if max_category[1] > 0 else 'strategy'

def create_slug(title):
    """Create URL-friendly slug from title."""
    # Convert to lowercase and replace spaces/special chars with hyphens
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug[:80]  # Limit length

def generate_article_html(metadata, template):
    """Generate HTML for a single article using template."""
    # Create slug for filename
    slug = create_slug(metadata['title'])

    # Format date
    date_str = metadata['date'].strftime('%B %d, %Y') if metadata['date'] else 'Date Unknown'

    # Get category display name
    category_name = CATEGORIES.get(metadata['category'], 'Insights')

    # Content is already cleaned during extraction, just use it
    content_html = metadata['content_html']

    # Create meta description from content
    soup = BeautifulSoup(content_html, 'html.parser')
    text_content = soup.get_text()
    first_para = ' '.join(text_content.split()[:30])
    meta_description = first_para[:155] + "..." if len(first_para) > 155 else first_para

    # Replace template variables
    html = template.replace('{{TITLE}}', metadata['title'])
    html = html.replace('{{DATE}}', date_str)
    html = html.replace('{{CATEGORY}}', category_name)
    html = html.replace('{{CATEGORY_SLUG}}', metadata['category'])
    html = html.replace('{{READ_TIME}}', str(metadata['read_time']))
    html = html.replace('{{CONTENT}}', content_html)
    html = html.replace('{{META_DESCRIPTION}}', meta_description)

    return slug, html

def main():
    """Main conversion process."""
    print("=" * 60)
    print("VYCERAL BLOG ARTICLE CONVERTER")
    print("=" * 60)

    # Find all GenAI newsletter articles
    print("\n1. Finding GenAI in GTM newsletter articles...")
    genai_articles = []

    for file_path in SOURCE_DIR.glob("*.html"):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if "GenAI for Go-To-Market teams" in content:
                genai_articles.append(file_path)

    print(f"   Found {len(genai_articles)} GenAI newsletter articles")

    # Extract metadata from all articles
    print("\n2. Extracting metadata from all articles...")
    articles_metadata = []

    for i, file_path in enumerate(genai_articles, 1):
        try:
            metadata = extract_article_metadata(file_path)
            articles_metadata.append(metadata)
            if i % 10 == 0:
                print(f"   Processed {i}/{len(genai_articles)} articles...")
        except Exception as e:
            print(f"   Error processing {file_path.name}: {e}")

    print(f"   Successfully extracted metadata from {len(articles_metadata)} articles")

    # Sort by date (most recent first) and select all articles
    print("\n3. Selecting all GenAI in GTM articles...")
    articles_metadata.sort(key=lambda x: x['date'] if x['date'] else datetime.min, reverse=True)
    top_50 = articles_metadata  # Using all articles instead of limiting to 50

    # Show category distribution
    category_counts = {}
    for article in top_50:
        cat = article['category']
        category_counts[cat] = category_counts.get(cat, 0) + 1

    print("\n   Category distribution:")
    for cat, count in sorted(category_counts.items()):
        print(f"   - {CATEGORIES[cat]}: {count} articles")

    # Save metadata to JSON for reference
    print("\n4. Saving metadata...")
    metadata_output = []
    for article in top_50:
        metadata_output.append({
            'title': article['title'],
            'date': article['date'].isoformat() if article['date'] else None,
            'category': article['category'],
            'read_time': article['read_time'],
            'word_count': article['word_count'],
            'source_file': article['file_name']
        })

    with open('blog/articles-metadata.json', 'w') as f:
        json.dump(metadata_output, f, indent=2)

    print(f"   Saved metadata to blog/articles-metadata.json")

    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE!")
    print("=" * 60)
    print(f"\nNext steps:")
    print(f"1. Review the category distribution above")
    print(f"2. Check blog/articles-metadata.json for the selected articles")
    print(f"3. Run the conversion process to generate HTML files")
    print("\n" + "=" * 60)

    # Auto-proceed with conversion
    print("\nProceeding with conversion...")

    # Load template
    print("\n5. Loading article template...")
    with open('blog/article-template.html', 'r') as f:
        template = f.read()

    # Create category folders
    print("\n6. Creating category folders...")
    for category_slug in CATEGORIES.keys():
        category_dir = OUTPUT_DIR / category_slug
        category_dir.mkdir(exist_ok=True)
        print(f"   Created: blog/{category_slug}/")

    # Convert each article
    print("\n7. Converting articles to website format...")
    converted_articles = []

    for i, article in enumerate(top_50, 1):
        try:
            slug, html = generate_article_html(article, template)

            # Determine output path
            category_dir = OUTPUT_DIR / article['category']
            output_path = category_dir / f"{slug}.html"

            # Write HTML file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)

            converted_articles.append({
                'title': article['title'],
                'slug': slug,
                'category': article['category'],
                'date': article['date'],
                'read_time': article['read_time'],
                'path': f"blog/{article['category']}/{slug}.html"
            })

            if i % 10 == 0:
                print(f"   Converted {i}/{len(top_50)} articles...")

        except Exception as e:
            print(f"   Error converting {article['title']}: {e}")

    print(f"   Successfully converted {len(converted_articles)} articles")

    # Save converted articles list
    print("\n8. Saving converted articles index...")
    with open('blog/converted-articles.json', 'w') as f:
        json.dump(converted_articles, f, indent=2, default=str)

    print("\n" + "=" * 60)
    print("CONVERSION COMPLETE!")
    print("=" * 60)
    print(f"\nResults:")
    print(f"- Converted {len(converted_articles)} articles")
    print(f"- Organized into {len(CATEGORIES)} categories")
    print(f"- Saved to blog/ folder with category subfolders")
    print(f"- Index saved to blog/converted-articles.json")
    print(f"\nNext: Update blog.html landing page with article cards")

if __name__ == "__main__":
    main()
