# Blog System Architecture Diagram

## System Flow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        LINKEDIN NEWSLETTER                       │
│                    "GenAI for Go-To-Market teams"               │
│                                                                  │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐               │
│  │  Article   │  │  Article   │  │  Article   │  ... (160+)   │
│  │     #1     │  │     #2     │  │     #3     │               │
│  └────────────┘  └────────────┘  └────────────┘               │
└─────────────────────────────────────────────────────────────────┘
         │                 │                 │
         └─────────────────┼─────────────────┘
                           │ Export as HTML
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                       blog/articles-raw/                         │
│                                                                  │
│  article-title-vikram-ekambaram-hash1.html                      │
│  article-title-vikram-ekambaram-hash2.html                      │
│  article-title-vikram-ekambaram-hash3.html                      │
│  ... (160+ files)                                               │
└─────────────────────────────────────────────────────────────────┘
                           │
                           │ convert_articles.py
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CONVERSION PIPELINE                           │
│                                                                  │
│  ┌──────────────────┐       ┌──────────────────┐               │
│  │  Extract Content │       │   Categorize     │               │
│  │  - Title         │  ───> │   - Keywords     │               │
│  │  - Date          │       │   - AI (future)  │               │
│  │  - HTML          │       │   - 8 categories │               │
│  └──────────────────┘       └──────────────────┘               │
│           │                           │                          │
│           └───────────┬───────────────┘                          │
│                       │                                          │
│  ┌──────────────────┐ │ ┌──────────────────┐                   │
│  │  Generate Slug   │ │ │  Apply Template  │                   │
│  │  - URL-safe      │ │ │  - Variables     │                   │
│  │  - 80 char max   │ │ │  - Navigation    │                   │
│  └──────────────────┘ │ └──────────────────┘                   │
│                       │                                          │
│                       ▼                                          │
│  ┌─────────────────────────────────────────────┐               │
│  │        blog/{category}/{slug}.html          │               │
│  └─────────────────────────────────────────────┘               │
└─────────────────────────────────────────────────────────────────┘
                           │
                           │ Output
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CONVERTED ARTICLES                            │
│                                                                  │
│  blog/                                                           │
│    ├── ai-agents/                                               │
│    │   ├── index.html                                           │
│    │   ├── agent-builders-a-new-ui-paradigm.html               │
│    │   ├── autonomous-agents-it-all-started-with-manus.html    │
│    │   └── ... (15 articles)                                    │
│    │                                                             │
│    ├── gtm-strategy/                                            │
│    │   ├── index.html                                           │
│    │   └── ... (12 articles)                                    │
│    │                                                             │
│    ├── practical-applications/                                  │
│    │   ├── index.html                                           │
│    │   └── ... (27 articles)                                    │
│    │                                                             │
│    └── [6 more categories...]                                   │
│                                                                  │
│  + converted-articles.json (master index)                       │
│  + articles-metadata.json (metadata)                            │
└─────────────────────────────────────────────────────────────────┘
                           │
                           │ create_category_indexes.py
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CATEGORY INDEX PAGES                          │
│                                                                  │
│  blog/ai-agents/index.html                                      │
│  blog/gtm-strategy/index.html                                   │
│  blog/practical-applications/index.html                         │
│  ... (8 category indexes)                                       │
└─────────────────────────────────────────────────────────────────┘
                           │
                           │ generate_blog_page.py
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BLOG LANDING PAGE                             │
│                                                                  │
│  blog/featured-articles.html  ──┐                               │
│  (6 newest articles)            │ Manual copy                   │
│                                 └───────> blog.html             │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Detail

```
┌─────────────────────┐
│  LinkedIn Article   │
│  (HTML Export)      │
└──────────┬──────────┘
           │
           ▼
    ┌────────────┐
    │ BeautifulSoup │
    │   Parser     │
    └──────┬───────┘
           │
           ├─────────────────┐
           │                 │
           ▼                 ▼
    ┌──────────┐      ┌─────────────┐
    │ Metadata │      │   Content   │
    │  Title   │      │    HTML     │
    │  Date    │      │   (clean)   │
    │  Author  │      └──────┬──────┘
    └────┬─────┘             │
         │                   │
         └────────┬──────────┘
                  │
                  ▼
         ┌────────────────┐
         │ Categorization │
         │  (keywords)    │
         └────────┬───────┘
                  │
                  ▼
         ┌────────────────┐
         │  Slug Creation │
         │   (URL-safe)   │
         └────────┬───────┘
                  │
                  ▼
         ┌────────────────┐
         │    Template    │
         │   Processing   │
         └────────┬───────┘
                  │
                  ▼
         ┌────────────────┐
         │  HTML Output   │
         │   + JSON Index │
         └────────────────┘
```

## Template System Architecture

