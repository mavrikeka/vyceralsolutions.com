# Pre-Deploy Check

You are performing comprehensive pre-deployment validation before code is pushed to production (main branch). This is a safety net to catch issues before they go live.

## Context

- This is a static website hosted on GitHub Pages
- Pushing to `main` branch auto-deploys to https://vyceralsolutions.com
- No CI/CD, so validation must happen locally
- SEO is critical (canonical URLs, sitemaps, meta tags)
- Site has 121 HTML files: 8 main pages + 95 blog articles + 9 case studies + 8 category indexes

## Your Task

Run a comprehensive pre-deployment validation checklist. Use TodoWrite to track progress through all checks.

### Check 1: Git Status

```bash
git status
git branch
```

- Verify you're on the correct branch
- Show user what files have changed
- Count files changed (should be reasonable, not 100+)

### Check 2: JSON Validation

Validate all JSON files are syntactically correct:

```bash
# Validate blog article registry
python3 -c "import json; data=json.load(open('blog/converted-articles.json')); print(f'✅ Valid JSON: {len(data)} articles')"

# Validate article metadata
python3 -c "import json; json.load(open('blog/articles-metadata.json')); print('✅ articles-metadata.json is valid')"
```

- If validation fails, show the error and STOP (critical issue)
- If success, show article count

### Check 3: Critical Files Exist

Verify critical files are present and non-empty:

```bash
# Check CNAME
test -f CNAME && echo "✅ CNAME exists: $(cat CNAME)" || echo "❌ CNAME missing!"

# Check robots.txt
test -f robots.txt && echo "✅ robots.txt exists" || echo "❌ robots.txt missing!"

# Check sitemap.xml
test -f sitemap.xml && echo "✅ sitemap.xml exists" || echo "❌ sitemap.xml missing!"

# Check main stylesheet
test -f css/style.css && echo "✅ style.css exists ($(wc -l < css/style.css) lines)" || echo "❌ style.css missing!"

# Check main JavaScript
test -f js/main.js && echo "✅ main.js exists" || echo "❌ main.js missing!"
```

- Flag any missing files as CRITICAL

### Check 4: HTML Validation (Sample)

Check a sample of HTML files for basic syntax:

1. Pick 3 changed files (from git status) OR 3 random files if nothing changed
2. For each file, check:
   - File exists and is readable
   - Contains `<!DOCTYPE html>`
   - Contains `</html>` closing tag
   - Has proper `<head>` and `</head>`
   - Has `<title>` tag
   - Has closing `</body>` tag

Show results in a table format.

### Check 5: Image Validation

Check if all referenced images exist:

1. Find all changed HTML files: `git diff --name-only HEAD`
2. For each changed HTML file:
   - Extract image references: `grep -o 'src="[^"]*"'`
   - Check if each image file exists
   - Flag missing images as ⚠️ WARNING

3. Check for large images in `/images/article-images/`:
```bash
find images/article-images -name "*.jpg" -o -name "*.png" | while read img; do
  size=$(du -k "$img" | cut -f1)
  if [ $size -gt 500 ]; then
    echo "⚠️ Large image: $img (${size}KB)"
  fi
done
```

### Check 6: Internal Links Check (Sample)

Check internal links in changed files:

1. Get list of changed HTML files
2. For each file, extract `href="..."` attributes
3. For relative links (not starting with http):
   - Resolve the path relative to the file
   - Check if target file exists
   - Flag broken links as ❌ ERROR

Show summary: X links checked, Y broken

### Check 7: SEO Validation (Sample)

Check SEO elements in main pages:

```bash
# For each main HTML file (index.html, about.html, etc.)
# Check for these elements:
```

1. Canonical URL: `<link rel="canonical"`
2. Meta description: `<meta name="description"`
3. Open Graph title: `<meta property="og:title"`
4. Title tag length (should be 50-60 chars)

Show results in table: File | Canonical | Meta Desc | OG Tags | Title Length

### Check 8: Sitemap Validation

Validate sitemap.xml:

```bash
# Check if it's valid XML
python3 -c "import xml.etree.ElementTree as ET; ET.parse('sitemap.xml'); print('✅ sitemap.xml is valid XML')"

# Count URLs
grep -c "<loc>" sitemap.xml
```

### Check 9: Navigation Consistency (Sample)

Check that navigation is consistent across pages:

1. Extract `<nav class="nav">` section from index.html
2. Extract same section from 2-3 other main pages
3. Compare if they're identical (excluding active states)
4. Flag inconsistencies as ⚠️ WARNING

### Check 10: Blog Article Integrity

If any blog articles were added/modified:

```bash
# Verify all articles in JSON actually exist as files
python3 << 'EOF'
import json
missing = []
with open('blog/converted-articles.json') as f:
    articles = json.load(f)
    for article in articles:
        path = article.get('path', '')
        import os
        if path and not os.path.exists(path):
            missing.append(path)
if missing:
    print(f"❌ Missing articles: {len(missing)}")
    for m in missing[:5]:
        print(f"  - {m}")
else:
    print(f"✅ All {len(articles)} articles exist")
EOF
```

## Final Report

Present a summary checklist:

```
Pre-Deployment Validation Report
=================================

Critical Checks:
 [✅/❌] JSON files valid
 [✅/❌] CNAME file correct
 [✅/❌] sitemap.xml valid
 [✅/❌] CSS and JS files exist

Important Checks:
 [✅/⚠️] HTML syntax (sampled)
 [✅/⚠️] Images exist and reasonable size
 [✅/⚠️] Internal links valid (sampled)
 [✅/⚠️] SEO elements present

Optional Checks:
 [✅/⚠️] Navigation consistency
 [✅/⚠️] Blog article integrity

Files Changed: X files
Branch: <current-branch>

Recommendation: [SAFE TO DEPLOY / FIX ISSUES FIRST / CRITICAL ISSUES - DO NOT DEPLOY]
```

## Decision Logic

- **CRITICAL ISSUES** (block deployment):
  - Invalid JSON (breaks blog)
  - Missing CNAME (site unreachable)
  - Missing critical files (style.css, main.js)
  - Broken links to main pages

- **WARNINGS** (proceed with caution):
  - Large images (>500KB)
  - Missing images in blog articles
  - Missing SEO tags
  - Navigation inconsistencies

- **SAFE TO DEPLOY**:
  - All critical checks pass
  - No warnings or only minor warnings

## User Interaction

1. Ask user if they want to proceed with deployment if warnings found
2. If critical issues, DO NOT offer to push - user must fix first
3. If safe, ask: "Ready to push to main branch?"
4. If user confirms, run: `git push origin main`

## Important Rules

- ❌ DON'T skip checks even if they seem redundant
- ❌ DON'T push if critical issues found
- ✅ DO use TodoWrite to track progress through checks
- ✅ DO provide clear recommendations
- ✅ DO explain what each error means

Begin by checking git status and current branch.
