# Sync Navigation

You are updating the navigation menu consistently across all HTML files in the website. This is a critical operation affecting 121 files.

## Context

- Navigation appears in `<nav class="nav">` section on all pages
- Consists of: logo + 7 menu items + mobile menu toggle
- Must be identical across all pages (except active states)
- Files to update: 8 main pages + 95 blog articles + 9 case studies + 8 category indexes + 1 legacy services page

## Your Task

Update navigation menu across all HTML files with proper safeguards.

### Step 1: Find Current Navigation

1. Extract the current navigation from `index.html`:
```bash
# Find the nav section (from <nav class="nav"> to </nav>)
sed -n '/<nav class="nav">/,/<\/nav>/p' index.html
```

2. Show the user the current navigation structure
3. Parse menu items and display in a numbered list

### Step 2: Get User's Desired Changes

Ask the user what they want to change:

**Options:**
- Add a new menu item
- Remove a menu item
- Reorder menu items
- Change a link URL
- Change link text
- Just sync current navigation (no changes, fix inconsistencies)

If "just sync", use navigation from index.html as source of truth.

If making changes, guide user through modification:
- Show current state
- Ask for new state
- Confirm before proceeding

### Step 3: Generate New Navigation HTML

1. Build the new navigation HTML structure
2. Maintain exact formatting/indentation from original
3. Preserve:
   - Mobile menu toggle button
   - Logo link
   - CSS classes
   - Proper structure

4. Show user the new navigation HTML
5. Ask for confirmation before applying to all files

### Step 4: Find All HTML Files

```bash
# Find all HTML files that likely have navigation
find . -name "*.html" -not -path "./blog/new-articles/*" -not -path "./blog/articles-raw/*" -not -path "./venv/*" | sort
```

Count files found and show to user.

### Step 5: Backup Current State

Create a safety backup:

```bash
# Create backup branch
git checkout -b navigation-update-backup-$(date +%Y%m%d-%H%M%S)
git add -A
git commit -m "Backup before navigation update"

# Return to original branch
git checkout -
```

Inform user that backup branch was created.

### Step 6: Preview Changes (Sample)

Before updating all files, preview changes on 3 sample files:

1. Pick: index.html, about.html, and one blog article
2. For each file:
   - Extract current nav section
   - Show what it will become
   - Highlight differences
3. Ask user to confirm before proceeding to bulk update

### Step 7: Perform Bulk Update

Use TodoWrite to track progress through file updates.

For each HTML file:

1. Create a Python script to do the replacement:

```python
import re
import os

def update_nav_in_file(filepath, new_nav):
    """Replace nav section in HTML file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find and replace nav section
        pattern = r'<nav class="nav">.*?</nav>'
        if not re.search(pattern, content, re.DOTALL):
            return False, "No nav section found"

        updated = re.sub(pattern, new_nav, content, count=1, flags=re.DOTALL)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated)

        return True, "Updated"
    except Exception as e:
        return False, str(e)

# List of all HTML files
files = [...]  # Generated from find command

new_nav = """<nav class="nav">
  <!-- New navigation HTML here -->
</nav>"""

results = {'success': 0, 'failed': 0, 'skipped': 0}
failed_files = []

for filepath in files:
    success, message = update_nav_in_file(filepath, new_nav)
    if success:
        results['success'] += 1
    elif "No nav section found" in message:
        results['skipped'] += 1
    else:
        results['failed'] += 1
        failed_files.append((filepath, message))

print(f"✅ Updated: {results['success']}")
print(f"⏭️ Skipped: {results['skipped']}")
print(f"❌ Failed: {results['failed']}")

if failed_files:
    print("\nFailed files:")
    for filepath, error in failed_files[:10]:
        print(f"  - {filepath}: {error}")
```

2. Run the script
3. Show results summary

### Step 8: Validation

After bulk update, validate:

1. **HTML Syntax Check** (sample 5 files):
```bash
# Check files can still be parsed as HTML
python3 << 'EOF'
from html.parser import HTMLParser
import os

files_to_check = ['index.html', 'about.html', 'blog.html', 'case-studies.html', 'blog/ai-agents/index.html']

for f in files_to_check:
    if os.path.exists(f):
        try:
            with open(f) as file:
                HTMLParser().feed(file.read())
            print(f"✅ {f}")
        except Exception as e:
            print(f"❌ {f}: {e}")
EOF
```

2. **Visual Consistency Check**:
   - Start local server: `python3 -m http.server 8000`
   - List 3-4 URLs for user to check in browser
   - Ask user to verify navigation looks correct

3. **Git Diff Check**:
```bash
# Show summary of changes
git diff --stat

# Show detailed diff of one file (for user review)
git diff index.html | head -50
```

### Step 9: Commit Changes

If validation passes:

1. Show user the git status
2. Generate commit message:
   ```
   Sync navigation across all pages: [describe change]

   - Updated navigation in 121 HTML files
   - [Specific change made, e.g., "Added Blog menu item"]
   - Validated HTML syntax and visual consistency

   Files updated:
   - 8 main pages
   - 95 blog articles
   - 9 case studies
   - 8 category indexes
   - 1 legacy services page
   ```

3. Ask user to confirm commit message
4. Stage and commit:
```bash
git add .
git commit -m "[generated message]"
```

5. Ask user if they want to push to main
6. Remind user to test on live site after push

### Step 10: Cleanup

Delete the backup branch (if user confirms everything works):

```bash
git branch -d navigation-update-backup-YYYYMMDD-HHMMSS
```

## Error Handling

Common issues:

- **File encoding issues**: Try with 'latin-1' if UTF-8 fails
- **Regex doesn't match**: Navigation structure might be different in some files - handle manually
- **Permission errors**: Check file permissions
- **Git conflicts**: Ensure working directory is clean before starting

## Important Rules

- ❌ DON'T proceed without user confirmation at each major step
- ❌ DON'T skip the backup step (safety first!)
- ❌ DON'T update files if preview shows unexpected changes
- ✅ DO create backup branch before making changes
- ✅ DO validate after bulk update
- ✅ DO show clear progress tracking (use TodoWrite)
- ✅ DO provide rollback instructions if something goes wrong

## Rollback Instructions

If something goes wrong:

```bash
# Discard all changes
git checkout .

# Or restore from backup branch
git checkout navigation-update-backup-YYYYMMDD-HHMMSS
git checkout -b navigation-fix
# Make fixes, then retry
```

## Success Criteria

- ✅ All 121 HTML files have identical navigation structure
- ✅ No HTML syntax errors introduced
- ✅ Visual consistency verified in browser
- ✅ Changes committed to git
- ✅ User confirmed navigation works as expected

Begin by extracting current navigation from index.html.
