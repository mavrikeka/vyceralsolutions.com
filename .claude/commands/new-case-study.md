# New Case Study

You are creating a new case study for the Vyceral Solutions website. This scaffolds the case study from template and updates all necessary files.

## Context

- Case studies are critical for lead generation (consulting business)
- All 9 existing case studies follow identical template structure
- Must update: case study file + case-studies.html index + sitemap.xml
- Two categories: GTM Automation vs Consulting Transformation

## Your Task

Create a new case study with proper scaffolding and multi-file updates.

### Step 1: Gather Information

Ask the user for the following information (one at a time):

1. **Client Name** (or type description if confidential)
   - Example: "Mann Partners" or "Leadership Development Firm"

2. **Case Study Type** (choose one):
   - GTM Automation
   - Consulting Transformation

3. **Industry/Category Badge**
   - Examples: "B2B SaaS", "Industrial IoT", "Executive Recruiting", "Digital Experience"
   - This appears as colored badge at top

4. **One-line Description** (tagline)
   - Example: "CES-Targeted Manufacturing Campaign" or "Executive Search Automation"

5. **Technologies Used** (comma-separated)
   - Examples: "Clay, MindStudio, Instantly" or "AnyQuest.ai, Custom Development"

6. **Primary Industry**
   - Example: "Manufacturing", "Professional Services", "Healthcare"

Store all responses for later use.

### Step 2: Generate Slug

1. Convert client name to slug (lowercase, hyphens)
   - "Mann Partners" → "mann-partners"
   - "Healthcare Tech Company" → "healthcare-tech-company"

2. Show user the slug
3. Check if file already exists: `case-studies/{slug}.html`
4. If exists, append "-2" or ask user for alternative
5. Confirm slug with user

### Step 3: Copy Template

1. Use `healthcare-tech.html` as the template:
```bash
cp case-studies/healthcare-tech.html case-studies/{slug}.html
```

2. Confirm file was created

### Step 4: Update Case Study File

Read the new file and update these sections (use Edit tool):

1. **`<title>` tag**:
   ```html
   <title>[Client Name] Case Study | [One-line Description] | Vyceral Solutions</title>
   ```

2. **Meta description**:
   ```html
   <meta name="description" content="[Client Name] case study: [Brief summary of results]. Learn how [technologies] delivered [key outcome].">
   ```

3. **Open Graph tags** (og:title, og:description, twitter:title, twitter:description):
   - Update to match title and meta description

4. **Article Schema** (JSON-LD in `<head>`):
   ```json
   {
     "headline": "[Client Name]: [One-line Description]",
     "description": "[Meta description]",
     "datePublished": "[Today's date in YYYY-MM-DD]",
     "dateModified": "[Today's date in YYYY-MM-DD]"
   }
   ```

5. **Breadcrumb - Current page name**:
   ```html
   <span class="current">[Client Name]</span>
   ```

6. **Badge**:
   ```html
   <span class="badge badge-primary">[Category Badge]</span>
   ```

7. **Title and Tagline**:
   ```html
   <h1>[Client Name or Description]</h1>
   <p class="tagline">[One-line Description]</p>
   ```

8. **Case Study Meta** (Client, Industry, Technologies):
   ```html
   <div class="meta-item">
     <span>Client</span>
     <span>[Client Name]</span>
   </div>
   <div class="meta-item">
     <span>Industry</span>
     <span>[Industry]</span>
   </div>
   <div class="meta-item">
     <span>Technologies</span>
     <span>[Technologies]</span>
   </div>
   ```

9. **Add TODO Comments** for sections user must complete:
   ```html
   <!-- TODO: Update these 3 result metrics -->
   <div class="results-grid">
     <div class="result-card">
       <h4>XX%</h4>
       <p>Metric 1 Description</p>
     </div>
     <!-- ... -->
   </div>

   <!-- TODO: Fill in Challenge section -->
   <div class="challenge-box">
     <h3>The Problem</h3>
     <h4>[Challenge Title]</h4>
     <ul>
       <li>[Pain point 1]</li>
       <li>[Pain point 2]</li>
       <li>[Pain point 3]</li>
     </ul>
     <p style="margin-top: 1rem;"><em>The Opportunity: [Strategic insight]</em></p>
   </div>

   <!-- TODO: Fill in Solution section -->
   <div class="solution-box">
     <h3>Our Solution</h3>
     <h4>[Solution Title]</h4>
     <ul>
       <li>[Outcome 1]</li>
       <li>[Outcome 2]</li>
       <li>[Outcome 3]</li>
     </ul>
     <p style="margin-top: 1rem;"><em>The Learning: [Key takeaway]</em></p>
   </div>

   <!-- TODO: Fill in 4 Impact & Results cards -->
   ```

### Step 5: Update Case Studies Index Page

1. Read `case-studies.html`
2. Determine which section to update:
   - "Consulting Transformation" section (if that type)
   - "GTM Automation" section (if that type)