```
┌──────────────────────────────────────────────────────────┐
│                   article-template.html                   │
│                                                           │
│  ┌────────────────────────────────────────────────┐     │
│  │              Navigation (site-wide)             │     │
│  └────────────────────────────────────────────────┘     │
│                                                           │
│  ┌────────────────────────────────────────────────┐     │
│  │   Breadcrumbs: Home > Blog > {{CATEGORY}}      │     │
│  └────────────────────────────────────────────────┘     │
│                                                           │
│  ┌────────────────────────────────────────────────┐     │
│  │        Hero Image: {{SLUG}}.jpg (optional)     │     │
│  └────────────────────────────────────────────────┘     │
│                                                           │
│  ┌────────────────────────────────────────────────┐     │
│  │  Article Header (gradient background)          │     │
│  │    - Category Badge: {{CATEGORY}}              │     │
│  │    - Title: {{TITLE}}                          │     │
│  │    - Meta: {{DATE}} • {{READ_TIME}} min read   │     │
│  └────────────────────────────────────────────────┘     │
│                                                           │
│  ┌────────────────────────────────────────────────┐     │
│  │  Article Content                                │     │
│  │    {{CONTENT}}                                  │     │
│  │    (styled: typography, images, code, etc)     │     │
│  └────────────────────────────────────────────────┘     │
│                                                           │
│  ┌────────────────────────────────────────────────┐     │
│  │  Footer: LinkedIn CTA                          │     │
│  └────────────────────────────────────────────────┘     │
│                                                           │
│  ┌────────────────────────────────────────────────┐     │
│  │  CTA Section: Contact / Case Studies           │     │
│  └────────────────────────────────────────────────┘     │
│                                                           │
│  ┌────────────────────────────────────────────────┐     │
│  │  Site Footer (site-wide)                       │     │
│  └────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────┘
```

## Category Organization

```
Blog Structure
│
├── 🤖 AI Agents (15 articles)
│   ├── Agent builders, MCP, Anthropic
│   └── Autonomous systems
│
├── 🧠 AI Philosophy (6 articles)
│   ├── Future of work
│   └── AI ethics & impact
│
├── 🎯 GTM Strategy (12 articles)
│   ├── Go-to-market automation
│   └── Sales & customer success
│
├── 🏭 Industry Research (4 articles)
│   └── Industry-specific insights
│
├── 🚀 Personal Journey (13 articles)
│   ├── Entrepreneurship
│   └── Business setup
│
├── 💡 Practical Applications (27 articles)
│   ├── Tutorials & how-tos
│   └── Use case implementations
│
├── ⚙️ Technical Analysis (7 articles)
│   ├── Architecture & APIs
│   └── Technical deep dives
│
└── 🛠️ Tools & Platforms (13 articles)
    ├── GenAI tools
    └── Platform reviews
```

## File Dependency Map

```
┌────────────────────────────────────────────────────┐
│                Source Files                        │
├────────────────────────────────────────────────────┤
│  blog/articles-raw/*.html (160+ files)             │
│  blog/article-template.html                        │
│  images/article-images/*.jpg                       │
└────────────┬───────────────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────────────┐
│              Python Scripts                        │
├────────────────────────────────────────────────────┤
│  convert_articles.py           (main conversion)   │
│  create_category_indexes.py    (category pages)    │
│  generate_blog_page.py         (featured articles) │
│  fix_missing_hero_images.py    (image check)       │
└────────────┬───────────────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────────────┐
│             Generated Files                        │
├────────────────────────────────────────────────────┤
│  blog/{category}/{slug}.html   (81+ articles)      │
│  blog/{category}/index.html    (8 indexes)         │
│  blog/converted-articles.json  (master index)      │
│  blog/articles-metadata.json   (metadata)          │
│  blog/featured-articles.html   (featured cards)    │
└────────────┬───────────────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────────────┐
│              Website Pages                         │
├────────────────────────────────────────────────────┤
│  blog.html                     (landing page)      │
│  └─> includes featured-articles.html (manual)      │
└────────────────────────────────────────────────────┘
```

## User Journey Flow

```
                    User arrives at website
                            │
                            ▼
                   ┌─────────────────┐
                   │   blog.html     │
                   │  (Landing Page) │
                   └────────┬────────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
            ▼               ▼               ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │   Featured   │ │   Browse     │ │   Category   │
    │   Article    │ │  Categories  │ │    Badge     │
    └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
           │                │                │
           │                ▼                │
           │    ┌─────────────────────┐     │
           │    │ Category Index Page │     │
           │    │  (e.g., ai-agents/) │     │
           │    └──────────┬──────────┘     │
           │               │                │
           └───────────────┼────────────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Individual      │
                  │ Article Page    │
                  └────────┬────────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
            ▼              ▼              ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐
    │ LinkedIn │   │ Contact  │   │  Case    │
    │   CTA    │   │   CTA    │   │ Studies  │
    └──────────┘   └──────────┘   └──────────┘
```

## Build & Deploy Process

```
┌─────────────────┐
│ Developer Local │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│   Add new LinkedIn HTML to articles-raw │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│   Run Python Scripts                    │
│   1. convert_articles.py                │
│   2. create_category_indexes.py         │
│   3. generate_blog_page.py              │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│   Add hero images to article-images/    │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│   Manual: Copy featured-articles.html   │
│           content to blog.html          │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│   Test locally in browser               │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│   Git commit & push                     │
│   - blog/{category}/                    │
│   - images/article-images/              │
│   - blog.html                           │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│   Static Site Deployment                │
│   (Netlify / Vercel / GitHub Pages)     │
└─────────────────────────────────────────┘
```

## Error Handling Flow

```
                 Article Processing
                        │
                        ▼
              ┌─────────────────┐
              │ Extract Content │
              └────────┬────────┘
                       │
                ┌──────┴──────┐
                │             │
          Error │             │ Success
                │             │
                ▼             ▼
        ┌──────────┐   ┌──────────┐
        │   Log    │   │ Continue │
        │   Skip   │   │ Process  │
        └──────────┘   └────┬─────┘
                            │
                     ┌──────┴──────┐
                     │             │
               Error │             │ Success
                     │             │
                     ▼             ▼
             ┌──────────┐   ┌──────────┐
             │ Fallback │   │ Generate │
             │ Category │   │   HTML   │
             └────┬─────┘   └────┬─────┘
                  │              │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │ Write Output │
                  └──────────────┘
```

---

**Diagram Version**: 1.0
**Last Updated**: November 25, 2025
