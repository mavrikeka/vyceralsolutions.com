# Blog System Technical Implementation Details

## Content Extraction Pipeline

### LinkedIn HTML Structure

LinkedIn article exports have this general structure:

```html
<!DOCTYPE html>
<html>
<head>
  <title>Article Title - Vikram Ekambaram</title>
</head>
<body>
  <h1><a href="...">Article Title</a></h1>
  <p class="created">Created on 2025-01-15 14:30</p>
  <p class="published">Published on 2025-01-15 14:30</p>
  <div>
    <!-- Article content -->
    <p>First paragraph...</p>
    <figure>
      <img src="https://media.licdn.com/...">
    </figure>
    <!-- More content -->
  </div>
</body>
</html>
```

### Extraction Logic (convert_articles.py)

**Title Extraction**
```python
# Priority order:
1. <h1><a>text</a></h1>  # More reliable formatting
2. <title>text</title>    # Fallback
```

**Date Extraction**
```python
# Try published date first
published_tag = soup.find('p', class_='published')
date_text = published_tag.text.replace('Published on', '').strip()
published = datetime.strptime(date_text, '%Y-%m-%d %H:%M')

# Fallback to created date
if not published:
    created_tag = soup.find('p', class_='created')
    # Parse similarly
```

**Content Extraction**
```python
# Strategy: Get last div in body (contains article content)
body_content = soup.find('body')
all_divs = body_content.find_all('div', recursive=False)
content_div = all_divs[-1]  # Last div has article content

# Alternative: Find all siblings after h1
for sibling in h1.find_next_siblings():
    if sibling.name:
        content_parts.append(str(sibling))
```

**Read Time Calculation**
```python
text_content = soup.get_text()
word_count = len(text_content.split())
read_time = max(1, round(word_count / 200))  # 200 WPM standard
```

## Categorization System

### Keyword-Based Categorization

The fallback categorization uses keyword matching:

```python
def categorize_article_fallback(title, content):
    title_lower = title.lower()
    content_lower = content.lower()[:1000]  # First 1000 chars

    # Define keyword sets
    gtm_keywords = ['gtm', 'sales', 'pipeline', 'crm', 'customer success']
    agent_keywords = ['agent', 'autonomous', 'anthropic', 'claude']
    # ... etc

    # Score each category
    scores = {
        'gtm-strategy': sum(1 for kw in gtm_keywords
                           if kw in title_lower or kw in content_lower),
        'ai-agents': sum(1 for kw in agent_keywords
                        if kw in title_lower or kw in content_lower),
        # ... etc
    }

    # Return highest scoring category
    max_category = max(scores.items(), key=lambda x: x[1])
    return max_category[0] if max_category[1] > 0 else 'strategy'
```

### AI Categorization (Disabled)

The original implementation used an API for smarter categorization:

```python
def categorize_article(title, content):
    # Get text preview
    soup = BeautifulSoup(content, 'html.parser')
    text_preview = soup.get_text()[:2000]

    # Define categories with descriptions
    categories_desc = """
    - gtm-automation: Go-to-market, sales, account planning, CRM
    - ai-agents: AI agents, Anthropic, Claude, MindStudio
    # ... etc
    """

    # Call AI API with prompt
    instructions = f"""Categorize this article into ONE category:
    {categories_desc}

    Title: {title}
    Content: {text_preview}

    Respond with only the category slug."""

    # API call (removed for security)
    # response = requests.post(api_url, json={...})
```

## Template Processing

### Variable Replacement

Simple string replacement with validation:

```python
def generate_article_html(metadata, template):
    slug = create_slug(metadata['title'])
    date_str = metadata['date'].strftime('%B %d, %Y')
    category_name = CATEGORIES.get(metadata['category'], 'Insights')

    # Create meta description
    soup = BeautifulSoup(content_html, 'html.parser')
    text_content = soup.get_text()
    first_para = ' '.join(text_content.split()[:30])
    meta_description = first_para[:155] + "..."

    # Replace all variables
    html = template
    html = html.replace('{{TITLE}}', metadata['title'])
    html = html.replace('{{DATE}}', date_str)
    html = html.replace('{{CATEGORY}}', category_name)
    html = html.replace('{{SLUG}}', slug)
    # ... etc

    return slug, html
```

