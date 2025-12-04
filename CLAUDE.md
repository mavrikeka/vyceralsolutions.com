# CLAUDE.md - Vyceral Solutions Website

> **Last Updated**: December 4, 2025

## Project Overview

**Vyceral Solutions LLC** is a GenAI consulting firm specializing in go-to-market automation for B2B software companies and AI-powered transformation for strategy consulting firms.

### What This App Does

This is a **static marketing website** with the following capabilities:

1. **Dual-Market Positioning**
   - **GTM Automation Services**: Clay, Agent.ai, MindStudio implementations for B2B software sales teams
   - **Consulting Transformation**: AnyQuest.ai deployments for strategy consulting firms (internal efficiency + client delivery)

2. **Content Marketing Hub**
   - 95 blog articles across 8 categories (cross-posted from LinkedIn)
   - 9 detailed case studies with quantified results
   - SEO-optimized with structured data and canonical URLs

3. **Lead Generation**
   - Direct contact CTAs (email + LinkedIn)
   - B2B visitor tracking via Reb2b integration
   - No forms (directs to email/LinkedIn for human touch)

### Key User Flows

```
Visitor Discovery Flow:
├─ Google Search → Blog Article → Category Index → Service Page → Contact
├─ LinkedIn Post → Homepage → Case Studies → Service Page → Contact
└─ Direct Visit → Homepage → Two-Path Split → GTM or Consulting → Case Studies → Contact

Content Flow:
├─ LinkedIn Article → Python Script → Blog Category → Site Deployment → Google Index
└─ Client Engagement → Case Study Creation → Manual HTML → Git Commit → Pages Deploy
```

### Architecture Overview

```
Static Site Architecture (No Build Process)
┌─────────────────────────────────────────────────────┐
│                     GitHub Pages                     │
│              (Automatic deployment from main)        │
└─────────────────────────────────────────────────────┘
                          ↑
                    Git Push (main)
                          ↑
┌─────────────────────────────────────────────────────┐
│             Local Development Environment            │
│  ┌────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │   HTML     │  │     CSS      │  │ JavaScript  │ │
│  │  (8 pages) │  │ (style.css)  │  │  (main.js)  │ │
│  └────────────┘  └──────────────┘  └─────────────┘ │
│  ┌────────────────────────────────────────────────┐ │
│  │  Python Scripts (Blog Content Management)     │ │
│  │  - add_article.py (publish new posts)         │ │
│  │  - create_category_indexes.py (rebuild cats)  │ │
│  └────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────┐ │
│  │  Content Directories                           │ │
│  │  /blog/ (95 articles + 8 category indexes)    │ │
│  │  /case-studies/ (9 client success stories)    │ │
│  │  /images/ (logos, hero images, article imgs)  │ │
│  └────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
                          ↓
                  Local Testing (Python)
                python3 -m http.server 8000
```

---

## Tech Stack Summary

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| **Frontend** | HTML5 | - | Semantic markup, SEO-optimized |
| **Styling** | CSS3 | - | Custom design system with CSS variables |
| **Interactivity** | Vanilla JavaScript | ES6+ | Mobile nav, scroll effects, animations |
| **Blog Engine** | Python 3 | 3.x | Article conversion, metadata management |
| **Hosting** | GitHub Pages | - | Static site hosting with custom domain |
| **Analytics** | Reb2b | - | B2B visitor identification |
| **Fonts** | Google Fonts (Inter) | - | Typography |
| **Version Control** | Git | - | Source control |

### Key Dependencies

**None!** This is a dependency-free static site.

**Python Scripts** (for content management only):
- No `requirements.txt` or `package.json`
- Uses Python 3 standard library only
- Scripts: `add_article.py`, `create_category_indexes.py`, `add_blog_seo.py`

**External Services**:
- **Reb2b**: B2B visitor tracking (`1N5W0HM2RYO5` key in `<script>` tags)
- **Google Fonts**: Inter font family (preconnected for performance)

---

## Key Commands

### Development

```bash
# Start local development server
python3 -m http.server 8000
# Then visit: http://localhost:8000

# Alternative (if you have Python 2)
python -m SimpleHTTPServer 8000
```

### Blog Management

```bash
# Add new blog article from LinkedIn HTML
# 1. Save LinkedIn article HTML to /blog/new-articles/
# 2. Run conversion script
python3 blog/add_article.py --category practical-applications

# Regenerate all category index pages
python3 blog/create_category_indexes.py

# Add SEO improvements to blog pages (canonical tags, breadcrumbs, schemas)
python3 add_blog_seo.py

# Test mode (process only 3 files)
python3 add_blog_seo.py --test

# Dry run (preview changes without modifying files)
python3 add_blog_seo.py --dry-run
```

### AI/LLM Commands

```bash
# Auto-categorize a blog article using AI
python3 blog/anyquest_client.py categorize blog/new-articles/article.html

# Generate case study from technical description
echo "[technical description]" | python3 blog/anyquest_client.py generate-case-study

# Test mode with verbose output
python3 blog/anyquest_client.py categorize blog/new-articles/article.html --verbose
```

