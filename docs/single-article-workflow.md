# Single Article Publishing Workflow

## Complete Automated Publishing System

**Zero manual steps required** - Just drop a file and run one command!

---

## Your Publishing Workflow

### Step 1: Create & Publish on LinkedIn
1. Write article on LinkedIn
2. Create hero image in Nanao Banana
3. Publish to LinkedIn newsletter

### Step 2: Extract Article
Run this JavaScript in Chrome console on the LinkedIn newsletter page:

```javascript
(() => {
  // Extract metadata
  const title = document.querySelector('[data-scaffold-immersive-reader-title]')?.textContent?.trim() || 'Untitled';
  const author = document.querySelector('.reader-author-info__author-lockup--flex a h2')?.textContent?.trim() || '';
  const date = document.querySelector('.reader-author-info__container time')?.textContent?.trim() || '';
  const coverImg = document.querySelector('.reader-cover-image__wrapper-right-rail-layout img')?.src || '';

  // Extract body content
  const contentContainer = document.querySelector('.reader-content-blocks-container');
  let bodyHtml = '';

  if (contentContainer) {
    contentContainer.querySelectorAll('p, blockquote, .reader-image-block img').forEach(el => {
      if (el.tagName === 'P') {
        const text = el.innerHTML
          .replace(/<!---->/g, '')
          .replace(/<span class="white-space-pre">\s*<\/span>/g, ' ')
          .trim();
        if (text && text !== '<br>') {
          bodyHtml += `  <p>${text}</p>\n\n`;
        }
      } else if (el.tagName === 'BLOCKQUOTE') {
        const text = el.innerHTML
          .replace(/<!---->/g, '')
          .replace(/<span class="white-space-pre">\s*<\/span>/g, ' ')
          .trim();
        bodyHtml += `  <blockquote>${text}</blockquote>\n\n`;
      } else if (el.tagName === 'IMG') {
        bodyHtml += `  <figure>\n    <img src="${el.src}" alt="Article image">\n  </figure>\n\n`;
      }
    });
  }

  // Build clean HTML
  const cleanHtml = `<article>
  <header>
    <h1>${title}</h1>
    <p class="meta">
      <span class="author">${author}</span>
      <time>${date}</time>
    </p>
${coverImg ? `    <img src="${coverImg}" alt="Cover image" class="cover-image">\n` : ''}  </header>

${bodyHtml}</article>`;

  // Create filename from title
  const filename = title
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
    .substring(0, 50) + '.html';

  // Download
  const blob = new Blob([cleanHtml], { type: 'text/html' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);

  console.log(`✅ Downloaded: ${filename}`);
})();
```

**Result**: HTML file downloads to `~/Downloads/{slug}.html`

### Step 3: Move to Inbox
```bash
mv ~/Downloads/{slug}.html blog/new-articles/
```

### Step 4: Run Publishing Script
```bash
cd blog && source venv/bin/activate && python3 add_article.py --category personal-journey
```

**That's it!** Everything else is 100% automated.

---

## What Gets Automatically Updated

### Files Created (2):
1. **Article HTML Page**
   - `blog/{category}/{slug}.html`
   - Full article with navigation, breadcrumbs, content, styling

2. **Hero Image**
   - `images/article-images/{slug}.jpg`
   - Downloaded from LinkedIn CDN (~1-2MB)

### Files Updated (4):
3. **Master Article Index**
   - `blog/converted-articles.json`
   - New article added at beginning (sorted by date)
   - Total count updated

4. **Metadata Index**
   - `blog/articles-metadata.json`
   - Article metadata stored (title, date, word count, etc.)

5. **Category Index Page**
   - `blog/{category}/index.html`
   - Regenerated with new article at top
   - Article count updated

6. **Blog Homepage**
   - `blog.html`
   - New article added to "Latest Articles" grid
   - Maintains 6 most recent articles
   - Oldest article automatically removed

### Files Regenerated (8):
7-14. **All Category Index Pages**
   - All 8 category indexes regenerated for consistency:
     - `blog/ai-agents/index.html`
     - `blog/ai-philosophy/index.html`
     - `blog/gtm-strategy/index.html`
     - `blog/industry-research/index.html`
     - `blog/personal-journey/index.html`
     - `blog/practical-applications/index.html`
     - `blog/technical-analysis/index.html`
     - `blog/tools-platforms/index.html`

