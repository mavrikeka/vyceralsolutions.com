# Publish Article

You are helping publish a new blog article to the Vyceral Solutions website. This is a comprehensive end-to-end workflow.

## Context

- This is a static website with blog articles managed via Python scripts
- Articles are sourced from LinkedIn and placed in `/blog/new-articles/`
- **Images are also placed in `/blog/new-articles/` alongside the article:**
  - `{slug}-cover.jpg` - hero/cover image
  - `{slug}-img-1.jpg`, `{slug}-img-2.jpg`, etc. - inline images
- The `add_article.py` script converts articles to the site's template format
- **After publishing, images are copied to their final locations:**
  - Cover → `/images/article-images/{slug}.jpg`
  - Inline → `/images/article-images/inline/{slug}-img-X.jpg`
- Article HTML is updated to reference local image paths (not LinkedIn CDN)
- Articles are organized into 8 categories with indexes that must be regenerated
- **Must update sitemap.xml** for every new article (critical for SEO)

## Your Task

Execute the complete blog article publishing workflow:

### Step 1: Validate Prerequisites

1. Check if there are any HTML files in `/blog/new-articles/`
2. List the files found (if any)
3. If no files found, instruct user to save LinkedIn article HTML there first and exit
4. If multiple files found, ask user which one to publish

### Step 2: Select Category

**Option A: AI-Powered Auto-Categorization (Recommended)**

1. Ask user: "Would you like AI to automatically categorize this article? (yes/no)"

2. **If yes (AI categorization)**:
   - Show message: "Analyzing article content with LLM... (this takes 30-60 seconds)"
   - Run categorization:
     ```bash
     venv/bin/python3 blog/anyquest_client.py categorize blog/new-articles/[article-filename].html
     ```
   - Wait for response (LLM will analyze and return category)
   - Capture the category from stdout (e.g., "ai-agents")
   - Show user: "✨ AI suggests: **[category]** - [Category Full Name]"
   - Ask: "Accept this categorization? (yes/no)"
     - If **yes**: Use the AI-suggested category and proceed to Step 3
     - If **no**: Fall through to Option B (Manual Selection)

3. **Error handling**:
   - If LLM call fails (network error, timeout, API error): Automatically fall back to Option B
   - Show user: "⚠️ AI categorization failed. Falling back to manual selection."

**Option B: Manual Category Selection**

1. Present the 8 available categories:
   - `ai-agents` - AI Agents & Agentic Systems
   - `ai-philosophy` - AI Philosophy & Future of Work
   - `gtm-strategy` - Business & GTM Strategy
   - `industry-research` - Industry Research & Insights
   - `personal-journey` - Personal Journey & Entrepreneurship
   - `practical-applications` - Practical Applications & Use Cases
   - `technical-analysis` - Technical Deep Dives & Analysis
   - `tools-platforms` - GenAI Tools & Platforms

2. Ask user to select one (1-8)

3. Wait for user confirmation before proceeding

### Step 3: Run Article Publishing Script

**IMPORTANT**: This project uses a virtual environment. You must check for it and use it.

1. **Check if virtual environment exists**:
   ```bash
   ls -la venv/bin/python3
   ```

2. **Determine which Python to use**:
   - If venv exists: Use `venv/bin/python3`
   - If venv doesn't exist: Use `python3` (but warn user)

3. **Check if dependencies are installed** (only if using venv):
   ```bash
   venv/bin/python3 -c "import bs4; print('✅ Dependencies OK')" 2>&1
   ```

4. **If dependencies missing**, install them:
   ```bash
   venv/bin/pip install beautifulsoup4 lxml
   ```

5. **Run the publishing script**:
   ```bash
   venv/bin/python3 blog/add_article.py --category [selected-category]
   ```
   (or `python3` if no venv)

6. **Monitor the output carefully for**:
   - Success messages
   - Generated article slug
   - Image download status
   - Any error messages

7. **If errors occur**, diagnose and attempt to fix, or guide user

### Step 4: Copy Images to Proper Locations

**IMPORTANT**: Images are now placed in `/blog/new-articles/` alongside the article HTML. The script must copy them to their final locations.

1. **Identify the article slug** from the generated article filename

2. **Copy hero/cover image**:
   - Source: `/blog/new-articles/{slug}-cover.jpg`
   - Destination: `/images/article-images/{slug}.jpg`
   ```bash
   cp blog/new-articles/{slug}-cover.jpg images/article-images/{slug}.jpg
   ```
   - If cover image doesn't exist, warn user but continue
   - Show: "✅ Copied hero image: {slug}.jpg"