### Slash Commands

Available slash commands in `.claude/commands/`:
- `/publish-article` - Publish new blog article (includes AI categorization, sitemap update)
- `/new-case-study` - Create new case study (includes AI generation, CTA customization)
- `/sync-docs` - Update CLAUDE.md based on code changes

### Git Workflow

```bash
# Standard workflow for content updates
git add .
git commit -m "Description of changes"
git push origin main
# GitHub Pages auto-deploys in 1-2 minutes

# Working on design changes (use branch)
git checkout -b design-update
# Make changes...
git commit -m "Update hero section design"
git push origin design-update
# Create PR → Review → Merge to main
```

### Deployment

**Automatic Deployment**: GitHub Pages deploys automatically when you push to `main` branch.

**Manual Steps** (if needed):
1. Verify changes locally with `python3 -m http.server 8000`
2. Push to main: `git push origin main`
3. Wait 1-2 minutes for GitHub Pages to rebuild
4. Visit https://vyceralsolutions.com to verify

---

## Project Structure

```
/
├── index.html                   # Homepage (hero + two-path split)
├── about.html                   # Company story + founder bio
├── contact.html                 # Contact info (no form, direct links)
├── blog.html                    # Blog homepage (featured articles + categories)
├── case-studies.html            # Case study hub (split: GTM vs Consulting)
├── gtm-automation.html          # GTM service page (4 services)
├── consulting-transformation.html  # Consulting service page (4 services)
├── services.html                # Legacy services page (keep for backlinks)
│
├── css/
│   └── style.css                # Single stylesheet (1043 lines, component-based)
│
├── js/
│   └── main.js                  # All JavaScript (152 lines, vanilla JS)
│
├── images/
│   ├── logo.png                 # Main logo (navigation)
│   ├── logo_vs_clear.png        # Logo for Open Graph/social sharing
│   ├── favicon-*.png            # Favicons (16x16, 32x32, 180x180)
│   ├── tools/                   # Platform logos (Clay, Agent.ai, MindStudio, etc.)
│   └── article-images/          # Blog article hero images (slug-based names)
│
├── blog/
│   ├── article-template.html    # Master template with {{VARIABLES}}
│   ├── converted-articles.json  # Registry of all 95 articles
│   ├── articles-metadata.json   # Extended metadata (word count, source file)
│   ├── add_article.py           # Main script for publishing articles
│   ├── create_category_indexes.py  # Rebuild category index pages
│   ├── [8 category folders]/    # ai-agents, practical-applications, etc.
│   │   ├── index.html           # Category landing page
│   │   └── *.html               # Individual articles
│   └── articles-raw/            # Source HTML from LinkedIn (164 files)
│
├── case-studies/
│   ├── healthcare-tech.html
│   ├── data-governance-company.html  # Immuta case study
│   ├── industrial-iot-company.html   # Viaduct case study
│   ├── management-consulting-firm-*.html  # Mann Partners (3 case studies)
│   ├── leadership-development-firm*.html  # CEOWorks (3 case studies)
│   └── bridgeline-search-assessment.html
│
├── docs/                        # Documentation folder (unused)
├── venv/                        # Python virtual environment (not required)
├── CNAME                        # Custom domain: vyceralsolutions.com
├── robots.txt                   # SEO: Allow all, link to sitemap
├── sitemap.xml                  # 651 lines, 104 URLs indexed
├── README.md                    # Project documentation (261 lines)
└── add_blog_seo.py              # Script for adding SEO elements to blog
```

### Key File Locations

