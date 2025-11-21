# Vyceral Solutions LLC - Company Website

Modern, multi-page website for Vyceral Solutions LLC - a GenAI consulting firm specializing in go-to-market automation for B2B software companies.

## Overview

**Tagline:** Deep Understanding → Tangible Outcomes

Vyceral Solutions helps B2B software companies transform their go-to-market strategies using Generative AI, reducing manual work by 60-75% while improving personalization and results.

### Core Services

1. **Account & Executive Research** - AI agents that reduce research time from 2-3 hours to 30 minutes
2. **Case Study Intelligence** - Intelligent matching of prospect characteristics with customer success stories
3. **Website Visitor Conversion** - Automated qualification pipeline using Warmly + Agent.ai + Clay + SalesLoft
4. **Personalized Landing Pages** - Dynamic page generation using Agent.ai + Clay + Webflow

### Platform Expertise

- **AnyQuest.ai** - Enterprise-grade AI agent orchestration
- **Agent.ai** - Rapid AI agent development
- **MindStudio.ai** - Research automation and data gathering
- **Clay** - Data orchestration and workflow automation
- **Warmly** - Website visitor identification
- **SalesLoft** - Sales engagement automation

## File Structure

```
/
├── index.html                 # Home page
├── services.html              # Services overview
├── case-studies.html          # Case studies overview
├── about.html                 # About the company
├── blog.html                  # Blog index
├── contact.html               # Contact page
├── css/
│   └── style.css             # Global stylesheet with design system
├── js/
│   └── main.js               # JavaScript for navigation and interactions
├── images/
│   ├── logo.png              # Company logo (add your logo here)
│   ├── tools/                # Platform/tool logos
│   └── case-studies/         # Case study screenshots and diagrams
├── case-studies/
│   ├── mann-partners-intelligence.html
│   ├── ceoworks.html
│   └── [additional case studies]
└── blog/
    └── [individual blog posts]
```

## Design System

### Color Palette

- **Primary:** `#1E40AF` - Deep navy/dark blue
- **Accent:** `#3B82F6` - Bright blue
- **Dark:** `#1F2937` - Dark backgrounds
- **Gray:** `#94A3B8` - Neutral gray (inspired by logo gear)
- **White:** `#FFFFFF` - Clean whites for contrast
- **Light Gray:** `#F1F5F9` - Background sections

### Typography

- **Font Family:** System fonts (-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', 'Roboto', sans-serif)
- **Approach:** Large bold typography, generous white space, clean hierarchy
- **Style:** Bold/Modern Tech (inspired by Vercel, Linear, Anthropic)

### Components

The CSS includes reusable components:
- Navigation (fixed header with mobile menu)
- Hero sections
- Cards with hover effects
- Grid layouts (2, 3, 4 column)
- Buttons (primary, outline, large)
- Badges and tags
- Stats displays
- Footer

## Deployment to GitHub Pages

### Prerequisites

- GitHub account
- Git installed locally

### Step-by-Step Deployment

1. **Initialize Git Repository**
   ```bash
   cd "/Users/vikramekambaram/Vyceral Documents/Applications/VyceralSolutions.com"
   git init
   git add .
   git commit -m "Initial commit: Vyceral Solutions website"
   ```

2. **Create GitHub Repository**
   - Go to [GitHub](https://github.com) and create a new repository
   - Name it `VyceralSolutions.com` or your preferred name
   - Don't initialize with README (we already have one)

3. **Connect Local to Remote**
   ```bash
   git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
   git branch -M main
   git push -u origin main
   ```

4. **Enable GitHub Pages**
   - Go to your repository on GitHub
   - Click **Settings**
   - Scroll to **Pages** section (left sidebar)
   - Under **Source**, select branch: `main`
   - Select folder: `/ (root)`
   - Click **Save**

5. **Wait for Deployment**
   - GitHub will build and deploy your site
   - Usually takes 1-2 minutes
   - Your site will be live at: `https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/`

### Custom Domain (Optional)

To use a custom domain like `vyceralsolutions.com`:

1. **Add CNAME file**
   - Create a file named `CNAME` (no extension) in the root directory
   - Add your domain: `www.vyceralsolutions.com`

2. **Configure DNS**
   - In your domain registrar (GoDaddy, Namecheap, etc.):
   - Add a CNAME record: `www` pointing to `YOUR-USERNAME.github.io`
   - Or add A records pointing to GitHub's IP addresses:
     ```
     185.199.108.153
     185.199.109.153
     185.199.110.153
     185.199.111.153
     ```

3. **Update GitHub Pages Settings**
   - Go to repository Settings → Pages
   - Enter your custom domain
   - Enable "Enforce HTTPS" (recommended)

## Before You Launch

### Add Your Content

1. **Logo**
   - Add your company logo to `images/logo.png`
   - Recommended size: 200px height, transparent background
   - Format: PNG or SVG

2. **Platform Logos**
   - Add logos for Clay, AnyQuest, Agent.ai, MindStudio, Warmly, SalesLoft
   - Place in `images/tools/` directory

3. **Case Study Images**
   - Add screenshots, diagrams, or workflow images
   - Place in `images/case-studies/` directory
   - Reference in case study HTML files

4. **Client Logos** (if available)
   - Add client logos to `images/clients/` directory
   - Update home page client logos section

### Update Contact Information

Ensure all contact links are correct:
- Email: `vikram.ekambaram@vyceralsolutions.com`
- LinkedIn: Update with actual profile URL
- Location: Croton-on-Hudson, NY

### Test Locally

Before deploying, test the website locally:

1. **Using Python's built-in server:**
   ```bash
   python3 -m http.server 8000
   ```
   Then open: `http://localhost:8000`

2. **Or use VS Code Live Server extension**
   - Install "Live Server" extension
   - Right-click `index.html`
   - Select "Open with Live Server"

### SEO & Performance

- All pages include meta descriptions
- Semantic HTML structure
- Mobile-responsive design
- Fast loading (no heavy dependencies)
- Clean, crawlable URLs

## Future Enhancements

### Content to Add

1. **Blog Posts** - Add individual blog post pages in `/blog/` directory
2. **Additional Case Studies** - Create pages for:
   - Healthcare Tech Company
   - Bridgeline Digital
   - Viaduct
   - Vertosoft

3. **Testimonials** - Add more client quotes and testimonials
4. **Video Content** - Embed demo videos or client testimonials
5. **Contact Form Backend** - Integrate with form service (FormSpree, Netlify Forms, etc.)

### Technical Improvements

1. **Analytics** - Add Google Analytics or similar
2. **Form Handling** - Set up contact form submission (currently client-side only)
3. **Newsletter** - Integrate email newsletter service
4. **Performance** - Add image optimization and lazy loading
5. **Accessibility** - Further WCAG compliance testing

## Maintenance

### Regular Updates

- **Blog Posts:** Add monthly articles cross-posted from LinkedIn
- **Case Studies:** Update with new client success stories
- **Services:** Evolve service descriptions based on market feedback
- **Results:** Keep metrics and results current

### Git Workflow

When making updates:
```bash
git add .
git commit -m "Description of changes"
git push origin main
```

GitHub Pages will automatically rebuild and deploy.

## Support

For questions or issues with the website:
- **Developer:** Contact Claude Code support
- **Content Updates:** Edit HTML files directly
- **Design Changes:** Modify `css/style.css`

## License

Copyright © 2025 Vyceral Solutions LLC. All rights reserved.

---

Built with HTML, CSS, and JavaScript. Designed for GitHub Pages deployment.

**Built by:** Claude Code
**Date:** November 2024
**Version:** 1.0
