# Single Article Ingestion Plan

## Current State Analysis

### Existing System (Batch Migration)
- **Purpose**: One-time migration of 93 LinkedIn articles
- **Input**: Raw LinkedIn HTML exports in `blog/articles-raw/`
- **Process**: Batch conversion via `convert_articles.py`
- **Output**: All 81+ articles converted at once

### New Workflow Requirements

**Your Publishing Process**:
1. Write article on LinkedIn
2. Create hero image in Nanao Banana (AI image generator)
3. Publish to LinkedIn newsletter
4. Run JavaScript console code on newsletter page
5. Downloads clean HTML file to `~/Downloads/{slug}.html`

**What We Need to Build**:
- Single-article ingestion script
- Extract content from new HTML format
- Download/save hero image from LinkedIn CDN
- Categorize article (AI or manual)
- Generate article HTML page
- Update blog.html (add to featured articles)
- Update category index page
- Update converted-articles.json
- Maintain article counts

## New HTML Structure Analysis

### From Console Extraction Script

```html
<article>
  <header>
    <h1>Article Title</h1>
    <p class="meta">
      <span class="author">Vikram Ekambaram</span>
      <time>November 25, 2025</time>
    </p>
    <img src="[LinkedIn CDN URL]" alt="Cover image" class="cover-image">
  </header>

  <p>Paragraph content...</p>
  <blockquote>Quote content...</blockquote>
  <figure>
    <img src="[LinkedIn CDN URL]" alt="Article image">
  </figure>
  <!-- More content -->
</article>
```

**Key Differences from Old Format**:
- ✅ Clean HTML structure (no LinkedIn cruft)
- ✅ Explicit metadata in header
- ✅ Cover image URL available
- ✅ Inline images included
- ❌ No "GenAI for Go-To-Market teams" identifier
- ❌ No category information
- ❌ No read time calculation

## Proposed Single-Article Workflow

### Step 1: User Actions
```
1. Write article on LinkedIn
2. Create hero image in Nanao Banana
3. Publish to LinkedIn newsletter
4. Run console script on LinkedIn newsletter page
5. Downloads to: ~/Downloads/{auto-generated-slug}.html
6. Move file to: blog/new-articles/{slug}.html
7. Run: python3 blog/add_article.py --category ai-agents
   (Script auto-finds the single file in new-articles/)
```

### Step 2: Script Actions (`add_article.py`)

**Find & Validate**:
1. Check `blog/new-articles/` for files
   - 0 files → Error: "No article found"
   - 1 file → Proceed
   - 2+ files → Error: "Multiple articles found. Process one at a time."
2. Use filename as slug

**Extract & Process**:
1. Parse HTML file from `blog/new-articles/`
2. Extract metadata:
   - Title from `<h1>`
   - Date from `<time>`
   - Author from `<span class="author">`
   - Cover image URL from `<img class="cover-image">`
   - Content from article body
3. Calculate read time (word count / 200 WPM)
4. Generate slug from filename

**Categorization**:
- Option 1: User provides via CLI flag `--category ai-agents`
- Option 2: AI categorization (requires API)
- Option 3: Interactive prompt (user selects from list)
- **Recommended**: CLI flag with interactive fallback

**Image Handling**:
1. Download cover image from LinkedIn CDN
2. Save as: `images/article-images/{slug}.jpg`
3. Convert to JPG if needed
4. Optimize file size (optional)

**Generate Article Page**:
1. Load `blog/article-template.html`
2. Replace template variables:
   - `{{TITLE}}`: From `<h1>`
   - `{{DATE}}`: From `<time>`, formatted
   - `{{CATEGORY}}`: From user input
   - `{{SLUG}}`: Generated or from filename
   - `{{READ_TIME}}`: Calculated
   - `{{CONTENT}}`: Article body HTML
3. Save to: `blog/{category}/{slug}.html`

