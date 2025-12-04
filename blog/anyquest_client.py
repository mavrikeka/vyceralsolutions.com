#!/usr/bin/env python3
"""
AnyQuest API Client for LLM Integration
Provides article categorization and case study generation

Usage:
    python3 anyquest_client.py categorize <article_file>
    echo "description" | python3 anyquest_client.py generate-case-study
"""

import os
import sys
import json
import uuid
import re
import requests
import websocket
from typing import List, Dict
from pathlib import Path
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
ANYQUEST_API_KEY = os.getenv('ANYQUEST_API_KEY')
ANYQUEST_API_URL = 'https://api.anyquest.ai/run'
WEBHOOK_RELAY_BASE = 'https://anyquest-webhook-relay-production-863f.up.railway.app'

# Valid article categories
VALID_CATEGORIES = [
    'ai-agents',
    'ai-philosophy',
    'gtm-strategy',
    'industry-research',
    'personal-journey',
    'practical-applications',
    'technical-analysis',
    'tools-platforms'
]


def extract_text_from_html(html: str) -> str:
    """
    Extract plain text from HTML content

    Args:
        html: HTML string

    Returns:
        Plain text content
    """
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text(separator=' ', strip=True)


def call_anyquest(prompt: str, timeout: int = 120) -> str:
    """
    Call AnyQuest API with a prompt and wait for response

    Args:
        prompt: The prompt to send to LLM
        timeout: Timeout in seconds (default 120)

    Returns:
        LLM response text

    Raises:
        Exception: If API call fails or times out
    """
    if not ANYQUEST_API_KEY:
        raise Exception("ANYQUEST_API_KEY not found in environment. Check .env file.")

    # Generate unique ID for this request
    unique_id = str(uuid.uuid4())

    # Submit prompt to AnyQuest
    webhook_url = f"{WEBHOOK_RELAY_BASE}/webhook/{unique_id}"

    files = {
        'Prompt': (None, prompt),
        'webhook': (None, webhook_url)
    }

    headers = {
        'x-api-key': ANYQUEST_API_KEY
    }

    try:
        response = requests.post(ANYQUEST_API_URL, files=files, headers=headers)
        response.raise_for_status()
        job_id = response.json()['jobId']

        print(f'[AnyQuest] Submitted prompt, Job ID: {job_id}', file=sys.stderr)

    except Exception as e:
        raise Exception(f"Failed to submit prompt to AnyQuest: {e}")

    # Wait for response via WebSocket
    ws_url = f"wss://anyquest-webhook-relay-production-863f.up.railway.app/ws?id={unique_id}"

    try:
        print('[AnyQuest] Waiting for LLM response...', file=sys.stderr)
        ws = websocket.create_connection(ws_url, timeout=timeout)

        try:
            message = ws.recv()
            response_data = json.loads(message)
            return response_data['content']
        finally:
            ws.close()

    except Exception as e:
        raise Exception(f"Failed to receive response from AnyQuest: {e}")


def categorize_article(article_html: str) -> str:
    """
    Auto-categorize a blog article based on content

    Args:
        article_html: Raw HTML from LinkedIn article

    Returns:
        Category slug (e.g., 'ai-agents', 'practical-applications')

    Raises:
        ValueError: If LLM returns invalid category
    """
    # Extract text from HTML
    text_content = extract_text_from_html(article_html)

    # Limit to first 2000 words to avoid token limits
    words = text_content.split()[:2000]
    text_sample = ' '.join(words)

    # Build categorization prompt
    prompt = f"""Analyze this blog article and categorize it into ONE of these 8 categories.

Categories:
1. ai-agents - AI Agents & Agentic Systems (building autonomous agents, multi-agent systems)
2. ai-philosophy - AI Philosophy & Future of Work (impact on society, workforce transformation)
3. gtm-strategy - Business & GTM Strategy (go-to-market, sales automation, B2B strategy)
4. industry-research - Industry Research & Insights (market trends, industry analysis)
5. personal-journey - Personal Journey & Entrepreneurship (founder stories, lessons learned)
6. practical-applications - Practical Applications & Use Cases (hands-on guides, real-world implementations)
7. technical-analysis - Technical Deep Dives & Analysis (architecture, technical details)
8. tools-platforms - GenAI Tools & Platforms (tool reviews, platform guides, Clay, MindStudio, Agent.ai)

Article content (first 2000 words):
{text_sample}

CRITICAL: Return ONLY the category slug (e.g., 'ai-agents'), nothing else. No explanations, no punctuation, just the slug.

Category:"""

    # Call LLM
    response = call_anyquest(prompt)

    # Clean up response
    category = response.strip().lower()

    # Remove any quotes or extra text
    category = re.sub(r'["\']', '', category)
    category = category.split()[0]  # Take first word only

    # Validate category
    if category not in VALID_CATEGORIES:
        raise ValueError(f"Invalid category returned: '{category}'. Must be one of: {', '.join(VALID_CATEGORIES)}")

    return category


