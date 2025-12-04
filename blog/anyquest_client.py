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
        description: Brief case study description (2-3 paragraphs)

    Returns:
        dict with structured case study data:
        {
            'client_name': str,
            'industry': str,
            'badge': str,
            'tagline': str,
            'technologies': str,
            'challenge': str,
            'solution': str,
            'metrics': [{'value': str, 'description': str}, ...],
            'results': [{'title': str, 'description': str}, ...]
        }

    Raises:
        ValueError: If response cannot be parsed as JSON
    """
    # Build generation prompt
    prompt = f"""Based on this case study description, generate structured case study content.

Description:
{description}

Generate a JSON object with the following structure:
{{
  "client_name": "Client name or generic description (e.g., 'Healthcare Tech Company')",
  "industry": "Primary industry (e.g., 'Manufacturing', 'Healthcare', 'Professional Services')",
  "badge": "Category badge (e.g., 'B2B SaaS', 'Industrial IoT', 'Executive Recruiting')",
  "tagline": "One-line description (5-8 words, e.g., 'CES-Targeted Manufacturing Campaign')",
  "technologies": "Comma-separated tech stack (e.g., 'Clay, Agent.ai, MindStudio')",
  "challenge": "2-3 sentence challenge description explaining the core problem",
  "solution": "2-3 sentence solution description explaining the approach and outcome",
  "metrics": [
    {{"value": "75%", "description": "Time Saved"}},
    {{"value": "3x", "description": "Faster Processing"}},
    {{"value": "2 weeks", "description": "Implementation Time"}}
  ],
  "results": [
    {{"title": "Efficiency Gains", "description": "2-3 sentence detailed description of this specific result"}},
    {{"title": "Quality Improvement", "description": "2-3 sentence detailed description"}},
    {{"title": "Strategic Impact", "description": "2-3 sentence detailed description"}},
    {{"title": "Scalability", "description": "2-3 sentence detailed description"}}
  ]
}}

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