**Update Category Index**:
1. Load `blog/converted-articles.json`
2. Add new article entry
3. Sort by date (newest first)
4. Regenerate `blog/{category}/index.html`
5. Update article count in category page

**Update Blog Homepage**:
1. Load `blog/converted-articles.json`
2. Get 6 most recent articles
3. Generate featured article cards
4. **Option A**: Auto-update `blog.html` (risky)
5. **Option B**: Generate `blog/featured-articles.html` for manual copy
6. **Recommended**: Option B (safe, allows review)

**Update Master Index**:
1. Add new article to `blog/converted-articles.json`
2. Add metadata to `blog/articles-metadata.json`
3. Update counts in category definitions

**Cleanup**:
1. Delete processed file from `blog/new-articles/`
2. Folder is now empty and ready for next article

### Step 3: Verification
- Article page renders correctly
- Category index shows new article at top
- Featured articles includes new article (if recent enough)
- Image displays properly
- Links work (breadcrumbs, navigation)

## Proposed Directory Structure

```
blog/
├── new-articles/              # NEW: Drop zone for console-extracted HTML
│   └── {slug}.html           # File from ~/Downloads
├── articles-raw/              # OLD: Batch migration files (archive only)
├── {category}/                # Generated article pages
│   ├── index.html
│   └── {slug}.html
├── article-template.html      # Template for articles
├── converted-articles.json    # Master index
├── add_article.py             # NEW: Single-article ingestion script
└── ...
```

## Script Design: `add_article.py`

### Command-Line Interface

```bash
# Standard usage - auto-finds single file in new-articles/
python3 blog/add_article.py --category ai-agents

# Interactive category selection (if no category specified)
python3 blog/add_article.py

# Dry run (preview without changes or deletion)
python3 blog/add_article.py --category gtm-strategy --dry-run

# Skip image download (if already exists)
python3 blog/add_article.py --category ai-agents --skip-image
```

**Note**: Script always looks in `blog/new-articles/` for exactly ONE HTML file. No filename needed in CLI.

### Script Flow

```python
1. Parse CLI arguments (--category, --dry-run, --skip-image)
2. Check blog/new-articles/ folder:
   - Count HTML files
   - Error if 0 or 2+ files
   - Proceed if exactly 1 file
3. Extract metadata from HTML
4. Determine category (from flag or interactive prompt)
5. Generate slug from filename
6. Download and save hero image
7. Calculate read time
8. Generate article HTML from template
9. Add to converted-articles.json
10. Regenerate category index
11. Generate featured articles
12. Delete file from new-articles/ (unless --dry-run)
13. Show summary and next steps
```

### Error Handling

```python
- No files in new-articles/ → "No article found in blog/new-articles/. Please add an HTML file."
- Multiple files in new-articles/ → "Found {n} files. Process one article at a time."
- Invalid HTML structure → Show what's missing, don't delete file
- Image download fails → Warn but continue (manual fix later)
- Category not recognized → Show list, prompt again
- Slug collision → Append -2, -3, etc. or prompt user
- JSON corruption → Backup before modifying
- Processing error → Don't delete source file (for retry)
```

### Output Example

```
🔍 Checking blog/new-articles/ for article...
✓ Found: two-years-of-content-completely-invisible-here-s-h.html

📄 Parsing article...
✓ Title: "Two Years of Content. Completely Invisible. Here's How I Fixed It."
✓ Date: November 25, 2025
✓ Author: Vikram Ekambaram
✓ Words: 450
✓ Read time: 3 min
✓ Slug: two-years-of-content-completely-invisible-here-s-h

📁 Category: Personal Journey (from --category flag)

📥 Downloading hero image...
✓ Saved to: images/article-images/two-years-of-content-completely-invisible-here-s-h.jpg

📝 Generating article page...
✓ Created: blog/personal-journey/two-years-of-content-completely-invisible-here-s-h.html

📊 Updating indexes...
✓ Updated: blog/converted-articles.json
✓ Updated: blog/articles-metadata.json
✓ Regenerated: blog/personal-journey/index.html (14 articles → 15 articles)
✓ Generated: blog/featured-articles.html

🗑️  Cleaning up...
✓ Deleted: blog/new-articles/two-years-of-content-completely-invisible-here-s-h.html
✓ Folder blog/new-articles/ is ready for next article

✅ Article published successfully!

📋 Next Steps:
1. Review article: blog/personal-journey/two-years-of-content-completely-invisible-here-s-h.html
2. Update blog.html: Copy content from blog/featured-articles.html (optional)
3. Commit to git:
   git add blog/personal-journey/
   git add images/article-images/two-years-of-content-completely-invisible-here-s-h.jpg
   git add blog/converted-articles.json
   git add blog/articles-metadata.json
   git commit -m "Add article: Two Years of Content. Completely Invisible..."
   git push
```