| What You Need | Where to Find It | Line Reference |
|---------------|------------------|----------------|
| **Navigation menu** | All HTML files | `<nav class="nav">` around line 90 |
| **Hero section** | index.html, about.html, service pages | `<section class="hero">` |
| **Footer** | All HTML files | `<footer class="footer">` (end of file) |
| **CSS variables** | css/style.css | Lines 7-65 (color, typography, spacing) |
| **Mobile menu JS** | js/main.js | Lines 4-36 (toggle logic) |
| **Blog template** | blog/article-template.html | Template with 8 variables |
| **Article registry** | blog/converted-articles.json | 95 articles with metadata |
| **Sitemap** | sitemap.xml | All URLs for Google indexing |
| **Case study template** | case-studies/*.html | Consistent structure across all 10 |

---

## Database

**N/A** - This is a static site with no database.

**Data Storage**:
- Blog articles: JSON files (`converted-articles.json`, `articles-metadata.json`)
- Content: HTML files (no CMS, no database)
- Images: Static files in `/images/` directory

---

## Authentication

**N/A** - Public website with no authentication.

**Access Control**: None. All content is publicly accessible.

---

## External Integrations

### 1. Reb2b (B2B Visitor Tracking)

**Purpose**: Identify company visitors for sales outreach

**Integration Pattern**:
```html
<script>!function(key){if(window.reb2b)return;window.reb2b={loaded:true};var s=document.createElement("script");s.async=true;s.src="https://b2bjsstore.s3.us-west-2.amazonaws.com/b/"+key+"/"+key+".js.gz";document.getElementsByTagName("script")[0].parentNode.insertBefore(s,document.getElementsByTagName("script")[0]);}("1N5W0HM2RYO5");</script>
```

**Location**: In `<head>` section of most HTML pages (index.html:85, about.html, contact.html, blog.html, case-studies.html, gtm-automation.html, consulting-transformation.html)

**Error Handling**: Script loads asynchronously, fails silently if blocked

**Note**: Not present on service pages or individual blog articles

### 2. Google Fonts (Inter)

**Purpose**: Typography (Inter font family)

**Integration Pattern**:
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
```

**Location**: In `<head>` section of all HTML files

**Performance**: Uses preconnect for faster font loading

### 3. LinkedIn (External Links)

**Purpose**: Social proof and newsletter subscription

**Links**:
- Personal Profile: `https://www.linkedin.com/in/vekambar/`
- Newsletter: `https://www.linkedin.com/newsletters/7158509558993215488`

**Usage**: Footer links, about page, blog article disclaimers

---

## Environment Variables

**Environment Variables** (for AI/LLM integration):
- `.env` file (gitignored) - Contains API keys
- `.env.example` - Template with required variables

**Required Variables**:
| Variable | Purpose | Where Used |
|----------|---------|------------|
| ANYQUEST_API_KEY | LLM API for AI-powered content generation | blog/anyquest_client.py |

**Static Configuration** (hardcoded):
- Domain: Hardcoded in `CNAME` file (`vyceralsolutions.com`)
- Reb2b Key: Hardcoded in HTML (`1N5W0HM2RYO5`)
- Email: Hardcoded in HTML (`vikram.ekambaram@vyceralsolutions.com`)

**Customization Points**:
| Item | File | Location |
|------|------|----------|
| ANYQUEST_API_KEY | .env | Used in blog/anyquest_client.py for case study generation and article categorization |
| Domain | CNAME | Line 1 |
| Company Email | All HTML files | `mailto:` links and schema |
| LinkedIn Profile | All HTML files | Footer and schema |
| Reb2b Tracking Key | HTML `<head>` | Script tag in head section |
| Google Analytics | N/A | Not currently implemented |

---

## Code Style & Conventions

### Naming Conventions

**HTML Files**:
- Kebab-case: `gtm-automation.html`, `case-studies.html`
- Descriptive names matching content: `consulting-transformation.html`

**CSS Classes**:
- BEM-inspired: `.nav`, `.nav-container`, `.nav-menu`, `.nav-link`
- Component-based: `.card`, `.btn`, `.hero`, `.section`
- Modifier pattern: `.btn-primary`, `.btn-outline`, `.btn-large`
- Utility classes: `.bg-light`, `.text-center`, `.glass-panel`

**JavaScript Functions**:
- camelCase: `loadClientLogos()`, `formatNumber()`
- Descriptive names: `mobileToggle`, `navMenu`

**Python Scripts**:
- snake_case: `add_article.py`, `create_category_indexes.py`
- Function names: `extract_title()`, `process_blog_file()`

### File Organization Patterns

**HTML Structure** (Every page follows this pattern):
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Meta tags (charset, viewport, description) -->
  <!-- Canonical URL -->
  <!-- Favicons (3 sizes) -->
  <!-- Open Graph tags -->
  <!-- Twitter Card tags -->
  <!-- Google Fonts -->
  <!-- Stylesheet -->
  <!-- Structured Data (JSON-LD) -->
  <!-- Reb2b tracking script -->
</head>
<body>
  <!-- Navigation -->
  <nav class="nav">...</nav>

  <!-- Breadcrumbs (on non-homepage pages) -->
  <div class="breadcrumbs">...</div>

  <!-- Hero Section -->
  <section class="hero">...</section>

  <!-- Content Sections -->
  <section class="section">...</section>
  <section class="section bg-light">...</section>

  <!-- CTA Section -->
  <section class="section">
    <div class="cta-section">...</div>
  </section>

  <!-- Footer -->
  <footer class="footer">...</footer>

  <!-- JavaScript -->
  <script src="js/main.js"></script>
</body>
</html>
```

**CSS Architecture** (style.css:1-1043):
```css
/* 1. CSS Variables (lines 7-65) */
:root { --color-primary, --font-sans, --space-lg, etc. }

/* 2. Reset & Base Styles (lines 67-91) */
*, html, body { box-sizing, font-family, etc. }

/* 3. Typography (lines 93-150) */
h1-h6, p, a, strong { font-size, weight, color }

/* 4. Layout Utilities (lines 152-167) */
.container, .section { max-width, padding }

/* 5. Components (lines 168-873) */
.nav, .btn, .card, .hero, .footer, etc.

/* 6. Responsive Design (lines 874-988) */
@media queries for tablet and mobile
```

### Component/Function Patterns

**Reusable HTML Components**:

1. **Card Component** (used 50+ times):
```html
<div class="card">
  <h3>Title</h3>
  <p>Description text here.</p>
  <a href="#" class="btn btn-primary">Call to Action →</a>
</div>
```

2. **Button Component**:
```html
<!-- Primary Button -->
<a href="contact.html" class="btn btn-primary">Get Started →</a>

