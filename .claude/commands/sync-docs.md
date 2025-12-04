# Sync Documentation

> **When to use this command:**
> - After adding new dependencies (npm packages, Python libraries)
> - After creating new files/directories in key locations (scripts, configs, pages)
> - After adding/changing environment variables
> - After modifying database schema
> - After adding new slash commands or scripts
> - Before committing major changes (run as final documentation check)
> - **Pro tip:** Run this after completing feature work to ensure docs stay current

**What this command does:**
Automatically detects code changes and updates only the affected sections of CLAUDE.md. Shows you a diff before applying changes, so you stay in control.

---

## Your Task

Keep CLAUDE.md synchronized with recent code changes by detecting modifications and updating relevant documentation sections.

### Step 1: Detect Code Changes

1. **Check git status** to see what files changed:
   ```bash
   git status --short
   git diff --name-only HEAD
   git diff --cached --name-only
   ```

2. **Get recent commits** (last 5) to catch already-committed changes:
   ```bash
   git log --oneline --name-only -5
   ```

3. **Categorize changes** into these buckets:

   **Bucket A: Dependencies**
   - `package.json`, `package-lock.json`, `requirements.txt`, `Pipfile`, `poetry.lock`, `Gemfile`, `go.mod`
   - Affects: **Tech Stack Summary**, **Key Commands** (install commands)

   **Bucket B: Database Schema**
   - `migrations/`, `schema.sql`, `*.prisma`, `models.py`, `database/`
   - Affects: **Database** section

   **Bucket C: Environment Variables**
   - `.env.example`, config files that reference `process.env.*` or `os.getenv()`
   - Use grep to find new environment variables:
     ```bash
     git diff HEAD | grep -E '(process\.env\.|os\.getenv|getenv\(|ENV\[)' | head -20
     ```
   - Affects: **Environment Variables** section

   **Bucket D: Project Structure**
   - New directories created
   - New files in key locations (blog/, case-studies/, .claude/commands/, css/, js/, images/)
   - Check with:
     ```bash
     git diff HEAD --name-status | grep "^A" | head -20
     ```
   - Affects: **Project Structure** section, **Key File Locations** table

   **Bucket E: Scripts & Commands**
   - New Python scripts (*.py)
   - New slash commands (.claude/commands/*.md)
   - Changes to existing scripts (check if script purpose changed)
   - Affects: **Key Commands** section

   **Bucket F: Configuration Files**
   - `.gitignore`, `robots.txt`, `sitemap.xml`, `CNAME`
   - ESLint, Prettier, TypeScript configs
   - Affects: **Code Style & Conventions**, **Deployment**

4. **Show summary** to user:
   ```
   📊 Detected Changes:

   Dependencies: [X files]
   - package.json (added 2 packages)

   Project Structure: [Y files]
   - New directory: blog/ai-philosophy/
   - New file: case-studies/new-case.html

   Scripts: [Z files]
   - Modified: blog/add_article.py
   - New command: .claude/commands/new-command.md

   Environment Variables: [N new vars]
   - ANYQUEST_API_KEY

   Configuration: [M files]
   - .gitignore updated
   ```

### Step 2: Read Current CLAUDE.md

1. **Read entire CLAUDE.md file**

2. **Identify section boundaries** (look for `## Section Name` headers)

3. **Extract affected sections** based on buckets from Step 1:
   - If Bucket A has changes → extract "Tech Stack Summary" and "Key Commands"
   - If Bucket B has changes → extract "Database"
   - If Bucket C has changes → extract "Environment Variables"
   - If Bucket D has changes → extract "Project Structure" and "Key File Locations"
   - If Bucket E has changes → extract "Key Commands"
   - If Bucket F has changes → extract "Code Style & Conventions"

### Step 3: Generate Updated Content

For each affected section:

**Tech Stack Summary (if dependencies changed):**
1. Read package.json or requirements.txt
2. List current dependencies with versions
3. Update the table format:
   ```markdown
   | Component | Technology | Version | Purpose |
   |-----------|------------|---------|---------|
   | **Frontend** | HTML5 | - | Semantic markup, SEO-optimized |
   | **Styling** | CSS3 | - | Custom design system with CSS variables |
   ```

**Key Commands (if scripts changed):**
1. List all .py files in blog/ and root
2. List all slash commands in .claude/commands/
3. Check if any script added new CLI arguments
4. Update the commands section:
   ```markdown
   ### Blog Management

   ```bash
   # Add new blog article from LinkedIn HTML
   python3 blog/add_article.py --category practical-applications
   ```
   ```

**Project Structure (if new files/dirs):**
1. Generate updated tree structure for changed areas
2. Update file counts if directories have new files
3. Update the structure section:
   ```markdown
   /
   ├── blog/
   │   ├── [8 category folders]/
   │   │   ├── index.html
   │   │   └── *.html
   ```

**Environment Variables (if new vars detected):**
1. List all variables from .env.example
2. Grep codebase for where each is used
3. Update the table:
   ```markdown
   | Item | File | Location |
   |------|------|----------|
   | ANYQUEST_API_KEY | .env | Used in blog/anyquest_client.py |
   ```

**Database (if schema changed):**
1. Read schema files
2. List tables/collections and key fields
3. Update database section (currently says "N/A" for this project)

### Step 4: Show Diff of Proposed Changes

For each section that will be updated:

1. **Show before/after comparison**:
   ```
   📝 Proposed Changes to CLAUDE.md:

   ═══════════════════════════════════════════════════════
   Section: Tech Stack Summary
   ═══════════════════════════════════════════════════════

   --- Before
   +++ After

   - | **Blog Engine** | Python 3 | 3.x | Article conversion, metadata management |
   + | **Blog Engine** | Python 3 | 3.13 | Article conversion, metadata management |
   + | **LLM Integration** | AnyQuest API | - | AI-powered content generation |

   ═══════════════════════════════════════════════════════
   Section: Key Commands
   ═══════════════════════════════════════════════════════

   --- Before
   +++ After

   + # Generate case study with AI
   + python3 blog/anyquest_client.py generate-case-study
   ```

2. **Ask for confirmation**:
   ```
   Update these sections in CLAUDE.md? (yes/no/edit)
   - yes: Apply all changes
   - no: Skip documentation update
   - edit: Apply changes one section at a time (ask for each)
   ```

### Step 5: Apply Updates

1. **If user confirms "yes"**:
   - Use Edit tool to update each affected section
   - Preserve existing formatting and structure
   - Keep the same markdown style

2. **If user confirms "edit"**:
   - Go through each section one by one
   - Ask: "Update [Section Name]? (yes/no)"
   - Apply only confirmed sections

3. **If user says "no"**:
   - Show message: "Skipped documentation update. Run `/sync-docs` again later to sync."
   - Exit without changes

### Step 6: Validate & Summary

1. **Validate CLAUDE.md** is still valid markdown:
   ```bash
   wc -l CLAUDE.md
   head -5 CLAUDE.md
   tail -5 CLAUDE.md
   ```

2. **Show summary**:
   ```
   ✅ Documentation Updated

   Updated sections:
   - Tech Stack Summary (added 1 dependency)
   - Key Commands (added 2 commands)
   - Environment Variables (added 1 variable)

   📝 Next steps:
   - Review CLAUDE.md to ensure accuracy
   - Commit with your other changes:
     git add CLAUDE.md
     git commit -m "Update documentation: [describe changes]"
   ```

3. **Optional: Show git diff** of CLAUDE.md:
   ```bash
   git diff CLAUDE.md
   ```

---

## Special Handling for Common Changes

### New Slash Command Added
If `.claude/commands/*.md` file was added:
1. Extract command name from filename
2. Read the description from the file
3. Add to "Key Commands" or create "Slash Commands" section if needed

### New Python Script Added
If `*.py` file was added:
1. Read first 20 lines looking for docstring
2. Extract purpose from docstring
3. Check if it has `if __name__ == "__main__"` (is it executable?)
4. Add to appropriate commands section

### New Page Added
If new HTML file in root, blog/, or case-studies/:
1. Extract `<title>` tag
2. Extract meta description
3. Update "Project Structure" section
4. Remind user to update sitemap.xml if not already done

### Environment Variable Added
If new `process.env.*` or `os.getenv()` usage found:
1. Check if variable exists in `.env.example`
2. If not, warn user: "⚠️ New env var detected but not in .env.example. Add it there for others."
3. Update Environment Variables section

### Dependency Added
If package.json or requirements.txt changed:
1. Extract package name and version
2. Infer purpose from package name (e.g., "beautifulsoup4" → "HTML parsing")
3. Update Tech Stack Summary

---

## Edge Cases & Smart Skipping

**Skip if:**
- No git changes detected (working tree clean)
- Only changes are to documentation files (*.md)
- Only changes are to images or static assets
- Changes are only whitespace/formatting

**Show warning if:**
- CLAUDE.md was manually edited (check git diff CLAUDE.md)
  - Ask: "CLAUDE.md has uncommitted changes. Merge with detected updates? (yes/no)"
- Major refactor detected (>20 files changed)
  - Suggest: "Large refactor detected. Consider manual CLAUDE.md review after auto-update."

**Error handling:**
- If Edit tool fails, show user the content to paste manually
- If git commands fail, suggest: "Run this from git repository root"
- If CLAUDE.md is missing, ask: "CLAUDE.md not found. Create new one? (yes/no)"

---

## Important Rules

- ✅ DO preserve existing CLAUDE.md structure and tone
- ✅ DO only update sections affected by code changes
- ✅ DO show diff before applying changes
- ✅ DO use exact file paths and line numbers when updating "Key File Locations"
- ✅ DO maintain the same markdown formatting (headers, tables, code blocks)
- ❌ DON'T regenerate the entire CLAUDE.md (only update affected sections)
- ❌ DON'T update sections unnecessarily (be conservative)
- ❌ DON'T lose existing content that's still accurate
- ❌ DON'T change the tone or style (keep it technical and concise)
- ❌ DON'T add speculative information (only document what exists in code)

---

## Success Criteria

- ✅ Detected all relevant code changes from git
- ✅ Identified affected CLAUDE.md sections accurately
- ✅ Showed clear diff of proposed changes
- ✅ Applied updates only to affected sections
- ✅ Preserved existing documentation structure
- ✅ CLAUDE.md is valid markdown after update
- ✅ User understands what was changed and why

Begin by checking git status and recent commits.
