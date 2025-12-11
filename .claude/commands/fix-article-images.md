# Fix Article Images

You are helping fix broken LinkedIn CDN images in blog articles by replacing them with local image references. This is a batch processing workflow for multiple articles.

## Context

- LinkedIn CDN image URLs expire (parameter `e=` in URL)
- User downloads articles from LinkedIn with images to `/blog/article raw images/`
- Each article has:
  - `{slug}.html` - raw HTML from LinkedIn
  - `{slug}-img-1.jpg`, `{slug}-img-2.jpg`, etc. - inline images
  - `{slug}-cover.jpg` - hero image (optional, not processed by this command)
- Published articles are in `/blog/{category}/{slug}.html`
- We need to:
  1. Copy inline images to `/images/article-images/inline/`
  2. Update published HTML to reference local images instead of LinkedIn CDN

## Your Task

Execute the complete image fix workflow:

### Step 1: Scan for Articles to Process

1. **List all files** in `/blog/article raw images/` directory
2. **Identify articles** by finding `.html` files (excluding any template files)
3. **For each article HTML file**:
   - Extract the slug (filename without .html extension)
   - Count associated image files: `{slug}-img-*.jpg`
   - Show summary:
     ```
     Found articles to process:
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     1. ai-horseless-carriages (7 images)
     2. genai-and-the-future-of-work (3 images)
     3. another-article (5 images)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     Total: 3 articles, 15 images
     ```
4. **If no articles found**:
   - Show message: "❌ No articles found in /blog/article raw images/"
   - Instruct user: "Download articles from LinkedIn (Save as complete webpage) and place them in this folder"
   - Exit

### Step 2: Confirm Processing

1. **Ask user**: "Process all [N] articles? (yes/no/specific)"
2. **If specific**: Ask "Enter article slug to process: "
3. **If no**: Exit

### Step 3: Find Published Articles

For each article to process:

1. **Search for published article** across all blog categories using fuzzy matching:
   ```bash
   # Try exact match first
   find blog -name "{slug}.html" -type f ! -path "*/article raw images/*" ! -path "*/new-articles/*" ! -name "index.html"

   # If not found, try partial match (handles truncated filenames)
   find blog -name "*{first-30-chars}*" -type f ! -path "*/article raw images/*"
   ```

2. **Handle filename variations**:
   - **Truncation**: `can-it-b` → `can-it-be-built.html`
   - **Apostrophes**: `can-t` → `cant.html` (apostrophe removed or converted)
   - **Special chars**: LinkedIn download names may differ from published names

3. **If not found**:
   - Show warning: "⚠️  Skipping {slug}: Published article not found"
   - Continue to next article

4. **If found**: Note the full path AND the actual published slug for processing

### Step 4: Process Each Article

For each article found, use the TodoWrite tool to track progress with tasks:
- "Processing {article-name}: Copying images"
- "Processing {article-name}: Updating HTML"
- "Processing {article-name}: Verifying changes"

**For each article:**

1. **Copy images to target directory with correct filenames**:
   - Create `/images/article-images/inline/` if it doesn't exist:
     ```bash
     mkdir -p images/article-images/inline
     ```
   - Copy images using the PUBLISHED slug (not raw slug) for filenames:
     ```python
     # If raw slug is "can-it-b" but published is "can-it-be-built":
     src: blog/article raw images/can-it-b-img-1.jpg
     dst: images/article-images/inline/can-it-be-built-img-1.jpg
     ```
   - This ensures image filenames match the published article slug
   - Show: "✅ Copied {N} images for {published-slug}"

2. **Count LinkedIn CDN image references**:
   - Read the published article HTML
   - Search for: `https://media.licdn.com/dms/image`
   - Count occurrences
   - Show: "Found {N} LinkedIn CDN URLs to replace"