<!-- Outline Button -->
<a href="case-studies.html" class="btn btn-outline">View Case Studies</a>

<!-- Large Button -->
<a href="#" class="btn btn-large btn-primary">Schedule Consultation</a>
```

3. **Badge Component**:
```html
<span class="badge badge-primary">GTM Automation</span>
<span class="badge badge-outline">AnyQuest.ai</span>
```

4. **Section Header** (consistent pattern):
```html
<div class="section-header">
  <h2>Section Title</h2>
  <p>Section subtitle or description goes here.</p>
</div>
```

**JavaScript Patterns**:

```javascript
// Event listeners wrapped in DOMContentLoaded
document.addEventListener('DOMContentLoaded', function() {
  // All initialization code here
});

// Query selectors stored in variables
const mobileToggle = document.querySelector('.mobile-menu-toggle');
const navMenu = document.querySelector('.nav-menu');

// Consistent event handling
element.addEventListener('click', function() {
  // Handle event
});
```

### TypeScript/Typing Patterns

**N/A** - Pure JavaScript (no TypeScript)

**Type Safety**: None. Uses vanilla JavaScript with no type checking.

---

## Testing

**Current Test Setup**: ❌ **None**

**No Testing Infrastructure**:
- No test files
- No testing frameworks
- No CI/CD testing

**Manual Testing Approach**:
1. Visual inspection in browser
2. Test on local server: `python3 -m http.server 8000`
3. Check responsive design (Chrome DevTools)
4. Verify links manually
5. Test on mobile devices

**Recommended Future Testing**:
- Link checking: Use `linkchecker` or similar tool
- HTML validation: W3C Markup Validation Service
- Accessibility: axe DevTools or WAVE
- Performance: Lighthouse in Chrome DevTools

---

## Git Workflow

### Branch Strategy

**Main Branches**:
- `main`: Production branch (auto-deploys to GitHub Pages)
- `design-refresh`: Experimental branch for design updates

**Current Branch**: `design-refresh` (per git status)

### Branching Convention (Inferred from History)

**Pattern**: Feature-based branches
- `design-refresh`: Design system updates
- Direct commits to `main`: Content updates, bug fixes

**Recommended Pattern**:
```bash
# For new features
git checkout -b feature/add-new-service-page

# For bug fixes
git checkout -b fix/mobile-nav-issue

# For content updates
git checkout -b content/add-december-articles
```

### Commit Message Format

**Observed Pattern** (from git log):
```
# Content updates (most common)
Add comprehensive SEO improvements to 103 blog pages (8 categories + 95 articles)
Remove all customer quotes and client personnel names from case studies
Fix LinkedIn URL: Update to correct profile vekambar

# Bug fixes
fix: standardize article image filenames to match article slugs
fix: add hero images to 17 articles that were missing them

# Features
Implement comprehensive SEO improvements: robots.txt, canonical tags, and enhanced schema markup
```

**Recommended: Conventional Commits**
```bash
# Format: <type>: <description>

