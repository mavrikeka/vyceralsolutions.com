# Optimized Case Study Generation Prompt (v3.0)

**Version:** 3.0 (Optimized through 3-round iterative testing)
**Date:** 2025-12-04
**Status:** All test inputs score 4+ across all criteria ✅

---

## Prompt

You are writing a case study for Vyceral Solutions' website. Given a technical description of an application, generate a case study following this exact structure and tone.

### Structure to follow:

- Header tags — [Industry] | [Project Type] (e.g., "Leadership Development | Community Tool")
- Title — "[Client Type]: [Descriptive Name of Capability]"
- One-line hook — A single sentence explaining what the tool does and the key insight it demonstrates
- Metadata table — Client, Industry, Project Type, Technologies
- Results at a Glance — 3 key metrics/deliverables with short labels
- The Challenge — 3 bullets describing the problem, ending with a "The Learning:" callout that captures the strategic insight
- The Solution — Deliverables list (4 items) + Strategic Approach (4 items) + "The Learning:" callout
- Measurable Business Impact — 4 quadrants (Efficiency Gains, System Performance, [Value Category], Strategic Benefits) with 4 bullets each
- CTA section — Not needed in output

---

## Technology Translation Rules

**Core Translations:**
- React, Next.js, Node, Express, or similar frameworks → **"Claude Code"**
- Vercel, Heroku, AWS, GCP, or deployment platforms → **"Railway"**
- LLM, language model, OpenAI, Anthropic, or AI API → **"AnyQuest"**
- Never say "AnyQuest LLM" — just **"AnyQuest"**

**Technologies Line:**
- Typical format: "AnyQuest, Claude Code, Railway"
- Exception: Named third-party integrations (Clay, MindStudio, Google Docs API, Airtable) are acceptable when they're specific integrations

**Decision Rule:**
- Generic tech component (database, server, frontend) → Translate to Claude Code/Railway
- Named third-party integration (Clay, Google Docs API) → Keep specific name

---

## Abstraction Rules

Frame the case study around the **generalizable capability**, not the specific use case. The specific project is an example of the broader concept.

**Ask yourself:** "What is the reusable product or approach here?" — then lead with that.

### Abstraction Examples:

| Too Narrow ❌ | Abstracted ✅ |
|--------------|--------------|
| Community survey for T2V practitioners | AI-Enabled Intelligent Survey |
| Built for 5-10 responses | Built for contexts where qualitative depth matters more than statistical scale |
| Community pilots | Research contexts with constrained sample sizes |
| T2V community insights | Stakeholder feedback collection |
| Resume Screening System | Multi-Criteria Candidate Evaluation Platform |
| Pitch Pack Automation | Automated Proposal Development System |

### Title Abstraction Checklist:

1. Does the title describe a capability that could apply to multiple contexts? (not just this one client)
2. Would a different company in a different industry see themselves in this title?
3. Is it one level of abstraction above the specific implementation?

### Title Abstraction: Specific Patterns to Avoid

❌ **Avoid job-function-specific titles:**
- "Resume Screening" → Use **"Candidate Evaluation"** or **"Multi-Criteria Assessment"**
- "Pitch Pack Creation" → Use **"Proposal Development"** or **"Document Generation"**
- "Email Writing" → Use **"Outreach Personalization"** or **"Communication Generation"**

❌ **Avoid medium-specific titles:**
- "Survey Application" → Use **"Research Platform"** or **"Data Collection System"**
- "Mobile App" → Focus on the capability, not the form factor
- "Dashboard" → Focus on the insight or workflow, not the UI

✅ **Prefer capability-level abstraction:**
- What capability does this system provide that could apply in other contexts?
- Example: "Resume Screening" is specific → "Multi-Criteria Candidate Evaluation" is generalizable to vendor selection, proposal evaluation, application scoring, etc.

### Title Quality Examples:

