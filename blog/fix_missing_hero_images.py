#!/usr/bin/env python3
"""
Add hero images to the 17 articles that are missing them.
"""

from pathlib import Path
from bs4 import BeautifulSoup

# Articles missing hero images with their correct image filenames
articles_to_fix = {
    'blog/ai-agents/autonomous-agents-it-all-started-with-manus.html': 'autonomous-agents---it-all-started-with-manus.jpg',
    'blog/ai-philosophy/schemingai-the-dark-side-of-ai.html': 'schemingai---the-dark-side-of-ai.jpg',
    'blog/ai-philosophy/why-ai-will-replace-some-humans.html': 'why-ai-will-replace-some-humans.jpg',  # might be different
    'blog/ai-philosophy/expertise-and-genai.html': 'expertise-and-genai.jpg',  # might be different
    'blog/gtm-strategy/the-future-is-multi-agentic.html': 'the-future-is-multi-agentic.jpg',
    'blog/gtm-strategy/genai-will-we-see-a-new-application-architecture.html': 'genai-will-we-see-a-new-application-architecture.jpg',  # might be different
    'blog/gtm-strategy/crm-20-a-genai-crm.html': 'crm-20---a-genai-crm.jpg',
    'blog/gtm-strategy/why-are-there-so-many-top-of-funnel-gen-ai-use-cases.html': 'why-are-there-so-many-top-of-funnel-gen-ai-use-cases.jpg',
    'blog/industry-research/big-tech-ai-layoffs-dividends-stock-prices.html': 'big-tech-ai-layoffs-dividends-stock-prices.jpg',  # might be different
    'blog/industry-research/the-mit-study-on-genai-that-roiled-stock-markets-my-002.html': 'the-mit-study-on-genai-that-roiled-stock-markets-my-002.jpg',  # might be different
    'blog/personal-journey/my-ai-journey-its-not-hype-2.html': 'my-ai-journey---its-not-hype-2.jpg',
    'blog/personal-journey/my-ai-journey-its-not-hype.html': 'my-ai-journey---its-not-hype.jpg',
    'blog/practical-applications/generating-images-with-an-agent.html': 'generating-images-with-an-agent.jpg',
    'blog/practical-applications/everyone-is-a-programmer.html': 'everyone-is-a-programmer.jpg',
    'blog/technical-analysis/using-genai-for-analytics-using-genai-to-understand-something-technical-.html': 'using-genai-for-analytics-using-genai-to-understand-something-technical.jpg',
    'blog/tools-platforms/will-operator-take-my-job.html': 'will-operator-take-my-job.jpg',
    'blog/tools-platforms/is-vibe-coding-for-me.html': 'is-vibe-coding-for-me.jpg',
}

success_count = 0
fail_count = 0

for article_path, image_filename in articles_to_fix.items():
    file_path = Path(article_path)

    if not file_path.exists():
        print(f"⚠️  File not found: {article_path}")
        fail_count += 1
        continue

    # Read the HTML
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Find the breadcrumbs div
    breadcrumbs = soup.find('div', class_='breadcrumbs')
    if not breadcrumbs:
        print(f"⚠️  No breadcrumbs found in: {article_path}")
        fail_count += 1
        continue

    # Check if hero image already exists
    if soup.find('div', class_='article-hero-image'):
        print(f"⚠️  Hero image already exists in: {article_path}")
        continue

    # Get the article title for alt text
    article_header = soup.find('header', class_='article-header')
    if article_header:
        h1 = article_header.find('h1')
        title = h1.get_text(strip=True) if h1 else 'Article'
    else:
        title = 'Article'

    # Create the hero image div
    hero_image_html = f'''
  <!-- Article Hero Image -->
  <div class="article-hero-image">
    <img src="../../images/article-images/{image_filename}" alt="{title}" onerror="this.parentElement.style.display='none'">
  </div>
'''

    # Create new div element
    hero_div = BeautifulSoup(hero_image_html, 'html.parser')

    # Insert after breadcrumbs
    breadcrumbs.insert_after(hero_div)

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    print(f"✓ Added hero image to: {article_path}")
    success_count += 1

print(f"\n{'='*60}")
print(f"Hero images added: {success_count}")
print(f"Failed: {fail_count}")
print(f"Total: {len(articles_to_fix)}")
print(f"{'='*60}")