# Types:
feat: Add new blog category for AI philosophy
fix: Correct mobile navigation hamburger animation
docs: Update README with new deployment instructions
style: Improve hero section gradient and spacing
refactor: Consolidate duplicate CSS rules
content: Add 5 new blog articles from LinkedIn
seo: Update meta descriptions for service pages
```

### PR Guidelines

**Current Process**: No formal PR process observed (direct commits to main)

**Recommended Process**:
1. Create feature branch from `main`
2. Make changes and commit with descriptive messages
3. Push branch to GitHub
4. Create Pull Request with description
5. Self-review (or have teammate review if applicable)
6. Merge to `main` → Triggers automatic deployment

---

## When to Use Extended Thinking

### 🔴 High-Risk Changes (ALWAYS use extended thinking)

**Core Business Logic**:
- Blog publishing scripts (`blog/add_article.py`)
- SEO implementation (`add_blog_seo.py`, `sitemap.xml`)
- Navigation structure changes (affects all pages)
- Footer changes (affects all pages)

**Data Integrity**:
- Modifying `converted-articles.json` (registry of all articles)
- Bulk updates to HTML files
- Image file renaming (breaks links)

**External Integrations**:
- Reb2b tracking script modifications
- Schema.org structured data changes
- Canonical URL updates

**Deployment**:
- CNAME file changes (affects domain routing)
- robots.txt modifications (affects SEO)
- Sitemap.xml updates (affects indexing)

### 🟡 Medium-Risk Changes (Use extended thinking when uncertain)

**Content Pages**:
- Service page restructuring
- Case study template changes
- Blog template modifications

**Styling**:
- CSS variable updates (affects entire site)
- Responsive breakpoint changes
- Component class modifications

**Navigation**:
- Adding/removing menu items
- Breadcrumb structure changes

### 🟢 Low-Risk Changes (Standard thinking OK)

**Content Updates**:
- Adding new blog articles (using existing script)
- Updating text on individual pages
- Adding new images

**Minor Styling**:
- Color adjustments within components
- Spacing tweaks on individual elements
- Hover effect modifications

**Documentation**:
- README updates
- Comment additions
- CLAUDE.md updates

---

## Critical Files List

### Tier 1 - CRITICAL (Data Loss or SEO Catastrophe if Broken)

| File | Why Critical | Review Checklist |
|------|-------------|------------------|
| **CNAME** | Domain routing. Wrong value = site unreachable | ✅ Verify domain is exactly `vyceralsolutions.com`<br>✅ No trailing slash or protocol<br>✅ Single line only |
| **sitemap.xml** | Google indexing. Broken = invisible in search | ✅ Valid XML syntax<br>✅ All URLs use https://vyceralsolutions.com<br>✅ All referenced files actually exist<br>✅ lastmod dates in YYYY-MM-DD format |
| **robots.txt** | Search engine access. Wrong = deindexing | ✅ `Allow: /` is present<br>✅ Sitemap URL is correct<br>✅ No accidental `Disallow: /` |
| **blog/converted-articles.json** | Article registry. Corruption = site-wide blog failure | ✅ Valid JSON syntax (use `jq` to validate)<br>✅ All slugs are unique<br>✅ All paths actually exist<br>✅ Dates in ISO format<br>✅ No duplicate entries |
| **css/style.css** | Entire site styling. Syntax error = unstyled site | ✅ Valid CSS (no unclosed braces)<br>✅ CSS variables defined in :root<br>✅ No !important overuse<br>✅ Test on mobile before deploying |
| **blog/article-template.html** | Master template. Error = all future articles broken | ✅ All 8 template variables present: {{TITLE}}, {{DATE}}, {{CATEGORY}}, {{CATEGORY_SLUG}}, {{READ_TIME}}, {{CONTENT}}, {{META_DESCRIPTION}}, {{SLUG}}<br>✅ Navigation structure intact<br>✅ Footer present<br>✅ Schema.org JSON-LD valid |

### Tier 2 - IMPORTANT (Affects Core User Flows)

| File | Why Important | Review Checklist |
|------|--------------|------------------|
| **index.html** | Homepage. First impression for 80% of visitors | ✅ Hero section compelling<br>✅ Two-path split visible<br>✅ CTAs prominent<br>✅ Links work<br>✅ Reb2b tracking present |
| **blog/add_article.py** | Article publishing. Broken = can't publish content | ✅ Template substitution works<br>✅ Image download logic intact<br>✅ JSON updates successful<br>✅ Dry-run mode before production<br>✅ Test with one article first |
| **js/main.js** | Site interactivity. Broken = poor mobile UX | ✅ Mobile nav toggle works<br>✅ No console errors<br>✅ Smooth scroll functional<br>✅ Animations performant |
| **case-studies.html** | Lead generation hub. Critical for conversions | ✅ All 9 case studies linked<br>✅ Results metrics accurate<br>✅ CTAs prominent<br>✅ Split between GTM and Consulting clear |
| **Navigation (<nav>)** | Appears on all pages. Inconsistency = confusion | ✅ Same menu items on all pages<br>✅ Logo links to index.html<br>✅ Mobile menu functional<br>✅ Active state highlights correct page |
| **Footer (<footer>)** | Appears on all pages. Critical for SEO and trust | ✅ Contact info correct<br>✅ LinkedIn links work<br>✅ Copyright year current<br>✅ All internal links valid |

### Tier 3 - STANDARD (Individual Pages)

- Individual blog articles
- Individual case studies
- About page
- Contact page
- Service pages (gtm-automation.html, consulting-transformation.html)

**Review Checklist for Tier 3**:
- ✅ All links work (no 404s)
- ✅ Images load (check browser console)
- ✅ Mobile responsive
- ✅ SEO tags present (title, description, canonical)
- ✅ Consistent with design system

---

## Important Rules (MUST FOLLOW)

### ✅ DO: HTML & Content

- ✅ **DO** maintain consistent navigation across all pages (same menu items, same order)
- ✅ **DO** use semantic HTML (`<article>`, `<section>`, `<nav>`, `<footer>`)
- ✅ **DO** include canonical URLs on every page
- ✅ **DO** add Open Graph and Twitter Card meta tags for social sharing
- ✅ **DO** use descriptive alt text for all images
- ✅ **DO** keep meta descriptions under 155 characters
- ✅ **DO** use breadcrumbs on non-homepage pages
- ✅ **DO** include JSON-LD structured data (Schema.org)
- ✅ **DO** test pages locally before pushing to production
- ✅ **DO** verify all links work (use Cmd+Click in VS Code)
- ✅ **DO** use relative paths for internal links (`href="case-studies.html"`)
- ✅ **DO** use absolute URLs in sitemaps and canonical tags

### ❌ DON'T: HTML & Content

- ❌ **DON'T** change navigation structure without updating ALL pages
- ❌ **DON'T** remove breadcrumbs (important for SEO)
- ❌ **DON'T** use inline styles except for one-off positioning adjustments
- ❌ **DON'T** forget to update `sitemap.xml` when adding new pages
- ❌ **DON'T** use absolute paths for internal links (breaks local testing)
- ❌ **DON'T** add forms without backend (site is static, no form processing)
- ❌ **DON'T** use `target="_blank"` on internal links (only for LinkedIn, external sites)
- ❌ **DON'T** include client-specific financial data or personal names in case studies
- ❌ **DON'T** add customer testimonials without explicit permission

### ✅ DO: CSS & Design System

- ✅ **DO** use CSS variables from `:root` (lines 7-65 in style.css)
- ✅ **DO** follow component naming convention (`.component`, `.component-element`)
- ✅ **DO** use existing utility classes (`.bg-light`, `.text-center`)
- ✅ **DO** maintain mobile-first responsive design
- ✅ **DO** test on mobile (375px), tablet (768px), desktop (1280px+)
- ✅ **DO** use rem units for typography (not px)
- ✅ **DO** keep hover effects subtle (translateY(-2px) max)
- ✅ **DO** use CSS Grid for layouts (not floats or tables)

### ❌ DON'T: CSS & Design System

- ❌ **DON'T** add new colors without updating CSS variables
- ❌ **DON'T** use inline styles for anything that should be reusable
- ❌ **DON'T** break the component naming convention
- ❌ **DON'T** add media queries outside the responsive section (lines 874-988)
- ❌ **DON'T** use `!important` (except in rare override cases)
- ❌ **DON'T** forget to test mobile menu on small screens
- ❌ **DON'T** add heavy animations (site should stay fast)

### ✅ DO: JavaScript

- ✅ **DO** wrap all code in `DOMContentLoaded` event listener
- ✅ **DO** use vanilla JavaScript (no jQuery or frameworks)
- ✅ **DO** store DOM queries in variables (avoid repeated queries)
- ✅ **DO** add comments for complex logic
- ✅ **DO** test on multiple browsers (Chrome, Safari, Firefox)
- ✅ **DO** handle edge cases (elements might not exist on all pages)

### ❌ DON'T: JavaScript

- ❌ **DON'T** add JavaScript frameworks (keep it lightweight)
- ❌ **DON'T** manipulate DOM before DOMContentLoaded fires
- ❌ **DON'T** add JavaScript that breaks without it (progressive enhancement)
- ❌ **DON'T** forget to check browser console for errors
- ❌ **DON'T** query DOM in loops (store reference first)

### ✅ DO: Blog Management

- ✅ **DO** use `add_article.py` script for publishing articles
- ✅ **DO** save source HTML to `/blog/new-articles/` first
- ✅ **DO** verify article renders correctly before committing
- ✅ **DO** ensure hero image exists at `/images/article-images/{slug}.jpg`
- ✅ **DO** regenerate category indexes after adding articles
- ✅ **DO** verify `converted-articles.json` is valid JSON after updates
- ✅ **DO** use descriptive, SEO-friendly slugs (kebab-case)
- ✅ **DO** assign articles to correct category (8 options available)

### ❌ DON'T: Blog Management

- ❌ **DON'T** manually edit `converted-articles.json` (use scripts)
- ❌ **DON'T** forget to download/add hero image for new articles
- ❌ **DON'T** use duplicate slugs (causes URL collisions)
- ❌ **DON'T** skip regenerating category indexes (will show wrong count)
- ❌ **DON'T** commit half-finished articles (breaks category pages)
- ❌ **DON'T** change article template variables without updating script
- ❌ **DON'T** edit HTML articles directly (make changes to template instead)

### ✅ DO: Git & Deployment

- ✅ **DO** test locally before pushing to `main`
- ✅ **DO** write descriptive commit messages (explain WHY, not just WHAT)
- ✅ **DO** commit related changes together (not scattered commits)
- ✅ **DO** use feature branches for experimental changes
- ✅ **DO** verify GitHub Pages deploys successfully (check site in 2-3 minutes)
- ✅ **DO** keep commits atomic (one logical change per commit)

### ❌ DON'T: Git & Deployment

- ❌ **DON'T** commit broken code to `main` branch
- ❌ **DON'T** push without testing locally first
- ❌ **DON'T** commit sensitive data (API keys, emails, personal info)
- ❌ **DON'T** force push to `main` (destroys history)
- ❌ **DON'T** commit large binary files (compress images first)
- ❌ **DON'T** make changes directly on GitHub web UI (use local environment)

### ✅ DO: SEO & Performance

- ✅ **DO** update sitemap.xml when adding pages
- ✅ **DO** use descriptive title tags (50-60 characters)
- ✅ **DO** include meta descriptions on all pages
- ✅ **DO** compress images before uploading (use ImageOptim or similar)
- ✅ **DO** use descriptive filenames for images (not IMG_1234.jpg)
- ✅ **DO** verify structured data with Google's Rich Results Test
- ✅ **DO** check page speed with Lighthouse
- ✅ **DO** use semantic HTML for accessibility

### ❌ DON'T: SEO & Performance

- ❌ **DON'T** forget to add new pages to sitemap.xml
- ❌ **DON'T** use duplicate meta descriptions across pages
- ❌ **DON'T** upload huge images (>500KB) without compression
- ❌ **DON'T** change URLs without adding redirects (breaks backlinks)
- ❌ **DON'T** remove canonical tags (causes duplicate content issues)
- ❌ **DON'T** block search engines in robots.txt by accident
- ❌ **DON'T** break structured data JSON (validates with JSON-LD validator)

### ✅ DO: Security & Privacy

- ✅ **DO** use HTTPS for all external links
- ✅ **DO** keep Reb2b tracking script up to date
- ✅ **DO** sanitize any user-provided content (if ever added)
- ✅ **DO** use `rel="noopener"` on external links with `target="_blank"`

### ❌ DON'T: Security & Privacy

- ❌ **DON'T** commit API keys or credentials
- ❌ **DON'T** include client-confidential information in public case studies
- ❌ **DON'T** expose personal contact information beyond business email
- ❌ **DON'T** add tracking scripts without understanding privacy implications

---

## Quick Reference Commands

```bash
# Local Development
python3 -m http.server 8000        # Start local server
open http://localhost:8000          # Open in browser (macOS)