3. **Replace LinkedIn CDN URLs with local paths** (ALL variations):

   **IMPORTANT**: Use regex pattern matching on `src` attribute ONLY, not entire figure blocks. This handles ALL HTML variations:
   - Simple figures: `<figure><img src="..."/></figure>`
   - Wrapped in links: `<figure><a href="..."><img src="..."/></a></figure>`
   - With captions: `<figure><img src="..."/><figcaption>Text</figcaption></figure>`
   - Mixed: `<figure><a><img src="..."/></a><figcaption>Text</figcaption></figure>`

   **Working Approach** (Python script):
   ```python
   import re

   # Read file
   with open(file_path, 'r') as f:
       content = f.read()

   # Find ALL LinkedIn CDN URLs in order
   linkedin_pattern = r'src="https://media\.licdn\.com/dms/image/[^"]*"'
   matches = list(re.finditer(linkedin_pattern, content))

   # Replace each sequentially with local path
   for i, match in enumerate(matches, 1):
       old_src = match.group(0)
       new_src = f'src="../../images/article-images/inline/{published_slug}-img-{i}.jpg"'
       content = content.replace(old_src, new_src, 1)  # Replace one at a time

   # Write back
   with open(file_path, 'w') as f:
       f.write(content)
   ```

   **Why this works**:
   - Replaces ONLY the src attribute, preserving all surrounding HTML
   - Works with ANY HTML structure around the image
   - Processes images in document order (top to bottom)
   - Preserves `data-media-urn`, `<a>` tags, `<figcaption>`, etc.

4. **Verify replacements**:
   - Read the updated file
   - Confirm no LinkedIn CDN URLs remain in the article content:
     ```bash
     grep -c "media.licdn.com/dms/image" blog/{category}/{slug}.html
     ```
   - Expected result: 0
   - Show: "✅ Verified: All LinkedIn URLs replaced"

### Step 5: Summary Report

After processing all articles, show comprehensive summary:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IMAGE FIX SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Articles Processed:     {N}
Images Copied:          {N}
HTML Files Updated:     {N}
LinkedIn URLs Removed:  {N}

✅ Successfully Processed:
   1. ai-horseless-carriages (7 images → 7 local)
   2. article-two (3 images → 3 local)

⚠️  Warnings:
   - article-three: Published file not found

❌ Errors:
   - None

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Test locally:
   python3 -m http.server 8000
   Visit: http://localhost:8000/blog/{category}/{slug}.html

2. Verify images load correctly in browser

3. Commit changes:
   git add images/article-images/inline/ blog/
   git commit -m "Fix expired LinkedIn CDN images for {N} articles"
   git push origin main

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Error Handling

**If image file doesn't exist**:
- Show: "❌ Image not found: {raw-slug}-img-{N}.jpg"
- Skip that specific image replacement
- Continue with remaining images

**If published article slug differs from raw slug**:
- Show mapping: "Raw: {raw-slug} → Published: {published-slug}"
- Copy images with published slug as target filename
- This handles truncation and character variations

**If filename variations found**:
- **Truncated names**: Search with first 30 chars as wildcard
- **Apostrophe variations**: Try both `can-t` and `cant`
- **Special characters**: Try with/without special chars
- Show which variation was matched

**If category directory not found**:
- Search all blog subdirectories
- Show path where article was found

**If permission errors**:
- Show clear error message
- Suggest checking file permissions

**Common Filename Variations**:
| Raw Image Slug | Published Article Slug | Reason |
|----------------|------------------------|--------|
| `can-it-b` | `can-it-be-built` | Truncation |
| `can-t` | `cant` | Apostrophe removed |
| `mcp-a` | `mcp-and-agentai` | Truncation |

## Important Notes

- **Use Python script for replacements**: More reliable than Edit tool for multiple replacements with HTML variations
- **ONLY replace src attribute**: Don't try to match entire `<figure>` blocks - this breaks with variations
- **Preserve ALL HTML structure**: `<figure>`, `<a>`, `<figcaption>`, `data-media-urn` - replacement only touches the src URL
- **Use published slug for image filenames**: Not the raw slug from download folder
- **Use relative paths**: `../../images/article-images/inline/{published-slug}-img-{N}.jpg` (from blog/category/ to images/)
- **Don't modify**: Hero images (those are handled separately)
- **Don't modify**: Article content, only image src attributes
- **Replace sequentially**: Process one URL at a time, in document order (top to bottom)
- **Handle filename variations**: Always check for truncation and character changes

## Testing Checklist

After processing, remind user to verify:
- [ ] Images load in browser (check Network tab)
- [ ] No 404 errors for images
- [ ] No LinkedIn CDN URLs remain (search codebase)
- [ ] Images display correctly on mobile
- [ ] Alt text is present on all images
- [ ] File sizes are reasonable (<500KB per image recommended)

## Success Criteria

✅ All inline images copied to `/images/article-images/inline/`
✅ All LinkedIn CDN URLs replaced with local paths
✅ No broken image links (verify in browser)
✅ HTML structure preserved (no malformed tags)
✅ User sees clear summary of changes made
