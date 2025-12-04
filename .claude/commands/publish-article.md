# Publish Article

You are helping publish a new blog article to the Vyceral Solutions website. This is a comprehensive end-to-end workflow.

## Context

- This is a static website with blog articles managed via Python scripts
- Articles are sourced from LinkedIn and placed in `/blog/new-articles/`
- The `add_article.py` script converts them to the site's template format
- Articles are organized into 8 categories with indexes that must be regenerated

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

### Step 4: Validate Output

1. Verify the article was created in `/blog/[category]/[slug].html`
2. Read the first 50 lines of the new article to verify it looks correct
3. Check that hero image exists at `/images/article-images/[slug].jpg`
4. Validate `blog/converted-articles.json` is valid JSON:
   ```bash
   python3 -c "import json; json.load(open('blog/converted-articles.json'))"
   ```
5. Verify the category index was updated: `blog/[category]/index.html`

### Step 5: Validate and Fix Article Counts in blog.html

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

### Step 6: Preview Article Locally

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

### Step 7: Prepare Commit

1. Run `git status` to show what changed
2. Extract article title from the HTML (look for `<h1>` tag)
3. Generate commit message in this format:
   ```
   Add [Category] article: [Article Title]

   - Published to /blog/[category]/[slug].html
   - Updated category index and blog homepage
   - [X] total articles, [Y] in [Category] category
   ```
4. Show user the proposed commit message
5. Ask if they want to commit now or make manual edits first

### Step 8: Commit and Push (if user confirms)

1. Stage all changes: `git add .`
2. Commit with the generated message
3. Ask user if they want to push to main branch
4. If yes, run: `git push origin main`
5. Remind user:
   - GitHub Pages will deploy in 2-3 minutes
   - Check https://vyceralsolutions.com/blog/[category]/[slug].html after deployment

## Important Rules

- ❌ DON'T use system `python3` if `venv/` exists - ALWAYS use `venv/bin/python3`
- ❌ DON'T skip Step 5 (article count validation) - counts are often wrong
- ❌ DON'T proceed if validation fails (especially JSON corruption)
- ❌ DON'T push to main without user confirmation
- ❌ DON'T skip the local preview step
- ❌ DON'T forget to stop the background server (use KillShell)
- ✅ DO check for and use virtual environment
- ✅ DO validate article counts in blog.html (Step 5)
- ✅ DO validate at each step before proceeding
- ✅ DO provide clear error messages if something fails
- ✅ DO show the user what files changed

## Error Handling

Common issues and solutions:

- **Missing `bs4` (beautifulsoup4)**: Install with `venv/bin/pip install beautifulsoup4 lxml`
- **No virtual environment**: Warn user, try with system `python3`, may need to create venv or use `--break-system-packages`
- **"externally-managed-environment" error**: This means they need to use the venv. Check if `venv/` exists and use `venv/bin/python3`
- **Missing hero image**: Article script should download it, but if it fails, ask user to provide image URL or path
- **Invalid JSON**: Show the syntax error, attempt to fix by re-running category index generator
- **Script fails**: Show full error output, check Python version, verify paths
- **Category typo**: Validate category slug matches one of the 8 exactly
- **Wrong article counts in blog.html**: The script doesn't always update these correctly. ALWAYS validate and fix in Step 5
- **Server still running**: If KillShell fails, guide user to manually kill: `lsof -ti:8000 | xargs kill`

## Success Criteria

- ✅ Article HTML created in correct category folder
- ✅ Hero image exists and loads
- ✅ Category index updated with new article
- ✅ `converted-articles.json` is valid JSON
- ✅ **Article counts in blog.html are correct** (total + category)
- ✅ Article displays correctly in browser
- ✅ Committed to git (or user opted to commit manually)

Begin by checking for HTML files in `/blog/new-articles/`.