# Blog Article Publishing
python3 blog/add_article.py --category practical-applications
python3 blog/create_category_indexes.py
python3 add_blog_seo.py

# Git Workflow
git status                          # Check what changed
git add .                           # Stage all changes
git commit -m "Description"         # Commit with message
git push origin main                # Deploy to production
git log --oneline -10               # View recent commits
git diff                            # See unstaged changes

# File Navigation
code .                              # Open project in VS Code
ls -la                              # List all files
find . -name "*.html" -type f       # Find all HTML files

# Image Optimization (if installed)
imageoptim-cli --directory images/article-images/  # Compress images

# Link Checking (if installed)
linkchecker http://localhost:8000   # Check for broken links

# Git Branch Management
git branch                          # List local branches
git checkout -b feature/new-page    # Create new branch
git merge feature/new-page          # Merge branch into current
git branch -d feature/new-page      # Delete branch after merge
```

---

## Common Tasks

### Adding a New Blog Article

**Prerequisites**:
- LinkedIn article HTML saved to `/blog/new-articles/filename.html`
- Hero image ready (JPEG, 1200x400px recommended)

**Steps**:
```bash
# 1. Save LinkedIn HTML to inbox folder
# (Manual: Copy HTML from LinkedIn, save to /blog/new-articles/)