### Files Deleted (1):
15. **Source File**
   - `blog/new-articles/{slug}.html`
   - Deleted after successful processing
   - Folder left empty for next article

---

## Complete Update List

### Automatic Updates: **15 items**
- ✅ 1 article page created
- ✅ 1 hero image downloaded
- ✅ 2 JSON files updated
- ✅ 1 category index regenerated
- ✅ 1 blog homepage updated
- ✅ 8 category indexes regenerated
- ✅ 1 source file deleted

### Manual Updates: **0 items**
- 🎉 Fully automated!

---

## Available Categories

Use the category slug with `--category` flag:

| Slug | Name | Icon | Current Count |
|------|------|------|---------------|
| `ai-agents` | AI Agents | 🤖 | 15 articles |
| `ai-philosophy` | AI Philosophy | 🧠 | 10 articles |
| `gtm-strategy` | GTM Strategy | 🎯 | 11 articles |
| `industry-research` | Industry Research | 🏭 | 3 articles |
| `personal-journey` | Personal Journey | 🚀 | 13 articles |
| `practical-applications` | Practical Applications | 💡 | 26 articles |
| `technical-analysis` | Technical Analysis | ⚙️ | 5 articles |
| `tools-platforms` | Tools & Platforms | 🛠️ | 12 articles |

---

## Script Output Example

```
🔍 Checking blog/new-articles/ for article...
✓ Found: two-years-of-content-completely-invisible-here-s-h.html

📄 Parsing article...
✓ Title: "Two Years of Content. Completely Invisible. Here's How I Fixed It."
✓ Date: November 25, 2025
✓ Author: Vikram Ekambaram
✓ Words: 719
✓ Read time: 4 min
✓ Slug: two-years-of-content-completely-invisible-here-s-h

📁 Category: 🚀 Personal Journey
   (from --category flag)

📥 Downloading hero image...
✓ Saved to: images/article-images/two-years-of-content-completely-invisible-here-s-h.jpg

📝 Generating article page...
✓ Created: blog/personal-journey/two-years-of-content-completely-invisible-here-s-h.html

📊 Updating indexes...
✓ Updated: blog/converted-articles.json (95 total articles)
✓ Updated: blog/articles-metadata.json
✓ Regenerated: blog/personal-journey/index.html (13 articles)
✓ Updated: blog.html (latest articles)

🗑️  Cleaning up...
✓ Deleted: /path/to/blog/new-articles/two-years-of-content-completely-invisible-here-s-h.html
✓ Folder blog/new-articles/ is ready for next article

✅ Article published successfully!

📋 Next Steps:
1. Review article: blog/personal-journey/two-years-of-content-completely-invisible-here-s-h.html
2. Commit to git:
   git add blog/personal-journey/
   git add blog.html
   git add images/article-images/two-years-of-content-completely-invisible-here-s-h.jpg
   git add blog/converted-articles.json
   git add blog/articles-metadata.json
   git commit -m "Add article: Two Years of Content. Completely Invisible..."
   git push
```

---

## Additional Options

### Interactive Category Selection
If you don't specify `--category`, the script will prompt you:

```bash
python3 add_article.py

? Select category:
  1. 🤖 AI Agents
  2. 🧠 AI Philosophy
  3. 🎯 GTM Strategy
  4. 🏭 Industry Research
  5. 🚀 Personal Journey
  6. 💡 Practical Applications
  7. ⚙️ Technical Analysis
  8. 🛠️ Tools & Platforms

Enter number (1-8):
```

### Dry Run Mode
Preview what will happen without making changes:

```bash
python3 add_article.py --category ai-agents --dry-run

🏃 DRY RUN MODE - No changes will be made

Would perform:
  - Download image to: images/article-images/article-slug.jpg
  - Create article: blog/ai-agents/article-slug.html
  - Update: blog/converted-articles.json
  - Update: blog/articles-metadata.json
  - Regenerate: blog/ai-agents/index.html
  - Update: blog.html (add to latest articles)
  - Delete: blog/new-articles/article-slug.html
```

### Skip Image Download
If you've already manually added the hero image:

```bash
python3 add_article.py --category personal-journey --skip-image
```