3. **Copy inline images**:
   - Find all files matching `/blog/new-articles/{slug}-img-*.jpg`
   - Copy each to `/images/article-images/inline/{slug}-img-X.jpg`
   ```bash
   mkdir -p images/article-images/inline
   cp blog/new-articles/{slug}-img-*.jpg images/article-images/inline/
   ```
   - Count how many were copied
   - Show: "✅ Copied {N} inline images"

4. **Update article HTML to reference local images**:
   - Read the published article at `/blog/{category}/{slug}.html`
   - Replace any LinkedIn CDN URLs with local paths:
     ```python
     import re
     # Replace LinkedIn CDN URLs in src attributes
     linkedin_pattern = r'src="https://media\.licdn\.com/dms/image/[^"]*"'
     matches = list(re.finditer(linkedin_pattern, content))
     for i, match in enumerate(matches, 1):
         old_src = match.group(0)
         new_src = f'src="../../images/article-images/inline/{slug}-img-{i}.jpg"'
         content = content.replace(old_src, new_src, 1)
     ```
   - Save the updated HTML
   - Show: "✅ Updated article HTML with local image paths"

### Step 5: Validate Output

1. Verify the article was created in `/blog/[category]/[slug].html`
2. Read the first 50 lines of the new article to verify it looks correct
3. Check that hero image exists at `/images/article-images/[slug].jpg`
4. Check that inline images exist in `/images/article-images/inline/[slug]-img-*.jpg`
5. Verify no LinkedIn CDN URLs remain:
   ```bash
   grep -c "media.licdn.com/dms/image" blog/[category]/[slug].html
   ```
   Expected: 0
6. Validate `blog/converted-articles.json` is valid JSON:
   ```bash
   python3 -c "import json; json.load(open('blog/converted-articles.json'))"
   ```
7. Verify the category index was updated: `blog/[category]/index.html`

### Step 6: Validate and Fix Article Counts in blog.html

**CRITICAL**: The `add_article.py` script updates `blog.html` but sometimes the article counts don't update correctly. You MUST validate and fix these:

1. **Get the correct total count** from `converted-articles.json`:
   ```bash
   python3 -c "import json; print(len(json.load(open('blog/converted-articles.json'))))"
   ```

2. **Check the total count in blog.html**:
   ```bash
   grep -o "Explore all [0-9]* articles" blog.html
   ```

3. **If the count is wrong**, fix it:
   - Expected: "Explore all [X] articles" where X is the total from step 1
   - Use Edit tool to update the count

4. **Get the category count** from the category index:
   - Look at `blog/[category]/index.html`
   - Count how many articles are listed, or extract from the page title/header

5. **Check the category count in blog.html**:
   ```bash
   grep -A2 "[Category Name]" blog.html | grep "articles"
   ```

6. **If the category count is wrong**, fix it:
   - Find the category card section in blog.html
   - Update the count to match the actual number in that category
   - Use Edit tool to update

7. **Verify both counts are now correct**:
   - Show user: "✅ Total articles: [X] (verified)"
   - Show user: "✅ [Category] articles: [Y] (verified)"

### Step 7: Update Sitemap

**IMPORTANT**: Every new article must be added to sitemap.xml for SEO.

1. **Read sitemap.xml**:
   ```bash
   cat sitemap.xml
   ```

2. **Find the correct blog category section**:
   - Look for comment like `<!-- [Category Name] Blog Posts -->`
   - Example: `<!-- AI Agents Blog Posts -->` or `<!-- Practical Applications Blog Posts -->`

3. **Add new entry** in alphabetical order within that category section:
   ```xml
   <url>
     <loc>https://vyceralsolutions.com/blog/[category]/[slug].html</loc>
     <changefreq>monthly</changefreq>
     <priority>0.6</priority>
   </url>
   ```

   **Note**: Do NOT add `<lastmod>` tag for blog articles (consistency with existing entries)

4. **Insert in alphabetical order**:
   - Compare the slug with other article URLs in the same category
   - Insert in the correct alphabetical position
   - Use Edit tool to add the entry

5. **Validate sitemap XML**:
   ```bash
   python3 -c "import xml.etree.ElementTree as ET; ET.parse('sitemap.xml'); print('✅ sitemap.xml is valid XML')"
   ```

6. **Verify the entry was added**:
   ```bash
   grep "[slug].html" sitemap.xml
   ```

7. **Show confirmation**:
   - "✅ Added article to sitemap.xml"
   - "✅ Sitemap XML is valid"

### Step 8: Preview Article Locally

1. **Start local server in background**:
   ```bash
   python3 -m http.server 8000 &
   ```
   Store the bash_id for later cleanup.

2. **Show user the preview URLs**:
   - Article: `http://localhost:8000/blog/[category]/[slug].html`
   - Category index: `http://localhost:8000/blog/[category]/index.html`
   - Blog homepage: `http://localhost:8000/blog.html` (to verify counts)