# 2. Run article conversion script
python3 blog/add_article.py --category practical-applications
# Script will:
# - Extract title, date, content
# - Calculate read time
# - Download/process hero image
# - Generate article HTML from template
# - Update converted-articles.json
# - Regenerate category index

# 3. Verify article renders correctly
python3 -m http.server 8000
# Visit: http://localhost:8000/blog/practical-applications/article-slug.html

# 4. Commit and deploy
git add .
git commit -m "Add new blog article: [Article Title]"
git push origin main

# 5. Verify live site in 2-3 minutes
# Visit: https://vyceralsolutions.com/blog/practical-applications/article-slug.html
```

**Available Categories** (must use exact slug):
- `ai-agents` - AI Agents & Agentic Systems
- `ai-philosophy` - AI Philosophy & Future of Work
- `gtm-strategy` - Business & GTM Strategy
- `industry-research` - Industry Research & Insights
- `personal-journey` - Personal Journey & Entrepreneurship
- `practical-applications` - Practical Applications & Use Cases
- `technical-analysis` - Technical Deep Dives & Analysis
- `tools-platforms` - GenAI Tools & Platforms

### Adding a New Case Study

**Prerequisites**:
- Client approval for public case study
- Results metrics verified
- Hero image or diagram ready

**Steps**:
```bash
# 1. Copy existing case study as template
cp case-studies/healthcare-tech.html case-studies/new-client.html

# 2. Edit new-client.html
# Update these sections:
# - <head>: Title, meta description, Open Graph tags
# - <head>: Article schema (headline, description, datePublished)
# - Badge: Category (e.g., "B2B SaaS", "Industrial IoT")
# - Title & tagline
# - Client name, industry, technologies
# - Results metrics (3 cards)
# - Challenge & Solution boxes
# - Impact & Results (4 cards)

# 3. Update case-studies.html
code case-studies.html
# Add new card to appropriate section:
# - Consulting Transformation section OR
# - GTM Automation section

<div class="card">
  <span class="badge badge-primary">Category</span>
  <h3>Client Name</h3>
  <p class="tagline">One-line Description</p>
  <div class="stats" style="margin: 1rem 0;">
    <div style="display: flex; gap: 2rem; flex-wrap: wrap;">
      <div><strong>XX%</strong> Metric 1</div>
      <div><strong>Xx</strong> Metric 2</div>
      <div><strong>X weeks</strong> Metric 3</div>
    </div>
  </div>
  <p><strong>Challenge:</strong> Brief description</p>
  <p><strong>Solution:</strong> Brief description</p>
  <a href="case-studies/new-client.html" class="btn btn-primary">Read Full Case Study →</a>
</div>

# 4. Update sitemap.xml
code sitemap.xml
# Add new URL entry (copy existing case study entry and modify)