| Score | Title | Reasoning |
|-------|-------|-----------|
| ❌ 2 | "Executive Resume Screening for Search Firms" | Too narrow—specific to one function and industry |
| ⚠️ 3 | "AI-Powered Resume Screening System" | Better, but "resume" is still narrow |
| ✅ 4 | "Multi-Criteria Candidate Evaluation System" | Good—generalizable to candidates, vendors, applicants |
| ✅ 5 | "Structured Assessment Platform" | Excellent—applies to any multi-criteria evaluation |

### Section-Level Abstraction:

**The Challenge** should describe the **general problem category**, with the specific use case as one example:
- ❌ "Community pilots often get only 5-10 responses"
- ✅ "Many research contexts—executive feedback, community pilots, qualitative studies—involve small samples where traditional surveys fail"

**The Solution** should position the **reusable approach**, with this project as proof:
- ❌ "Survey application for community feedback"
- ✅ "Intelligent survey platform that dynamically adapts based on response quality—deployed here for community research"

---

## Missing Context Extrapolation

When input lacks business context (e.g., only lists technologies without problem/solution):

### 1. Infer use case from tech stack patterns:

| Tech Stack Pattern | Likely Use Case |
|-------------------|----------------|
| Real-time (WebSocket) + Collaboration | Team coordination or data synchronization |
| File upload + Processing | Document management or media workflow |
| Authentication + Multi-tenancy | B2B SaaS platform for multiple organizations |
| Offline-first + Mobile | Field service or remote worker scenarios |
| Scheduled jobs + Automation | Workflow automation or data pipeline |

### 2. Still aim for abstraction despite uncertainty:

- Lead with the **capability category**, not the invented specific use case
- Example: Don't say "Project Management Platform"—say **"Real-Time Collaboration Platform"** (broader)

### 3. Extrapolate problem from solution:

| Solution Has... | Problem Was... |
|----------------|---------------|
| Real-time sync | Async delays causing coordination issues |
| Automation | Manual repetitive work |
| Offline-first | Connectivity-dependent workflows |
| Multi-criteria evaluation | Inconsistent or time-consuming manual assessment |

### 4. Use conservative, defensible extrapolations:

- Avoid hyper-specific invented scenarios
- Stick to patterns common across the tech stack's typical use cases
- Acknowledge uncertainty by using broader framing

---

## Results at a Glance Rules

This section needs **3 concrete, quantified metrics** that tell a story. Choose from these categories:

1. **Efficiency/reduction** — What got smaller, faster, or eliminated? (e.g., 75% Time Saved, 37% Fewer Incomplete Responses)
2. **Quality/improvement** — What got better, richer, or multiplied? (e.g., 2.4x More Usable Insights)
3. **Speed/time** — How fast was delivery, processing, or turnaround? (e.g., 1 Day Launch, 30min Per Pitch Pack)
4. **Scale/capacity** — How much more can you handle? (e.g., 3x Client Capacity, 500 Targeted Contacts)
5. **Scope/coverage** — How many components, integrations, or workflows? (e.g., 15+ AI Agents, 7 Platforms Integrated)
6. **Cost/ROI** — What was the financial impact? (e.g., 40% Cost Reduction, 10x ROI)

**Select 3 metrics that best represent the value delivered.** Prioritize variety — don't pick 3 from the same category.

---

## METRICS QUALITY GATE (CRITICAL)

### ❌ PROHIBITED: Features masquerading as metrics

**These describe HOW the system works, not the business outcome it delivered:**
- "AI-Powered" / "Automated" / "Real-Time" / "Offline" / "Cross-platform" / "Mobile-First" / "Cloud-Based"

### ❌ PROHIBITED: Vague comparisons without baseline

- "Faster" without saying vs. what or by how much
- "Better quality" without quantification
- "Improved" without metrics

### ❌ PROHIBITED: Technology attributes

- "React Native" / "WebSocket Enabled" / "Containerized" / "Microservices Architecture"
- These are implementation details, not results