### Slug Generation

URL-safe slug creation:

```python
def create_slug(title):
    # Remove special characters
    slug = re.sub(r'[^\w\s-]', '', title.lower())

    # Replace spaces with hyphens
    slug = re.sub(r'[-\s]+', '-', slug)

    # Limit length
    return slug[:80]
```

**Examples**:
- "Autonomous Agents - It all started with Manus!!" → `autonomous-agents-it-all-started-with-manus`
- "Can GenAI help with Account Research?" → `can-genai-help-with-account-research`

## Category Index Generation

### Template System

The category index uses a template string with placeholders:

```python
TEMPLATE = '''<!DOCTYPE html>
<html>
<head>
  <title>{{CATEGORY_NAME}} | Vyceral Solutions Blog</title>
  <meta name="description" content="{{DESCRIPTION}}">
</head>
<body>
  <h1>{{ICON}} {{CATEGORY_NAME}}</h1>
  <p>{{DESCRIPTION}}</p>
  <p>{{ARTICLE_COUNT}} articles</p>

  <div class="grid">
    {{ARTICLE_CARDS}}
  </div>
</body>
</html>'''
```

### Card Generation

Individual article cards:

```python
CARD_TEMPLATE = '''<div class="card">
  <img src="{{IMAGE_PATH}}">
  <span class="badge">{{CATEGORY_NAME}}</span>
  <span>{{DATE}}</span>
  <h3>{{TITLE}}</h3>
  <p>📖 {{READ_TIME}} min read</p>
  <a href="{{SLUG}}.html">Read Article →</a>
</div>'''

# Generate cards for category
cards_html = []
for article in cat_articles:
    card = CARD_TEMPLATE
    card = card.replace('{{TITLE}}', article['title'])
    card = card.replace('{{SLUG}}', article['slug'])
    # ... etc
    cards_html.append(card)

# Insert into template
html = TEMPLATE.replace('{{ARTICLE_CARDS}}', '\n'.join(cards_html))
```

### Sorting

Articles sorted by date (newest first):

```python
# In create_category_indexes.py
cat_articles = articles_by_category[cat_slug]

# Sort by date - newest first
cat_articles.sort(key=lambda x: x['date'], reverse=True)
```

## Data File Management

### JSON Schema

**converted-articles.json**
```json
[
  {
    "title": "string",          // Article title
    "slug": "string",            // URL-safe slug
    "category": "string",        // Category slug
    "category_name": "string",   // Display name
    "date": "ISO datetime",      // Publication date
    "read_time": number,         // Minutes
    "path": "string"             // Relative path to HTML
  }
]
```

**articles-metadata.json**
```json
[
  {
    "title": "string",
    "date": "ISO datetime",
    "category": "string",
    "read_time": number,
    "word_count": number,
    "source_file": "string"      // Original filename
  }
]
```

### File Operations

```python
# Save JSON with proper serialization
with open('blog/converted-articles.json', 'w') as f:
    json.dump(converted_articles, f, indent=2, default=str)
    # default=str handles datetime objects

# Load JSON
with open('blog/converted-articles.json', 'r') as f:
    articles = json.load(f)
```

## Image Handling

### Hero Images

Articles reference hero images:

```html
<!-- In article template -->
<div class="article-hero-image">
  <img src="../../images/article-images/{{SLUG}}.jpg"
       alt="{{TITLE}}"
       onerror="this.parentElement.style.display='none'">
</div>
```

**Graceful Degradation**:
- `onerror` handler hides entire div if image missing
- No broken image icons shown
- Article still displays properly

### Image Paths

- **From article**: `../../images/article-images/{slug}.jpg`
- **From category index**: `../../images/article-images/{slug}.jpg`
- **From blog.html**: `images/article-images/{slug}.jpg`

All paths are relative and work with static hosting.

## Build Process