# 5. Test locally
python3 -m http.server 8000
# Visit case study and verify all links work

# 6. Commit and deploy
git add case-studies/new-client.html case-studies.html sitemap.xml
git commit -m "Add [Client Name] case study: [Brief Description]"
git push origin main
```

### Updating Service Pages

**Files to Edit**:
- `gtm-automation.html` (4 GTM services)
- `consulting-transformation.html` (4 consulting services)

**Common Updates**:
1. **Add New Service**: Copy existing service card, update content
2. **Update Pricing**: No pricing on site (keep as "contact for pricing")
3. **Add Platform Badge**: Use existing platforms or add new logo to `/images/tools/`

**Steps**:
```bash
# 1. Edit service page
code gtm-automation.html

# 2. Find service grid section
# Look for: <div class="grid grid-2">

# 3. Add or modify service card
<div class="card">
  <div class="card-icon">🎯</div>
  <h3>Service Name</h3>
  <p>Service description highlighting benefits and outcomes.</p>
  <div class="platform-badges">
    <span class="platform-badge">
      <img src="images/tools/platform-logo.png" alt="Platform Name">
      Platform Name
    </span>
  </div>
  <ul style="text-align: left; margin-top: 1rem;">
    <li>Benefit 1</li>
    <li>Benefit 2</li>
    <li>Benefit 3</li>
  </ul>
</div>

# 4. Test locally
python3 -m http.server 8000

# 5. Commit and deploy
git add gtm-automation.html
git commit -m "Update GTM services: Add [Service Name]"
git push origin main
```

### Debugging Common Issues

**Issue: Site loads but unstyled**
```bash
# Check if CSS file exists and is linked correctly
ls -la css/style.css
grep "style.css" index.html
# Verify no syntax errors in CSS
# Check browser console for 404 errors
```

**Issue: Mobile menu not working**
```bash
# Check if JavaScript is loaded
ls -la js/main.js
grep "main.js" index.html
# Open browser console, look for errors
# Verify mobile-menu-toggle button exists in HTML
```

**Issue: Blog article not showing**
```bash
# Verify article exists
ls -la blog/practical-applications/article-slug.html

# Check if article is in registry
grep "article-slug" blog/converted-articles.json

# Regenerate category index
python3 blog/create_category_indexes.py

# Verify category index updated
open blog/practical-applications/index.html
```

**Issue: Images not loading**
```bash
# Check if image exists
ls -la images/article-images/article-slug.jpg

# Verify image path in HTML
grep "article-slug.jpg" blog/practical-applications/article-slug.html

# Check image file size (should be <500KB)
du -h images/article-images/article-slug.jpg

# If too large, compress:
# Use ImageOptim, TinyPNG, or similar tool
```

**Issue: GitHub Pages not deploying**
```bash
# Check if commit pushed to main branch
git log --oneline -3
git branch

# Verify CNAME file exists
cat CNAME
# Should output: vyceralsolutions.com

# Check GitHub Pages settings:
# Go to: github.com/[username]/VyceralSolutions.com/settings/pages
# Verify: Source = main branch, / (root)

# Wait 2-3 minutes for deployment
# Check GitHub Actions tab for build status
```

---

## Production Deployment Checklist

Before pushing to `main` branch:

### Pre-Deployment Checks
- [ ] Test all changed pages locally (`python3 -m http.server 8000`)
- [ ] Verify all links work (Cmd+Click in VS Code)
- [ ] Check mobile responsiveness (Chrome DevTools)
- [ ] Verify images load (check browser console for 404s)
- [ ] Run HTML validator on changed pages (validator.w3.org)
- [ ] Check for broken images (view Network tab in browser)
- [ ] Verify JavaScript has no console errors
- [ ] Test mobile menu on small screen (<768px)

### SEO Checks (If Applicable)
- [ ] Updated `sitemap.xml` with new pages
- [ ] Added canonical URLs to new pages
- [ ] Included meta descriptions (<155 chars)
- [ ] Added Open Graph tags for social sharing
- [ ] Verified JSON-LD structured data (use Google Rich Results Test)
- [ ] Checked that robots.txt still allows crawling

### Git Workflow
- [ ] Commit with descriptive message
- [ ] Verify you're on correct branch (`git branch`)
- [ ] Push to main: `git push origin main`
- [ ] Wait 2-3 minutes for GitHub Pages deployment
- [ ] Verify live site: https://vyceralsolutions.com
- [ ] Check GitHub Actions tab for successful deploy

### Post-Deployment Verification
- [ ] Visit homepage: https://vyceralsolutions.com
- [ ] Click through navigation menu (all links work)
- [ ] Test on mobile device (or Chrome DevTools mobile view)
- [ ] Verify new content appears correctly
- [ ] Check browser console for errors (F12)
- [ ] Test any changed functionality (forms, nav, etc.)

---

**Last Updated**: December 4, 2025

**Project Status**: Production (actively deployed at vyceralsolutions.com)

**Primary Maintainer**: Vikram Ekambaram (vikram.ekambaram@vyceralsolutions.com)

**Tech Stack Version**: Static HTML/CSS/JS (no version dependencies)