3. **Ask user to check**:
   - Article title and content display correctly
   - Hero image loads properly
   - Formatting looks good
   - Article appears in category index
   - Article counts are correct on blog homepage

4. **Wait for user confirmation**: "Does the article look good? (yes/no)"

5. **Stop the server** (use KillShell with the bash_id from step 1)

### Step 9: Prepare Commit

1. Run `git status` to show what changed
2. Extract article title from the HTML (look for `<h1>` tag)
3. Generate commit message in this format:
   ```
   Add [Category] article: [Article Title]

   - Published to /blog/[category]/[slug].html
   - Updated category index and blog homepage
   - Added to sitemap.xml for SEO
   - [X] total articles, [Y] in [Category] category
   ```
4. Show user the proposed commit message
5. Ask if they want to commit now or make manual edits first

### Step 10: Commit and Push (if user confirms)

1. Stage all changes: `git add .`
2. Commit with the generated message
3. Ask user if they want to push to main branch
4. If yes, run: `git push origin main`
5. Remind user:
   - GitHub Pages will deploy in 2-3 minutes
   - Check https://vyceralsolutions.com/blog/[category]/[slug].html after deployment

## Important Rules

- ❌ DON'T use system `python3` if `venv/` exists - ALWAYS use `venv/bin/python3`
- ❌ DON'T skip Step 4 (image copying) - images must be moved to proper locations
- ❌ DON'T skip Step 6 (article count validation) - counts are often wrong
- ❌ DON'T skip Step 7 (sitemap update) - critical for SEO
- ❌ DON'T proceed if validation fails (especially JSON corruption or XML validation)
- ❌ DON'T push to main without user confirmation
- ❌ DON'T skip the local preview step
- ❌ DON'T forget to stop the background server (use KillShell)
- ❌ DON'T leave LinkedIn CDN URLs in article HTML
- ✅ DO check for and use virtual environment
- ✅ DO copy images from `/blog/new-articles/` to proper locations (Step 4)
- ✅ DO replace LinkedIn CDN URLs with local paths (Step 4)
- ✅ DO validate no LinkedIn CDN URLs remain (Step 5)
- ✅ DO validate article counts in blog.html (Step 6)
- ✅ DO update sitemap.xml with new article URL (Step 7)
- ✅ DO validate sitemap XML syntax after editing
- ✅ DO validate at each step before proceeding
- ✅ DO provide clear error messages if something fails
- ✅ DO show the user what files changed

## Error Handling

Common issues and solutions:

- **Missing `bs4` (beautifulsoup4)**: Install with `venv/bin/pip install beautifulsoup4 lxml`
- **No virtual environment**: Warn user, try with system `python3`, may need to create venv or use `--break-system-packages`
- **"externally-managed-environment" error**: This means they need to use the venv. Check if `venv/` exists and use `venv/bin/python3`
- **Missing hero image**: Remind user to place `{slug}-cover.jpg` in `/blog/new-articles/`. Article can be published without it, but should be added later
- **Missing inline images**: Check that numbered image files (`{slug}-img-1.jpg`, etc.) match the number of images in the article HTML
- **Invalid JSON**: Show the syntax error, attempt to fix by re-running category index generator
- **Invalid XML in sitemap**: Show the syntax error, verify Edit tool preserved XML structure, validate with `python3 -c "import xml.etree.ElementTree as ET; ET.parse('sitemap.xml')"`
- **Script fails**: Show full error output, check Python version, verify paths
- **Category typo**: Validate category slug matches one of the 8 exactly
- **Wrong article counts in blog.html**: The script doesn't always update these correctly. ALWAYS validate and fix in Step 6
- **Server still running**: If KillShell fails, guide user to manually kill: `lsof -ti:8000 | xargs kill`

## Success Criteria

- ✅ Article HTML created in correct category folder
- ✅ **Hero image copied** from `/blog/new-articles/{slug}-cover.jpg` to `/images/article-images/{slug}.jpg`
- ✅ **Inline images copied** from `/blog/new-articles/{slug}-img-*.jpg` to `/images/article-images/inline/`
- ✅ **LinkedIn CDN URLs replaced** with local image paths in article HTML
- ✅ Hero image exists and loads in browser
- ✅ Inline images exist and load in browser
- ✅ No LinkedIn CDN URLs remain in article (verified with grep)
- ✅ Category index updated with new article
- ✅ `converted-articles.json` is valid JSON
- ✅ **Article counts in blog.html are correct** (total + category)
- ✅ **sitemap.xml updated with new article URL** (critical for SEO)
- ✅ sitemap.xml is valid XML (no syntax errors)
- ✅ Article displays correctly in browser
- ✅ Committed to git (or user opted to commit manually)

Begin by checking for HTML files in `/blog/new-articles/`.
