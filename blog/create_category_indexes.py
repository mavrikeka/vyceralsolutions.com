#!/usr/bin/env python3
"""
Create index.html pages for each category folder to list all articles.
"""

import json
from pathlib import Path
from datetime import datetime

# Load converted articles
with open('blog/converted-articles.json', 'r') as f:
    articles = json.load(f)

# Category info
CATEGORIES = {
    'ai-agents': {'name': 'AI Agents & Agentic Systems', 'icon': '🤖', 'description': 'Building and deploying autonomous AI agents'},
    'ai-philosophy': {'name': 'AI Philosophy & Future of Work', 'icon': '🧠', 'description': 'Exploring AI ethics, future of work, and organizational change'},
    'gtm-strategy': {'name': 'Business & GTM Strategy', 'icon': '🎯', 'description': 'Go-to-market strategies and business transformation'},
    'industry-research': {'name': 'Industry Research & Insights', 'icon': '🏭', 'description': 'Industry-specific AI insights and analysis'},
    'personal-journey': {'name': 'Personal Journey & Entrepreneurship', 'icon': '🚀', 'description': 'Lessons from building an AI-first business'},
    'practical-applications': {'name': 'GenAI Practical Applications & Use Cases', 'icon': '💡', 'description': 'Practical tutorials, how-tos, and implementations'},
    'technical-analysis': {'name': 'Technical Deep Dives & Analysis', 'icon': '⚙️', 'description': 'Architecture, APIs, and technical deep dives'},
    'tools-platforms': {'name': 'GenAI Tools & Platforms', 'icon': '🛠️', 'description': 'Reviews and guides for GenAI tools and platforms'}
}

# Group articles by category
articles_by_category = {}
for article in articles:
    cat = article['category']
    if cat not in articles_by_category:
        articles_by_category[cat] = []
    articles_by_category[cat].append(article)

# HTML template for category index
TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{{DESCRIPTION}}">
  <title>{{CATEGORY_NAME}} | Vyceral Solutions Blog</title>
  <link rel="stylesheet" href="../../css/style.css">
  <script>!function(key) {if (window.reb2b) return;window.reb2b = {loaded: true};var s = document.createElement("script");s.async = true;s.src = "https://b2bjsstore.s3.us-west-2.amazonaws.com/b/" + key + "/" + key + ".js.gz";document.getElementsByTagName("script")[0].parentNode.insertBefore(s, document.getElementsByTagName("script")[0]);}("1N5W0HM2RYO5");</script>