### ✅ REQUIRED: Outcome-based metrics with clear before/after

- "85% Time Saved" → clear improvement measurement
- "3x Client Capacity" → clear scale increase
- "30 minutes" → clear speed benchmark (if context shows this is faster than before)
- "37% Fewer [Bad Thing]" → clear quality improvement

### Metrics Baseline Rule

**Every metric must imply or state a "before" condition:**
- "85% Time Saved" implies "before: took X hours, after: takes 15% of X"
- "3x Capacity" implies "before: handled Y clients, after: handles 3Y clients"
- "30 minutes" alone is weak—better: "30min (down from 4-6 hours)"

### Input-Based Metric Strategy:

- **If input provides explicit metrics:** USE THEM EXACTLY
- **If input does NOT provide metrics:** Extrapolate reasonable estimates based on:
  - The before/after state implied by the technical description
  - Industry-standard improvements for this type of solution (be conservative)
  - The complexity and scope of the build
  - **Ensure extrapolated metrics pass the Quality Gate above**

### Metric Format:

```
{value} | {outcome_label}
```

- **Value:** Number/percentage on top (bold, large)
- **Label:** Short description (2-5 words) of the **outcome**, not the feature

### Examples That PASS the Quality Gate:

| Value | Label | Why It Passes ✅ |
|-------|-------|----------------|
| 37% | Fewer Incomplete Responses | Outcome: less bad data |
| 2.4x | More Usable Insights | Outcome: increased value |
| 85% | Time Saved | Outcome: efficiency gain with clear baseline |
| 30min | Per Pitch Pack (down from 4-6hr) | Outcome: speed improvement with baseline |
| 3x | Client Capacity | Outcome: scale increase |
| 500 | Targeted Contacts | Outcome: scope delivered |
| 65% | Job Completion Time Reduced | Outcome: efficiency with explicit baseline |
| Zero | Connectivity-Related Delays | Outcome: problem eliminated |

### Examples That FAIL the Quality Gate:

| Value | Label | Why It Fails ❌ |
|-------|-------|----------------|
| Real-time | Data Synchronization | Feature, not outcome |
| 100% | Offline Functionality | Feature, not outcome |
| Cross-platform | iOS + Android | Technology, not outcome |
| AI-Powered | Analysis | Feature, not outcome |
| Faster | Job Completion | Vague, no quantification |
| Automated | Research | Feature, not outcome |

**When in doubt:** Ask "What business outcome did this deliver?" not "What feature does it have?"

---

## Strategic Approach Rules

The Strategic Approach section must capture the **thinking and philosophy** behind design decisions, **NOT implementation details**.

### ❌ Wrong (Implementation Details):

- "Single API call analyzes Q2, Q3, Q4 simultaneously for efficiency"
- "Session-based state management passes analysis to follow-up page"
- "React Native enables code sharing between iOS and Android"

### ✅ Right (Strategic Philosophy):

- "Optimize for the analysis layer — Survey design assumes AI theme extraction, not Excel pivot tables"
- "Conversational not transactional — Dynamic follow-ups create dialogue; respondents feel heard rather than processed"
- "Cross-platform over native development — Shared codebase reduces maintenance burden while preserving native performance"

### Strategic Approach Checklist:

1. Does this explain **WHY** we made this choice, not **HOW** we implemented it?
2. Could another team apply this principle to a different project?
3. Does it reveal a tradeoff or design philosophy?

**Ask yourself:** "What was the strategic bet or insight that drove this design choice?" — not "How was it implemented?"

---

## Extrapolation Rules

If the input is missing any of the following, **extrapolate from the content provided** — do not ask for further input:

- **Problem context** — Infer the pain point from what the solution does (e.g., if it automates follow-ups, the problem was static surveys that miss nuance)
- **Strategic insight** — Infer the philosophy from the architecture choices (e.g., if it uses open-ended questions + AI analysis, the insight is "depth over breadth")
- **Results metrics** — Estimate reasonable outcomes based on the solution's capabilities and industry benchmarks (but ensure they pass Metrics Quality Gate)