## Implementation Phases

### Phase 1: Core Script (MVP)
- [ ] Parse new HTML format
- [ ] Extract metadata (title, date, content)
- [ ] Manual category selection (CLI flag)
- [ ] Generate article HTML
- [ ] Save to category folder
- [ ] Basic error handling

### Phase 2: Automation
- [ ] Download hero image from LinkedIn
- [ ] Update converted-articles.json
- [ ] Regenerate category index
- [ ] Generate featured articles HTML
- [ ] Slug generation/validation

### Phase 3: Polish
- [ ] Interactive category selection
- [ ] AI categorization option
- [ ] Image optimization
- [ ] Dry-run mode
- [ ] Better error messages
- [ ] Progress indicators

### Phase 4: Documentation
- [ ] Usage guide
- [ ] Quick reference
- [ ] Troubleshooting
- [ ] Update existing docs

## Testing Plan

### Test Article: "Two Years of Content..."
1. Use provided HTML file
2. Run through complete workflow
3. Verify all outputs:
   - Article page generated correctly
   - Image downloaded and saved
   - Category index updated
   - Featured articles updated
   - JSON files valid
   - No broken links

### Edge Cases to Test
- [ ] Article with no cover image
- [ ] Article with multiple inline images
- [ ] Very long title (>80 chars)
- [ ] Special characters in title
- [ ] Duplicate slug
- [ ] Invalid category
- [ ] Malformed HTML
- [ ] Network error during image download

## Success Criteria

- ✅ Single command adds new article
- ✅ Takes < 10 seconds to run
- ✅ No manual file editing required
- ✅ Regenerates all dependent files
- ✅ Clear error messages
- ✅ Safe (doesn't break existing articles)
- ✅ Documented workflow

## Future Enhancements

### Short Term
- Validate article before adding (preview mode)
- Auto-commit to git with generated message
- Send notification when article published

### Long Term
- Watch folder for new articles (auto-ingest)
- Integration with Nanao Banana (auto-download image)
- RSS feed auto-update
- Social media auto-post
- Analytics integration

## Migration from Batch to Single-Article

### What Stays
- `article-template.html` (same template)
- `converted-articles.json` (append to existing)
- `blog/{category}/` structure
- Category definitions
- Image naming convention

### What Changes
- `articles-raw/` → Archive only, no new files
- `convert_articles.py` → Not used for new articles
- New entry point: `add_article.py`
- New workflow documentation

### Coexistence Strategy
- Keep old batch scripts for reference
- Keep old docs in `docs/archive/`
- New articles go through `add_article.py`
- Old system still works for re-generation if needed

---

## Next Steps

1. **Review this plan** - Confirm approach
2. **Build MVP script** - `add_article.py` Phase 1
3. **Test with sample article** - "Two Years of Content..."
4. **Review generated output** - Verify all files correct
5. **Iterate and enhance** - Phases 2-3
6. **Document new workflow** - Update guides
7. **Archive old docs** - Move batch system docs to archive

---

**Plan Version**: 1.0
**Created**: November 25, 2025
**Status**: Ready for Review
