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

1. **Search for published article** across all blog categories:
   ```bash
   find blog -name "{slug}.html" -type f ! -path "*/article raw images/*" ! -path "*/new-articles/*" ! -name "index.html"
   ```
2. **If not found**:
   - Show warning: "⚠️  Skipping {slug}: Published article not found"
   - Continue to next article
3. **If found**: Note the full path for processing

### Step 4: Process Each Article

For each article found, use the TodoWrite tool to track progress with tasks:
- "Processing {article-name}: Copying images"
- "Processing {article-name}: Updating HTML"
- "Processing {article-name}: Verifying changes"

**For each article:**

1. **Copy images to target directory**:
   - Create `/images/article-images/inline/` if it doesn't exist:
     ```bash
     mkdir -p images/article-images/inline
     ```
   - Copy all inline images:
     ```bash
     cp "blog/article raw images"/{slug}-img-*.jpg images/article-images/inline/
     ```
   - Verify copy succeeded (check if files exist)
   - Show: "✅ Copied {N} images for {slug}"

2. **Read the published article HTML**
   - Use Read tool to get current content

3. **Count LinkedIn CDN image references**:
   - Search for: `https://media.licdn.com/dms/image`
   - Count occurrences
   - Show: "Found {N} LinkedIn CDN URLs to replace"

4. **Replace LinkedIn CDN URLs with local paths**:

   For each image number (1 through N):

   - **Extract the current LinkedIn URL** by finding the pattern:
     ```
     <figure><img data-media-urn="..." src="https://media.licdn.com/dms/image/v2/.../[anything]"/>
     ```

   - **Create replacement** with local path:
     ```html
     <figure><img data-media-urn="..." src="../../images/article-images/inline/{slug}-img-{N}.jpg" alt="Article image"/>
     ```

   - **Use Edit tool** to replace:
     - old_string: Full `<figure>...</figure>` block with LinkedIn CDN URL
     - new_string: Same block but with local image path

   - **Important**: Preserve the `data-media-urn` attribute for reference
   - **Important**: Handle images wrapped in `<a>` tags (for sponsored content)

5. **Handle special cases**:
   - If image is wrapped in link (`<figure><a href="..."><img src="..."/></a></figure>`):
     - Preserve the `<a>` tag and its href
     - Only replace the img src
   - If LinkedIn URL has different patterns (e.g., different domain or path structure):
     - Still replace with local path
     - Show warning if pattern doesn't match expected format

6. **Verify replacements**:
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
- Show: "❌ Image not found: {slug}-img-{N}.jpg"
- Skip that specific image replacement
- Continue with remaining images

**If Edit tool fails** (can't find unique old_string):
- Show the problematic HTML snippet
- Show: "⚠️  Manual fix needed for {slug} image {N}"
- Continue with next image

**If category directory not found**:
- Search all blog subdirectories
- Show path where article was found

**If permission errors**:
- Show clear error message
- Suggest checking file permissions

## Important Notes

- **Always use Edit tool** (never Read + Write) to preserve file integrity
- **Preserve HTML structure**: Keep `<figure>`, `<figcaption>`, `data-media-urn` attributes
- **Use relative paths**: `../../images/article-images/inline/{slug}-img-{N}.jpg` (from blog/category/ to images/)
- **Don't modify**: Hero images (those are handled separately)
- **Don't modify**: Article content, only image src attributes
- **Batch operations**: Process multiple edits sequentially, not in parallel

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
