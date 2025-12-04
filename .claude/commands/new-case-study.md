# New Case Study

You are creating a new case study for the Vyceral Solutions website. This scaffolds the case study from template and updates all necessary files.

## Context

- Case studies are critical for lead generation (consulting business)
- All 9 existing case studies follow identical template structure
- Must update: case study file + case-studies.html index + sitemap.xml
- Two categories: GTM Automation vs Consulting Transformation

## Your Task

Create a new case study with proper scaffolding and multi-file updates.

### Step 1: Choose Input Method

Ask user: "How would you like to create this case study?"

Display options:
```
1. 🤖 Generate from Description (AI-Powered) - Recommended
2. ✍️  Manual Entry (Fill in details yourself)
```

---

**Option 1: AI-Powered Generation** (If user selects 1)

1. **Ask for case study description**:
   ```
   Please provide a 2-4 paragraph description of the case study including:
   - Client/company context
   - The problem/challenge they faced
   - Your solution/approach
   - Key results/outcomes

   Paste your description below:
   ```

2. **Read multi-line description** from user (they can paste multiple paragraphs)

3. **Generate structured data with LLM**:
   - Show message: "Generating case study content with AI... (this takes 30-60 seconds)"
   - Save description to temporary file or pass via stdin:
     ```bash
     echo "[user-description]" | venv/bin/python3 blog/anyquest_client.py generate-case-study
     ```
   - Wait for response (returns JSON with all case study data)
   - Parse JSON output

4. **Show generated data to user**:
   ```
   ✨ Generated Case Study Data:

   Solution Type: [solution_type]
   Client: [client_name]
   Industry: [industry]
   Badge: [badge]
   Tagline: [tagline]
   Technologies: [technologies]

   Challenge: [challenge]

   Solution: [solution]

   Metrics (3):
   - [metric1_value]: [metric1_description]
   - [metric2_value]: [metric2_description]
   - [metric3_value]: [metric3_description]

   Results (4):
   - [result1_title]: [result1_description]
   - [result2_title]: [result2_description]
   - [result3_title]: [result3_description]
   - [result4_title]: [result4_description]

   CTA:
   - Headline: [cta_headline]
   - Description: [cta_description]
   ```

5. **Ask for confirmation**:
   ```
   Accept this generated content? (yes/no/regenerate)
   - yes: Proceed to Step 2 (Generate Slug)
   - no: Fall back to Option 2 (Manual Entry)
   - regenerate: Call LLM again with same description
   ```

6. **Error handling**:
   - If LLM call fails: Automatically fall back to Option 2
   - Show user: "⚠️ AI generation failed. Falling back to manual entry."
   - If JSON parsing fails: Show error and offer to regenerate or enter manually

**Store all data** (either from LLM or user input) for later use.

---

**Option 2: Manual Entry** (If user selects 2 OR fallback from Option 1)

Ask the user for the following information (one at a time):

1. **Case Study Type** (choose one - REQUIRED for CTA):
   - GTM Automation (B2B software sales teams)
   - Consulting Transformation (strategy consulting firms)

   **Important:** Store this for CTA generation in Step 4

2. **Client Name** (or type description if confidential)
   - Example: "Mann Partners" or "Leadership Development Firm"

3. **Industry/Category Badge**
   - Examples: "B2B SaaS", "Industrial IoT", "Executive Recruiting", "Digital Experience"
   - This appears as colored badge at top

4. **One-line Description** (tagline)
   - Example: "CES-Targeted Manufacturing Campaign" or "Executive Search Automation"

5. **Technologies Used** (comma-separated)
   - Examples: "Clay, MindStudio, Instantly" or "AnyQuest.ai, Custom Development"

6. **Primary Industry**
   - Example: "Manufacturing", "Professional Services", "Healthcare"

7. **Challenge** (2-3 sentences)

8. **Solution** (2-3 sentences)

9. **Three Metrics**:
   - Metric 1 value and description
   - Metric 2 value and description
   - Metric 3 value and description

10. **Four Results** (for detailed impact section):
    - Result 1: Title and description
    - Result 2: Title and description
    - Result 3: Title and description
    - Result 4: Title and description

11. **CTA Headline** (based on case study type):
    - **If GTM Automation:** Suggest a sales/GTM-focused CTA
      - Examples: "Ready to Transform Your Sales Intelligence?", "Ready to Automate Your Research-to-Outreach Pipeline?", "Ready to Automate Your Sales Qualification?"
    - **If Consulting Transformation:** Suggest a consulting workflow-focused CTA
      - Examples: "Ready to Transform Your Research Workflow?", "Ready to Automate Your Pitch Pack Creation?", "Ready to Automate Your Executive Recruiting Screening?"
    - Ask user to confirm or provide custom CTA

12. **CTA Description** (based on case study type):
    - **If GTM Automation:** "Learn how we can build [type of system] for your GTM/sales team."
    - **If Consulting Transformation:** "Learn how we can build [type of system] for your business/workflow."
    - Customize based on the specific solution

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

10. **CTA Section** (customize based on solution type):

   **If GTM Automation:**
   ```html
   <!-- CTA Section -->
   <section class="section cta-section">
     <div class="container">
       <div class="cta-section">
         <h2>[CTA Headline - GTM focused]</h2>
         <p>[CTA Description - mention GTM/sales team]</p>
         <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
           <a href="../contact.html" class="btn btn-large">Schedule a Consultation</a>
           <a href="../case-studies.html" class="btn btn-outline btn-large" style="background: transparent; color: white; border-color: white;">View More Case Studies</a>
         </div>
       </div>
     </div>
   </section>
   ```

   **If Consulting Transformation:**
   ```html
   <!-- CTA Section -->
   <section class="section cta-section">
     <div class="container">
       <div class="cta-section">
         <h2>[CTA Headline - Consulting workflow focused]</h2>
         <p>[CTA Description - mention business/workflow]</p>
         <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
           <a href="../contact.html" class="btn btn-large">Schedule a Consultation</a>
           <a href="../case-studies.html" class="btn btn-outline btn-large" style="background: transparent; color: white; border-color: white;">View More Case Studies</a>
         </div>
       </div>
     </div>
   </section>
   ```

   **CTA Examples by Type:**
   - **GTM Automation:**
     - "Ready to Transform Your Sales Intelligence?" / "Learn how we can build an intelligent automation system for your GTM team."
     - "Ready to Automate Your Research-to-Outreach Pipeline?" / "Learn how we can build an integrated Clay + Agent.ai + Outreach system for your sales team."
     - "Ready to Automate Your Sales Qualification?" / "Learn how we can build custom assessment tools that demonstrate value and qualify prospects at scale."

   - **Consulting Transformation:**
     - "Ready to Transform Your Research Workflow?" / "Learn how we can build a custom AI agent system for your business."
     - "Ready to Automate Your Pitch Pack Creation?" / "Learn how we can build a multi-agent system to transform your proposal development process."
     - "Ready to Automate Your Executive Recruiting Screening?" / "Learn how we can build a criteria-based evaluation agent for your recruiting workflows."

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
