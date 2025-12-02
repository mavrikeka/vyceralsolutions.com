#!/usr/bin/env python3
"""
Add SEO improvements to blog pages:
- Canonical tags
- Breadcrumb navigation (visual + schema)
- Article schema for article pages
- CollectionPage schema for category index pages
"""

import os
import re
from pathlib import Path
from typing import Tuple, Optional

# Category name mapping
CATEGORY_NAMES = {
    'ai-agents': 'AI Agents',
    'ai-philosophy': 'AI Philosophy',
    'gtm-strategy': 'GTM Strategy',
    'industry-research': 'Industry Research',
    'personal-journey': 'Personal Journey',
    'practical-applications': 'Practical Applications',
    'technical-analysis': 'Technical Analysis',
    'tools-platforms': 'Tools & Platforms'
}

def extract_title(html_content: str) -> str:
    """Extract title from HTML"""
    match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE)
    if match:
        # Remove " | Vyceral Solutions" suffix if present
        title = match.group(1)
        title = re.sub(r'\s*\|\s*Vyceral Solutions.*$', '', title)
        return title.strip()
    return "Article"

def extract_description(html_content: str) -> str:
    """Extract meta description"""
    match = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', html_content, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""

def is_category_page(file_path: Path) -> bool:
    """Check if file is a category index page"""
    return file_path.name == 'index.html'

def get_category_from_path(file_path: Path) -> str:
    """Extract category slug from file path"""
    # Path is like: blog/ai-agents/index.html or blog/ai-agents/article.html
    parts = file_path.parts
    if 'blog' in parts:
        blog_index = parts.index('blog')
        if len(parts) > blog_index + 1:
            return parts[blog_index + 1]
    return ""

def create_canonical_tag(url_path: str) -> str:
    """Create canonical link tag"""
    return f'  <!-- Canonical URL -->\n  <link rel="canonical" href="https://vyceralsolutions.com/{url_path}">\n'

def create_breadcrumb_html(levels: list) -> str:
    """Create breadcrumb navigation HTML"""
    breadcrumb_html = '''
  <!-- Breadcrumbs -->
  <div class="breadcrumbs">
    <div class="breadcrumbs-container">
      <nav aria-label="Breadcrumb">
'''

    for i, (name, url) in enumerate(levels[:-1]):
        breadcrumb_html += f'        <a href="{url}">{name}</a>\n'
        breadcrumb_html += '        <span class="separator">/</span>\n'

    # Last item (current page)
    breadcrumb_html += f'        <span class="current">{levels[-1][0]}</span>\n'
    breadcrumb_html += '''      </nav>
    </div>
  </div>
'''
    return breadcrumb_html

def create_breadcrumb_schema(levels: list, full_url: str) -> str:
    """Create BreadcrumbList schema"""
    schema = '''
  <!-- Breadcrumb Schema -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
'''

    items = []
    for i, (name, url) in enumerate(levels, 1):
        item = f'''      {{
        "@type": "ListItem",
        "position": {i},
        "name": "{name}",
        "item": "https://vyceralsolutions.com/{url}"
      }}'''
        items.append(item)

    schema += ',\n'.join(items)
    schema += '''
    ]
  }
  </script>
'''
    return schema

def create_article_schema(title: str, description: str, url_path: str) -> str:
    """Create Article schema for blog posts"""
    schema = f'''
  <!-- Article Schema -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{title}",
    "description": "{description}",
    "image": "https://vyceralsolutions.com/images/logo_vs_clear.png",
    "author": {{
      "@type": "Person",
      "name": "Vikram Ekambaram",
      "url": "https://vyceralsolutions.com/about.html"
    }},
    "publisher": {{
      "@type": "Organization",
      "name": "Vyceral Solutions LLC",
      "logo": {{
        "@type": "ImageObject",
        "url": "https://vyceralsolutions.com/images/logo_vs_clear.png"
      }}
    }},
    "datePublished": "2024-11-01",
    "dateModified": "2024-11-27",
    "mainEntityOfPage": {{
      "@type": "WebPage",
      "@id": "https://vyceralsolutions.com/{url_path}"
    }}
  }}
  </script>
'''
    return schema

def create_collection_schema(category_name: str, description: str, url_path: str) -> str:
    """Create CollectionPage schema for category pages"""
    schema = f'''
  <!-- CollectionPage Schema -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "{category_name}",
    "description": "{description}",
    "url": "https://vyceralsolutions.com/{url_path}",
    "publisher": {{
      "@type": "Organization",
      "name": "Vyceral Solutions LLC",
      "logo": {{
        "@type": "ImageObject",
        "url": "https://vyceralsolutions.com/images/logo_vs_clear.png"
      }}
    }}
  }}
  </script>
'''
    return schema