def generate_case_study(description: str) -> Dict:
    """
    Generate case study content from brief description

    Args:
        description: Technical description of the application/project

    Returns:
        dict with structured case study data following Vyceral Solutions format

    Raises:
        ValueError: If response cannot be parsed as JSON
    """
    # Build generation prompt using the strategic case study format
    prompt = f"""You are writing a case study for Vyceral Solutions' website. Given a technical description of an application, generate a case study following this exact structure and tone.

Structure to follow:

Header tags — [Industry] | [Project Type] (e.g., "Leadership Development | Community Tool")
Title — "[Client Type]: [Descriptive Name of Capability]"
One-line hook — A single sentence explaining what the tool does and the key insight it demonstrates
Metadata table — Client, Industry, Project Type, Technologies
Results at a Glance — 3 key metrics/deliverables with short labels
The Challenge — 3 bullets describing the problem, ending with a "The Learning:" callout that captures the strategic insight
The Solution — Deliverables list (4 items) + Strategic Approach (4 items) + "The Learning:" callout
Measurable Business Impact — 4 quadrants (Efficiency Gains, System Performance, [Value Category], Strategic Benefits) with 4 bullets each
CTA section — Not needed in output

Technology translation rules:

If input mentions React, Next.js, Node, Express, or similar frameworks → translate to "Claude Code"
If input mentions Vercel, Heroku, AWS, or deployment platforms → translate to "Railway"
If input mentions LLM, language model, AI API, or similar → translate to "AnyQuest"
Never say "AnyQuest LLM" — just "AnyQuest"
Technologies line should typically be: "AnyQuest, Claude Code, Railway" unless other specific tools are mentioned

Abstraction rules:
Frame the case study around the generalizable capability, not the specific use case. The specific project is an example of the broader concept.
Ask yourself: "What is the reusable product or approach here?" — then lead with that.

Examples of abstraction:
- Too Narrow: "Community survey for T2V practitioners" → Abstracted: "AI-Enabled Intelligent Survey"
- Too Narrow: "Built for 5-10 responses" → Abstracted: "Built for contexts where qualitative depth matters more than statistical scale"
- Too Narrow: "Community pilots" → Abstracted: "Research contexts with constrained sample sizes"
- Too Narrow: "T2V community insights" → Abstracted: "Stakeholder feedback collection"

The title should name the capability, not the specific deployment:
❌ "GenAI-Native Community Survey Application"
✅ "AI-Enabled Intelligent Survey Platform"

The Challenge section should describe the general problem category, with the specific use case as one example:
❌ "Community pilots often get only 5-10 responses"
✅ "Many research contexts—executive feedback, community pilots, qualitative studies—involve small samples where traditional surveys fail"

The Solution section should position the reusable approach, with this project as proof:
❌ "Survey application for community feedback"
✅ "Intelligent survey platform that dynamically adapts based on response quality—deployed here for community research"

Results at a Glance rules:
This section needs 3 concrete, quantified metrics that tell a story. Choose from these categories:

1. Efficiency/reduction — What got smaller, faster, or eliminated? (e.g., 75% Time Saved, 37% Fewer Incomplete Responses)
2. Quality/improvement — What got better, richer, or multiplied? (e.g., 2.4x More Usable Insights)
3. Speed/time — How fast was delivery, processing, or turnaround? (e.g., 1 Day Launch, 30min Per Pitch Pack)
4. Scale/capacity — How much more can you handle? (e.g., 3x Client Capacity, 500 Targeted Contacts)
5. Scope/coverage — How many components, integrations, or workflows? (e.g., 15+ AI Agents, 7 Platforms Integrated)
6. Cost/ROI — What was the financial impact? (e.g., 40% Cost Reduction, 10x ROI)

Select 3 metrics that best represent the value delivered. Prioritize variety — don't pick 3 from the same category.

If the input does not include specific metrics, extrapolate reasonable estimates based on:
- The before/after state implied by the technical description
- Industry-standard improvements for this type of solution
- The complexity and scope of the build

Metrics should be formatted as:
- Number/percentage on top (bold, large)
- Short label below (2-5 words)

Examples of good metrics:
- 37% | Fewer Incomplete Responses
- 2.4x | More Usable Insights
- 1 Day | Launch Timeline
- 75% | Time Saved
- 3x | Client Capacity
- 15+ | AI Agents
- 7 | Platforms Integrated
- 500 | Targeted Contacts
- 30min | Per Pitch Pack

Avoid vague metrics like:
❌ "AI-Powered" / "Automated" / "Real-Time" (these are features, not results)
❌ "Conversational" / "Adaptive" / "Dynamic" (these are descriptions, not outcomes)

Strategic Approach rules:
The Strategic Approach section must capture the thinking and philosophy behind design decisions, NOT implementation details.

❌ Wrong: "Single API call analyzes Q2, Q3, Q4 simultaneously for efficiency"
✅ Right: "Optimize for the analysis layer — Survey design assumes AI theme extraction, not Excel pivot tables"
❌ Wrong: "Session-based state management passes analysis to follow-up page"
✅ Right: "Conversational not transactional — Dynamic follow-ups create dialogue; respondents feel heard rather than processed"

Ask yourself: "What was the strategic bet or insight that drove this design choice?" — not "How was it implemented?"

Extrapolation rules:
If the input is missing any of the following, extrapolate from the content provided — do not ask for further input:

- Problem context — Infer the pain point from what the solution does (e.g., if it automates follow-ups, the problem was static surveys that miss nuance)
- Strategic insight — Infer the philosophy from the architecture choices (e.g., if it uses open-ended questions + AI analysis, the insight is "depth over breadth")
- Results metrics — Estimate reasonable outcomes based on the solution's capabilities and industry benchmarks

Be confident in extrapolations. Frame estimates as results, not guesses.

Tone guidelines:

Confident, not salesy
Focus on business outcomes and strategic insights
"The Learning" callouts should be reusable principles, not project-specific observations
Bullets should be scannable with bold lead-ins

Input:
{description}

Solution Type Classification:
Determine if this case study is:
- "GTM Automation" if it's for B2B software sales/marketing teams (outreach, prospecting, lead gen, sales enablement)
- "Consulting Transformation" if it's for strategy consulting firms (internal operations, client delivery, research automation)

Generate a JSON object with this structure:
{{
  "solution_type": "GTM Automation" or "Consulting Transformation",
  "header_tags": "Industry | Project Type",
  "title": "Client Type: Descriptive Name",
  "one_line_hook": "Single sentence hook",
  "client": "Client name or type",
  "industry": "Industry name",
  "project_type": "Type of project",
  "technologies": "Comma-separated (use translation rules)",
  "results_at_glance": [
    {{"value": "XX%", "label": "Short Label"}},
    {{"value": "Xx", "label": "Short Label"}},
    {{"value": "X weeks", "label": "Short Label"}}
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
    "Strategic insight 1 (NOT implementation detail)",
    "Strategic insight 2",
    "Strategic insight 3",
    "Strategic insight 4"
  ],
  "solution_learning": "The Learning: Strategic principle",
  "business_impact": {{
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
      "Value point 1",
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
  }},
  "cta_headline": "CTA question (GTM: sales-focused | Consulting: workflow-focused)",
  "cta_description": "Learn how we can... (GTM: mention GTM/sales team | Consulting: mention business/workflow)"
}}

CTA Guidelines by Solution Type:
- GTM Automation: Focus on sales/GTM automation ("Ready to Transform Your Sales Intelligence?", "Ready to Automate Your Research-to-Outreach Pipeline?")
- Consulting Transformation: Focus on consulting workflows ("Ready to Transform Your Research Workflow?", "Ready to Automate Your Pitch Pack Creation?")

CRITICAL: Return ONLY valid JSON, no markdown code blocks, no explanations. Just the raw JSON object.

JSON:"""

    # Call LLM
    response = call_anyquest(prompt)

    # Try to parse JSON directly
    try:
        data = json.loads(response)
        return data
    except json.JSONDecodeError:
        # Try to extract JSON from markdown code block
        match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass

        # Try to extract any JSON-like structure
        match = re.search(r'\{.*\}', response, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass

        raise ValueError(f"Could not parse JSON response from LLM. Response: {response[:200]}...")


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    """Command-line interface"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 anyquest_client.py categorize <article_file>")
        print("  echo 'description' | python3 anyquest_client.py generate-case-study")
        sys.exit(1)

    command = sys.argv[1]

    try:
        if command == 'categorize':
            # Categorize article
            if len(sys.argv) < 3:
                print("Error: Please provide article file path", file=sys.stderr)
                sys.exit(1)

            article_path = sys.argv[2]

            # Read article file
            with open(article_path, 'r', encoding='utf-8') as f:
                article_html = f.read()

            # Categorize
            category = categorize_article(article_html)

            # Output only the category slug (for easy parsing in bash)
            print(category)

        elif command == 'generate-case-study':
            # Generate case study from description (read from stdin)
            description = sys.stdin.read().strip()

            if not description:
                print("Error: Please provide case study description via stdin", file=sys.stderr)
                sys.exit(1)

            # Generate
            data = generate_case_study(description)

            # Output JSON
            print(json.dumps(data, indent=2))

        else:
            print(f"Error: Unknown command: {command}", file=sys.stderr)
            print("Valid commands: categorize, generate-case-study", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