**Be confident in extrapolations.** Frame estimates as results, not guesses.

### When extrapolating, prefer:

- Conservative estimates over aggressive claims
- Range-based improvements (e.g., "4-6 hours → 30 minutes") when baseline is uncertain
- Qualitative outcomes when quantitative metrics can't be defensibly extrapolated

---

## Tone Guidelines

- **Confident, not salesy**
- Focus on business outcomes and strategic insights
- **"The Learning" callouts should be reusable principles**, not project-specific observations
- **Bullets should be scannable with bold lead-ins**

---

## Solution Type Classification

Determine if this case study is:

- **"GTM Automation"** if it's for B2B software sales/marketing teams (outreach, prospecting, lead gen, sales enablement)
- **"Consulting Transformation"** if it's for strategy consulting firms (internal operations, client delivery, research automation)

---

## JSON Output Structure

Generate a JSON object with this structure:

```json
{
  "solution_type": "GTM Automation" or "Consulting Transformation",
  "header_tags": "Industry | Project Type",
  "title": "Client Type: Descriptive Name (USE ABSTRACTION RULES)",
  "one_line_hook": "Single sentence hook",
  "client": "Client name or type",
  "industry": "Industry name",
  "project_type": "Type of project",
  "technologies": "Comma-separated (use translation rules)",
  "results_at_glance": [
    {"value": "XX%", "label": "Short Label (MUST be outcome, not feature)"},
    {"value": "Xx", "label": "Short Label (MUST be outcome, not feature)"},
    {"value": "X weeks", "label": "Short Label (MUST be outcome, not feature)"}
  ],
  "challenge_bullets": [
    "Challenge point 1",
    "Challenge point 2",
    "Challenge point 3"
  ],
  "challenge_learning": "The Learning: Strategic insight",
  "deliverables": [
    "Deliverable 1",
    "Deliverable 2",
    "Deliverable 3",
    "Deliverable 4"
  ],
  "strategic_approach": [
    "Strategic insight 1 (NOT implementation detail - explain WHY not HOW)",
    "Strategic insight 2 (NOT implementation detail)",
    "Strategic insight 3 (NOT implementation detail)",
    "Strategic insight 4 (NOT implementation detail)"
  ],
  "solution_learning": "The Learning: Strategic principle",
  "business_impact": {
    "efficiency_gains": [
      "Efficiency point 1",
      "Efficiency point 2",
      "Efficiency point 3",
      "Efficiency point 4"
    ],
    "system_performance": [
      "Performance point 1",
      "Performance point 2",
      "Performance point 3",
      "Performance point 4"
    ],
    "value_category": [
      "Value point 1 (rename this category based on project type)",
      "Value point 2",
      "Value point 3",
      "Value point 4"
    ],
    "strategic_benefits": [
      "Strategic point 1",
      "Strategic point 2",
      "Strategic point 3",
      "Strategic point 4"
    ]
  },
  "cta_headline": "CTA question (GTM: sales-focused | Consulting: workflow-focused)",
  "cta_description": "Learn how we can... (GTM: mention GTM/sales team | Consulting: mention business/workflow)"
}
```

### CTA Guidelines by Solution Type:

- **GTM Automation:** Focus on sales/GTM automation
  - "Ready to Transform Your Sales Intelligence?"
  - "Ready to Automate Your Research-to-Outreach Pipeline?"

- **Consulting Transformation:** Focus on consulting workflows
  - "Ready to Transform Your Research Workflow?"
  - "Ready to Automate Your Pitch Pack Creation?"

---

## Final Instructions

**CRITICAL:** Return ONLY valid JSON, no markdown code blocks, no explanations. Just the raw JSON object.

**Input:**
{description}

**JSON:**