def process_blog_file(file_path: Path, dry_run: bool = False) -> Tuple[bool, str]:
    """Process a single blog HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if already has canonical tag
        if '<link rel="canonical"' in content:
            return False, "Already has canonical tag, skipping"

        # Get category and determine file type
        category_slug = get_category_from_path(file_path)
        if not category_slug:
            return False, "Could not determine category"

        category_name = CATEGORY_NAMES.get(category_slug, category_slug)
        is_category = is_category_page(file_path)

        # Calculate URL path relative to site root
        url_path = str(file_path).replace(str(Path.cwd()) + '/', '')

        # Extract metadata
        title = extract_title(content)
        description = extract_description(content)

        # Build breadcrumb levels
        if is_category:
            levels = [
                ("Home", ""),
                ("Blog", "blog.html"),
                (category_name, url_path)
            ]
        else:
            levels = [
                ("Home", ""),
                ("Blog", "blog.html"),
                (category_name, f"blog/{category_slug}/index.html"),
                (title, url_path)
            ]

        # Create SEO elements
        canonical = create_canonical_tag(url_path)
        breadcrumb_html = create_breadcrumb_html(levels)
        breadcrumb_schema = create_breadcrumb_schema(levels, url_path)

        if is_category:
            content_schema = create_collection_schema(category_name, description, url_path)
        else:
            content_schema = create_article_schema(title, description, url_path)

        # Insert canonical tag after <title> tag
        title_pattern = r'(<title>.*?</title>)'
        if re.search(title_pattern, content, re.IGNORECASE | re.DOTALL):
            content = re.sub(
                title_pattern,
                r'\1\n' + canonical,
                content,
                count=1,
                flags=re.IGNORECASE | re.DOTALL
            )
        else:
            return False, "Could not find <title> tag"

        # Insert breadcrumb HTML after </nav>
        nav_pattern = r'(</nav>)'
        if re.search(nav_pattern, content, re.IGNORECASE):
            content = re.sub(
                nav_pattern,
                r'\1\n' + breadcrumb_html,
                content,
                count=1,
                flags=re.IGNORECASE
            )
        else:
            return False, "Could not find </nav> tag"

        # Insert schemas before </head>
        head_pattern = r'(\s*<script>!function\(key\).*?</script>)\s*</head>'
        if re.search(head_pattern, content, re.IGNORECASE | re.DOTALL):
            content = re.sub(
                head_pattern,
                breadcrumb_schema + content_schema + r'\n\1\n</head>',
                content,
                count=1,
                flags=re.IGNORECASE | re.DOTALL
            )
        else:
            # Fallback: insert before </head>
            content = re.sub(
                r'</head>',
                breadcrumb_schema + content_schema + '\n</head>',
                content,
                count=1,
                flags=re.IGNORECASE
            )

        if not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

        return True, f"✓ Processed {'category' if is_category else 'article'}: {title}"

    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    """Main execution"""
    import sys

    dry_run = '--dry-run' in sys.argv
    test_mode = '--test' in sys.argv

    if dry_run:
        print("DRY RUN MODE - No files will be modified\n")

    blog_dir = Path('blog')

    # Find all HTML files, excluding articles-raw
    all_files = []
    for category_dir in blog_dir.iterdir():
        if category_dir.is_dir() and category_dir.name != 'articles-raw':
            for html_file in category_dir.glob('*.html'):
                all_files.append(html_file)

    if test_mode:
        # Test mode: process only 3 files (1 category, 2 articles)
        category_files = [f for f in all_files if f.name == 'index.html']
        article_files = [f for f in all_files if f.name != 'index.html']

        all_files = category_files[:1] + article_files[:2]
        print(f"TEST MODE - Processing only {len(all_files)} files:\n")

    all_files.sort()

    success_count = 0
    skip_count = 0
    error_count = 0

    for file_path in all_files:
        success, message = process_blog_file(file_path, dry_run=dry_run)

        if success:
            print(f"✓ {file_path}: {message}")
            success_count += 1
        elif "Already has" in message or "skipping" in message.lower():
            print(f"○ {file_path}: {message}")
            skip_count += 1
        else:
            print(f"✗ {file_path}: {message}")
            error_count += 1

    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Processed: {success_count}")
    print(f"  Skipped: {skip_count}")
    print(f"  Errors: {error_count}")
    print(f"  Total: {len(all_files)}")

    if dry_run:
        print(f"\nDRY RUN - No files were actually modified")
        print(f"Run without --dry-run to apply changes")

    if test_mode:
        print(f"\nTEST MODE - Only processed sample files")
        print(f"Remove --test flag to process all files")

if __name__ == '__main__':
    main()