</head>
<body>
  <!-- Navigation -->
  <nav class="nav">
    <div class="nav-container">
      <a href="../../index.html" class="nav-logo">
        <img src="../../images/logo.png" alt="Vyceral Solutions Logo" onerror="this.style.display='none'">
      </a>
      <ul class="nav-menu">
        <li><a href="../../index.html" class="nav-link">Home</a></li>
        <li><a href="../../gtm-automation.html" class="nav-link">GTM Automation</a></li>
        <li><a href="../../consulting-transformation.html" class="nav-link">Consulting Transformation</a></li>
        <li><a href="../../case-studies.html" class="nav-link">Case Studies</a></li>
        <li><a href="../../about.html" class="nav-link">About</a></li>
        <li><a href="../../blog.html" class="nav-link">Blog</a></li>
        <li><a href="../../contact.html" class="nav-link">Contact</a></li>
      </ul>
      <button class="mobile-menu-toggle" aria-label="Toggle mobile menu">
        <span></span>
        <span></span>
        <span></span>
      </button>
    </div>
  </nav>

  <!-- Header -->
  <section class="hero" style="min-height: 40vh;">
    <div class="hero-content">
      <a href="../../blog.html" style="color: rgba(255,255,255,0.8); text-decoration: none; font-size: 0.875rem; display: inline-block; margin-bottom: 1rem;">← Back to Blog</a>
      <h1>{{ICON}} {{CATEGORY_NAME}}</h1>
      <p class="subhead">{{DESCRIPTION}}</p>
      <p style="color: rgba(255,255,255,0.8); margin-top: 1rem;">{{ARTICLE_COUNT}} articles</p>
    </div>
  </section>

  <!-- Articles Grid -->
  <section class="section">
    <div class="container">
      <div class="grid grid-2">
{{ARTICLE_CARDS}}
      </div>
    </div>
  </section>

  <!-- CTA Section -->
  <section class="section bg-light">
    <div class="container">
      <div class="cta-section">
        <h2>Ready to Transform Your GTM Operations?</h2>
        <p>Let's discuss how AI agents can automate 60-75% of your manual work.</p>
        <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
          <a href="../../contact.html" class="btn btn-large">Schedule a Consultation</a>
          <a href="../../case-studies.html" class="btn btn-outline btn-large" style="background: transparent; color: white; border-color: white;">View Case Studies</a>
        </div>
      </div>
    </div>
  </section>

  <!-- Footer -->
  <footer class="footer">
    <div class="container">
      <div class="footer-content">
        <div class="footer-section">
          <h4>Vyceral Solutions LLC</h4>
          <p>Deep Understanding → Tangible Outcomes</p>
          <p style="margin-top: 1rem;">Transforming B2B go-to-market strategies with Generative AI and intelligent automation.</p>
        </div>

        <div class="footer-section">
          <h4>Solutions</h4>
          <ul class="footer-links">
            <li><a href="../../gtm-automation.html">GTM Automation</a></li>
            <li><a href="../../consulting-transformation.html">Consulting Transformation</a></li>
          </ul>
        </div>

        <div class="footer-section">
          <h4>Company</h4>
          <ul class="footer-links">
            <li><a href="../../about.html">About Us</a></li>
            <li><a href="../../case-studies.html">Case Studies</a></li>
            <li><a href="../../blog.html">Blog</a></li>
            <li><a href="../../contact.html">Contact</a></li>
          </ul>
        </div>

        <div class="footer-section">
          <h4>Get in Touch</h4>
          <ul class="footer-links">
            <li><a href="mailto:vikram.ekambaram@vyceralsolutions.com">vikram.ekambaram@vyceralsolutions.com</a></li>
            <li><a href="https://www.linkedin.com/in/vikramekambaram" target="_blank">LinkedIn Profile</a></li>
            <li><a href="https://www.linkedin.com/newsletters/7158509558993215488" target="_blank">Newsletter (LinkedIn)</a></li>
            <li style="margin-top: 0.5rem; color: var(--color-gray);">Croton-on-Hudson, NY</li>
          </ul>
        </div>
      </div>

      <div class="footer-bottom">
        <p>Copyright © 2025 Vyceral Solutions LLC. All rights reserved.</p>
      </div>
    </div>
  </footer>

  <script src="../../js/main.js"></script>
</body>
</html>
'''

CARD_TEMPLATE = '''        <div class="card">
          <div class="card-image-wrapper">
            <img src="../../images/article-images/{{SLUG}}.jpg" alt="{{TITLE}}" onerror="this.parentElement.style.display='none'">
          </div>
          <span class="badge badge-outline" style="margin-bottom: 1rem;">{{CATEGORY_NAME}}</span>
          <span style="color: var(--color-gray); font-size: 0.875rem; display: block; margin-bottom: 1rem;">{{DATE}}</span>
          <h3>{{TITLE}}</h3>
          <div style="margin-top: 1.5rem; color: var(--color-gray); font-size: 0.875rem;">
            <p>📖 {{READ_TIME}} min read</p>
          </div>
          <a href="{{SLUG}}.html" class="btn btn-outline" style="margin-top: 1.5rem;">Read Article →</a>
        </div>
'''

# Generate index.html for each category
for cat_slug, cat_info in CATEGORIES.items():
    if cat_slug not in articles_by_category:
        print(f"No articles found for category: {cat_slug}")
        continue

    cat_articles = articles_by_category[cat_slug]

    # Generate article cards
    cards_html = []
    for article in cat_articles:
        date_obj = datetime.fromisoformat(article['date'])
        date_str = date_obj.strftime('%B %d, %Y')

        card = CARD_TEMPLATE.replace('{{CATEGORY_NAME}}', cat_info['name'])
        card = card.replace('{{DATE}}', date_str)
        card = card.replace('{{TITLE}}', article['title'])
        card = card.replace('{{READ_TIME}}', str(article['read_time']))
        card = card.replace('{{SLUG}}', article['slug'])
        cards_html.append(card)

    # Generate full HTML
    html = TEMPLATE.replace('{{CATEGORY_NAME}}', cat_info['name'])
    html = html.replace('{{ICON}}', cat_info['icon'])
    html = html.replace('{{DESCRIPTION}}', cat_info['description'])
    html = html.replace('{{ARTICLE_COUNT}}', str(len(cat_articles)))
    html = html.replace('{{ARTICLE_CARDS}}', '\n'.join(cards_html))

    # Write index.html to category folder
    output_path = Path(f'blog/{cat_slug}/index.html')
    with open(output_path, 'w') as f:
        f.write(html)

    print(f"Created index for {cat_info['name']}: {output_path}")

print(f"\n✓ Created {len(articles_by_category)} category index pages")
