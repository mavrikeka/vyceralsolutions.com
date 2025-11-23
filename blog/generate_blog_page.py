#!/usr/bin/env python3
"""
Generate updated blog.html page with real article cards from converted articles.
"""

import json
from datetime import datetime
from pathlib import Path

# Load converted articles
with open('blog/converted-articles.json', 'r') as f:
    articles = json.load(f)

# Category mapping
CATEGORIES = {
    'gtm-automation': {'name': 'GTM Automation', 'icon': '🎯'},
    'ai-agents': {'name': 'AI Agents', 'icon': '🤖'},
    'use-cases': {'name': 'Use Cases', 'icon': '💡'},
    'strategy': {'name': 'Strategy', 'icon': '📊'},
    'technical': {'name': 'Technical', 'icon': '⚙️'}
}

# Generate article cards HTML
def generate_article_card(article):
    """Generate HTML for a single article card."""
    date_obj = datetime.fromisoformat(article['date'])
    date_str = date_obj.strftime('%B %d, %Y')
    category_info = CATEGORIES.get(article['category'], {'name': 'Insights', 'icon': '📝'})

    # Truncate title if too long
    title = article['title']
    if len(title) > 80:
        title = title[:77] + "..."

    return f'''
        <div class="card">
          <span class="badge badge-outline" style="margin-bottom: 1rem;">{category_info['name']}</span>
          <span style="color: var(--color-gray); font-size: 0.875rem; display: block; margin-bottom: 1rem;">{date_str}</span>
          <h3>{title}</h3>
          <div style="margin-top: 1.5rem; color: var(--color-gray); font-size: 0.875rem;">
            <p>📖 {article['read_time']} min read</p>
          </div>
          <a href="{article['path']}" class="btn btn-outline" style="margin-top: 1.5rem;">Read Article →</a>
        </div>'''

# Group articles by category for the topics section
category_counts = {}
for article in articles:
    cat = article['category']
    category_counts[cat] = category_counts.get(cat, 0) + 1

# Get featured articles (first 6 most recent)
featured_articles = articles[:6]

# Generate featured articles HTML
featured_html = '\n'.join([generate_article_card(article) for article in featured_articles])

print("Generated blog.html with:")
print(f"- {len(featured_articles)} featured articles")
print(f"- Category distribution:")
for cat, count in sorted(category_counts.items()):
    cat_info = CATEGORIES.get(cat, {'name': cat})
    print(f"  * {cat_info['name']}: {count} articles")
print(f"\nUpdate blog.html manually with the generated cards or run full replacement.")
print(f"Featured articles HTML saved to: blog/featured-articles.html")

# Save featured articles HTML to a file for easy copying
with open('blog/featured-articles.html', 'w') as f:
    f.write(featured_html)

print("\nNext step: Copy content from blog/featured-articles.html to blog.html")