### Full Conversion Flow

```python
# convert_articles.py main() function

1. Find all LinkedIn HTML files in articles-raw/
2. Filter for "GenAI for Go-To-Market teams" articles
3. For each article:
   a. Extract metadata (title, date, content)
   b. Categorize using keyword matching
   c. Calculate read time
4. Sort by date (newest first)
5. Save metadata to articles-metadata.json
6. For each article:
   a. Generate slug from title
   b. Load template
   c. Replace template variables
   d. Write HTML to blog/{category}/{slug}.html
7. Save index to converted-articles.json
```

### Incremental Updates

The system is designed for full rebuilds, not incremental:

**Limitations**:
- Re-running converts ALL articles
- Manual edits to HTML are overwritten
- No version control for article updates

**Workaround**:
- Don't edit generated HTML directly
- Edit raw files or template instead
- Use git to track changes

## Performance Considerations

### Processing Speed

For ~81 articles:
- Extraction: ~2-3 seconds
- Categorization: ~1-2 seconds (keyword-based)
- HTML Generation: ~1-2 seconds
- **Total: ~5-7 seconds**

### Optimization Opportunities

1. **Parallel Processing**
   ```python
   # Could use multiprocessing for article conversion
   from multiprocessing import Pool

   with Pool() as pool:
       results = pool.map(convert_article, article_files)
   ```

2. **Incremental Updates**
   ```python
   # Check if article already converted and unchanged
   if article_unchanged(file_path):
       skip_conversion()
   ```

3. **Template Caching**
   ```python
   # Load template once, reuse for all articles
   template = load_template_once()
   for article in articles:
       generate_html(article, template)
   ```

## Error Handling

### Common Errors

1. **Missing Date**
   ```python
   # Falls back to datetime.min for sorting
   articles.sort(key=lambda x: x['date'] if x['date'] else datetime.min)
   ```

2. **Malformed HTML**
   ```python
   try:
       metadata = extract_article_metadata(file_path)
   except Exception as e:
       print(f"Error processing {file_path.name}: {e}")
       continue  # Skip to next article
   ```

3. **Invalid Category**
   ```python
   # Default to 'strategy' if no keywords match
   category = categorize_article(title, content)
   if not category:
       category = 'strategy'
   ```

## Security Considerations

### Input Validation

LinkedIn HTML is trusted input (exported manually):
- No XSS risk (content from trusted source)
- No SQL injection (no database)
- File paths are controlled (slugs sanitized)

### API Key Management

Original design used AI API:
```python
# API key was in code - REMOVED for security
# Now using keyword-based fallback
# If re-enabling: Use environment variables
api_key = os.getenv('AI_API_KEY')
```

## Dependencies

### Python Packages

```
beautifulsoup4==4.12.x  # HTML parsing
requests==2.31.x        # HTTP requests (if using AI API)
```

### System Requirements

- Python 3.8+
- Virtual environment recommended
- No database required
- No external services (except optional AI API)

## Testing Approach

### Manual Testing Checklist

1. Add test article to `articles-raw/`
2. Run conversion: `python3 convert_articles.py`
3. Check output:
   - HTML file created in correct category
   - Template variables replaced
   - Content formatting preserved
4. Check category index updated
5. Check featured articles includes new article (if recent)
6. Verify image reference correct
7. Test in browser

### Validation Scripts

```python
# Check for broken links
for article in articles:
    check_internal_links(article['path'])

# Verify all articles have images
for article in articles:
    image_path = f"images/article-images/{article['slug']}.jpg"
    if not os.path.exists(image_path):
        print(f"Missing image: {image_path}")
```

## Deployment

### Static Site Deployment

1. Generate all files locally
2. Commit to git
3. Deploy entire site (including blog/)
4. No server-side processing required
5. Works with any static host (Netlify, Vercel, GitHub Pages)

### Git Workflow

```bash
# After running scripts
git add blog/
git add images/article-images/
git add blog.html
git commit -m "Add new blog articles"
git push
```

---

**Last Updated**: November 25, 2025
**Technical Version**: 1.0
