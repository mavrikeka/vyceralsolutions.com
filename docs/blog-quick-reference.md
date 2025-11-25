# Blog System Quick Reference

## Common Tasks

### Adding New Articles from LinkedIn

```bash
# 1. Export LinkedIn article as HTML
# Save to: blog/articles-raw/article-name-vikram-ekambaram-hash.html

# 2. Convert articles
cd blog
source venv/bin/activate
python3 convert_articles.py

# 3. Update category indexes
python3 create_category_indexes.py

# 4. Update blog landing page
python3 generate_blog_page.py
# Copy output from blog/featured-articles.html to blog.html

# 5. Add hero image
# Save as: images/article-images/{slug}.jpg
```

### Finding Article Information

```bash
# See all converted articles
cat blog/converted-articles.json | grep -A5 "title"

# Find articles by category
cat blog/converted-articles.json | grep -B2 "ai-agents"

# Check conversion stats
python3 convert_articles.py  # Shows category distribution
```

### Fixing Issues

```bash
# Find missing images
python3 blog/fix_missing_hero_images.py

# Regenerate all articles with updated template
python3 blog/regenerate_all_with_mapping.py

# Regenerate category indexes
python3 blog/create_category_indexes.py
```

## File Locations

| What | Where |
|------|-------|
| Raw LinkedIn articles | `blog/articles-raw/*.html` |
| Converted articles | `blog/{category}/{slug}.html` |
| Article template | `blog/article-template.html` |
| Hero images | `images/article-images/{slug}.jpg` |
| Article index | `blog/converted-articles.json` |
| Blog landing page | `blog.html` |
| Category indexes | `blog/{category}/index.html` |

## Categories

| Slug | Name | Description |
|------|------|-------------|
| `ai-agents` | AI Agents & Agentic Systems | Autonomous agents, Anthropic, Claude, MCP |
| `ai-philosophy` | AI Philosophy & Future of Work | AI ethics, organizational transformation |
| `gtm-strategy` | Business & GTM Strategy | Go-to-market, sales, customer success |
| `industry-research` | Industry Research & Insights | Industry-specific AI analysis |
| `personal-journey` | Personal Journey & Entrepreneurship | Personal stories, business setup |
| `practical-applications` | Practical Applications & Use Cases | Tutorials, how-tos, implementations |
| `technical-analysis` | Technical Deep Dives & Analysis | Architecture, APIs, technical details |
| `tools-platforms` | GenAI Tools & Platforms | Tools, platforms, technologies |

## Python Scripts

| Script | Purpose |
|--------|---------|
| `convert_articles.py` | Main conversion script - extracts and converts LinkedIn articles |
| `create_category_indexes.py` | Generates index.html for each category folder |
| `generate_blog_page.py` | Generates featured articles HTML for blog.html |
| `fix_missing_hero_images.py` | Identifies articles missing hero images |
| `regenerate_all_with_mapping.py` | Regenerates all articles with current template |
| `add_images_to_indexes.py` | Adds image wrappers to category index pages |

## Article URL Structure

```
Homepage:           vyceralsolutions.com/blog.html
Category Index:     vyceralsolutions.com/blog/ai-agents/index.html
Individual Article: vyceralsolutions.com/blog/ai-agents/autonomous-agents-it-all-started-with-manus.html
```

## Key Data Files

**converted-articles.json**
```json
{
  "title": "Article Title",
  "slug": "article-slug",
  "category": "category-slug",
  "date": "2025-03-13",
  "read_time": 5,
  "path": "blog/category/slug.html"
}
```

**Template Variables**
- `{{TITLE}}` - Article title
- `{{DATE}}` - Formatted date
- `{{CATEGORY}}` - Category display name
- `{{CATEGORY_SLUG}}` - Category URL slug
- `{{READ_TIME}}` - Minutes to read
- `{{CONTENT}}` - Article HTML
- `{{SLUG}}` - Article slug (for images)
- `{{META_DESCRIPTION}}` - SEO description

## Workflow Diagram

```
LinkedIn Article (HTML)
    ↓
blog/articles-raw/*.html
    ↓
convert_articles.py
    ↓
blog/{category}/{slug}.html
    ↓
create_category_indexes.py
    ↓
blog/{category}/index.html
    ↓
generate_blog_page.py
    ↓
blog/featured-articles.html → (manual) → blog.html
```

## Quick Commands

```bash
# Activate Python environment
cd blog && source venv/bin/activate

# Full rebuild
python3 convert_articles.py && \
python3 create_category_indexes.py && \
python3 generate_blog_page.py

# Count articles by category
cat converted-articles.json | grep '"category"' | sort | uniq -c

# List newest articles
cat converted-articles.json | grep -E '"title"|"date"' | head -20

# Find article by title
cat converted-articles.json | grep -B1 -A5 "Manus"
```

## Troubleshooting Checklist

- [ ] Article contains "GenAI for Go-To-Market teams"?
- [ ] File saved in `blog/articles-raw/`?
- [ ] Python venv activated?
- [ ] Scripts run without errors?
- [ ] Hero image matches slug exactly?
- [ ] Image is JPG format?
- [ ] Featured articles copied to blog.html?
- [ ] Category folder exists?
- [ ] Git committed changes?

---

**Pro Tip**: Always run `convert_articles.py` before `create_category_indexes.py` to ensure category pages have latest articles.