---

## Error Handling

### No File in Inbox
```
❌ Error: No article found in blog/new-articles/
   Please add an HTML file to blog/new-articles/
```

### Multiple Files in Inbox
```
❌ Error: Found 2 files in blog/new-articles/
   Please process one article at a time.

   Files found:
   - article-one.html
   - article-two.html
```

### Invalid Category
```
❌ Error: Unknown category 'invalid-category'

   Valid categories:
   - ai-agents: 🤖 AI Agents
   - ai-philosophy: 🧠 AI Philosophy
   - gtm-strategy: 🎯 GTM Strategy
   ... etc
```

### Image Download Failed
```
⚠️  Warning: Failed to download image: [error message]
   You can manually add it to: images/article-images/slug.jpg
```
*Note: Script continues processing, article still published*

---

## Where Articles Appear

After running the script, your article is immediately live on:

### 1. Individual Article Page
- **URL**: `https://vyceralsolutions.com/blog/{category}/{slug}.html`
- Full article with hero image, content, navigation
- Breadcrumbs: Home > Blog > Category > Article
- Related CTAs at bottom

### 2. Category Index Page
- **URL**: `https://vyceralsolutions.com/blog/{category}/index.html`
- Shows as first article (newest at top)
- Includes hero image thumbnail
- Category count updated

### 3. Blog Homepage
- **URL**: `https://vyceralsolutions.com/blog.html`
- Shows in "Latest Articles" grid (first position)
- Only 6 most recent articles shown
- Hero image and category badge included

### 4. Master Index (for programmatic access)
- **File**: `blog/converted-articles.json`
- Searchable, sortable list of all articles
- Used by search engines and future features

---

## Performance

- **Processing Time**: ~10 seconds
- **Image Download**: ~2-3 seconds (depends on size)
- **Total Time**: ~12-15 seconds from command to published

**100% Automated** - No manual intervention required!

---

## Troubleshooting

### Script Doesn't Find Article
- Check file is in `blog/new-articles/`
- Check file has `.html` extension
- Only one file should be in the folder

### Category Index Not Updated
- Category indexes regenerate automatically
- Check `blog/{category}/index.html` modified timestamp
- Re-run script if needed

### Blog.html Not Updated
- Check for BeautifulSoup parsing errors in output
- Verify `blog.html` has `<div class="grid grid-2">` structure
- Check file permissions

### Image Not Showing
- Verify image downloaded to correct path
- Check LinkedIn CDN URL is valid (may expire)
- Use `--skip-image` and add manually if needed

---

## Git Workflow

After publishing, commit your changes:

```bash
# Add all updated files
git add blog/{category}/
git add blog.html
git add images/article-images/{slug}.jpg
git add blog/converted-articles.json
git add blog/articles-metadata.json

# Commit with descriptive message
git commit -m "Add article: {title}"

# Push to remote
git push
```

**Pro tip**: The script output includes the exact git commands you need to run!

---

## System Requirements

- Python 3.8+
- Virtual environment with dependencies:
  - `beautifulsoup4`
  - (installed in `blog/venv/`)

---

## File Locations Reference

| What | Where |
|------|-------|
| Inbox (drop zone) | `blog/new-articles/` |
| Publishing script | `blog/add_article.py` |
| Article template | `blog/article-template.html` |
| Generated articles | `blog/{category}/{slug}.html` |
| Hero images | `images/article-images/{slug}.jpg` |
| Master index | `blog/converted-articles.json` |
| Metadata | `blog/articles-metadata.json` |
| Category indexes | `blog/{category}/index.html` |
| Blog homepage | `blog.html` |

---

## Summary

**Your Steps**:
1. Write on LinkedIn
2. Run console script (downloads HTML)
3. Move to `blog/new-articles/`
4. Run `python3 add_article.py --category {category}`

**Automated**:
- ✅ Extract content & metadata
- ✅ Download hero image
- ✅ Generate article page
- ✅ Update category index
- ✅ Update blog homepage
- ✅ Update master indexes
- ✅ Regenerate all category pages
- ✅ Clean up source file

**Result**: Fully published article across your entire website in ~15 seconds!

---

**Last Updated**: November 25, 2025
**Version**: 2.0 (Fully Automated)