3. Create new case study card:
```html
<div class="card">
  <span class="badge badge-primary">[Category Badge]</span>
  <h3>[Client Name]</h3>
  <p class="tagline">[One-line Description]</p>

  <div class="stats" style="margin: 1rem 0;">
    <div style="display: flex; gap: 2rem; flex-wrap: wrap;">
      <div><strong>XX%</strong> [Metric 1]</div>
      <div><strong>Xx</strong> [Metric 2]</div>
      <div><strong>X weeks</strong> [Metric 3]</div>
    </div>
  </div>

  <p><strong>Challenge:</strong> [Brief challenge description - 1-2 sentences]</p>
  <p><strong>Solution:</strong> [Brief solution description - 1-2 sentences]</p>

  <a href="case-studies/{slug}.html" class="btn btn-primary">Read Full Case Study →</a>
</div>
```

4. Add this card to the appropriate section in case-studies.html
5. Add TODO comment reminding user to fill in the metrics and descriptions

### Step 6: Update Sitemap

1. Read `sitemap.xml`
2. Find the `<!-- Case Studies -->` section
3. Add new entry:
```xml
<url>
  <loc>https://vyceralsolutions.com/case-studies/{slug}.html</loc>
  <lastmod>[Today's date: YYYY-MM-DD]</lastmod>
  <changefreq>monthly</changefreq>
  <priority>0.8</priority>
</url>
```

4. Insert in alphabetical order within case studies section

### Step 7: Summary and Next Steps

Show the user a checklist:

```
✅ Case Study File Created
   - Location: case-studies/{slug}.html
   - Template copied and basic info filled in
   - TODO comments added for sections to complete

✅ Case Studies Index Updated
   - Added card to [GTM Automation / Consulting Transformation] section
   - TODO: Fill in metrics and descriptions in the card

✅ Sitemap Updated
   - Added URL for new case study
   - Sitemap is valid XML

📝 Next Steps - Complete These Sections:

1. Open: case-studies/{slug}.html
2. Search for "TODO" comments (8 sections to complete):

   Required sections:
   ✏️ Results at a Glance (3 metrics)
   ✏️ Challenge section (problem description + pain points)
   ✏️ Solution section (approach + outcomes)
   ✏️ Impact & Results (4 detailed result cards)

   Optional sections:
   ✏️ Technology Stack details (if needed)
   ✏️ Implementation timeline (if relevant)

3. Update case-studies.html card:
   ✏️ Add actual metrics to the stats section
   ✏️ Fill in challenge and solution descriptions

4. Add hero image (optional):
   ✏️ Save image to: images/case-studies/{slug}.jpg
   ✏️ Add to case study HTML in appropriate section

5. Preview locally:
   python3 -m http.server 8000
   Visit: http://localhost:8000/case-studies/{slug}.html

6. When ready, commit:
   git add case-studies/{slug}.html case-studies.html sitemap.xml
   git commit -m "Add [Client Name] case study: [One-line Description]"
   git push origin main
```

### Step 8: Open Files for Editing

Ask user if they want to open the files now:

1. `code case-studies/{slug}.html` (if VS Code available)
2. Or show full path for manual opening

### Step 9: Validation

Validate the files before finishing:

```bash
# Check HTML syntax
python3 << 'EOF'
from html.parser import HTMLParser
try:
    with open('case-studies/{slug}.html') as f:
        HTMLParser().feed(f.read())
    print("✅ HTML syntax valid")
except Exception as e:
    print(f"⚠️ HTML syntax issue: {e}")
EOF

# Validate sitemap XML
python3 -c "import xml.etree.ElementTree as ET; ET.parse('sitemap.xml'); print('✅ sitemap.xml is valid XML')"

# Check case-studies.html still loads
python3 << 'EOF'
from html.parser import HTMLParser
try:
    with open('case-studies.html') as f:
        HTMLParser().feed(f.read())
    print("✅ case-studies.html syntax valid")
except Exception as e:
    print(f"⚠️ case-studies.html syntax issue: {e}")
EOF
```

### Step 10: Show Preview Command

```bash
# To preview the case study:
python3 -m http.server 8000

# Then visit:
# http://localhost:8000/case-studies/{slug}.html
# http://localhost:8000/case-studies.html (check index page)
```

## Important Rules

- ✅ DO preserve exact HTML structure from template
- ✅ DO add TODO comments for user to complete
- ✅ DO update all 3 files (case study + index + sitemap)
- ✅ DO validate XML and HTML syntax
- ❌ DON'T remove any template sections (user might need them)
- ❌ DON'T auto-commit without user review
- ❌ DON'T fill in fake metrics or results (use placeholders)

## Error Handling

- If template copy fails: Check file permissions and path
- If sitemap XML invalid: Show error, attempt to fix
- If Edit tool fails: Show user the content to paste manually

## Success Criteria

- ✅ New case study file created with basic info populated
- ✅ TODO comments guide user on what to complete
- ✅ Case studies index page updated with new card
- ✅ Sitemap includes new URL
- ✅ All files validated (HTML + XML syntax)
- ✅ User knows next steps to complete the case study

Begin by asking the user for the client name.
