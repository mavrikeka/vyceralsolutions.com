# Direct AnyQuest API Integration Guide
## Calling the Generic Prompt Agent Without AgentRelay

This guide shows how to call the AnyQuest API directly for the specific use case of executing prompts (like summarizing app ideas and feedback) without using the AgentRelay middleware.

---

## Overview

**Use this approach when:**
- You have a backend application (Node.js, Python, etc.)
- You can safely store the API key in environment variables
- You want the simplest possible integration
- You only need the generic prompt functionality

**Skip AgentRelay because:**
- It's just acting as a pass-through proxy
- You can call AnyQuest API directly with the same result
- Fewer moving parts = simpler architecture

---

## ⚠️ Important: Use axios, NOT fetch

When integrating with AnyQuest from Node.js server-side code:

✅ **DO**: Use `axios` with the `form-data` package
❌ **DON'T**: Use native `fetch` API with `form-data`

The native `fetch` API in Node.js doesn't properly serialize FormData from the `form-data` package, causing the AnyQuest API to return 500 errors. Always use `axios` for FormData submissions to AnyQuest.

See the [Error Handling](#error-handling) section for details.

---

## API Details

### Endpoint
```
POST https://api.anyquest.ai/run
```

### Authentication
Use the API key from the generic-prompt-agent configuration:
```
Header: x-api-key: API KEY
```

**IMPORTANT**: Store this in environment variables, never hard-code it!

### Request Format
**Content-Type**: `multipart/form-data`

**Required Fields**:
| Field | Type | Description |
|-------|------|-------------|
| `Prompt` | string | Your prompt text (case-sensitive!) |
| `webhook` | string | Webhook URL for receiving the response |


### Response Format
```json
{
  "jobId": "703afa55-c1e5-43de-9959-28d266cb9821"
}
```

The actual LLM response will be sent to your webhook URL asynchronously.

---

## Webhook Response Mechanism

### How It Works
1. You submit your prompt with a unique webhook URL
2. AnyQuest processes the prompt asynchronously
3. When complete, AnyQuest POSTs the result to your webhook URL
4. You receive the response via WebSocket (using the webhook relay service)

### Webhook URL Pattern
```
https://anyquest-webhook-relay-production-863f.up.railway.app/webhook/{YOUR_UNIQUE_ID}
```

Replace `{YOUR_UNIQUE_ID}` with a unique identifier for each request (UUID recommended).

### WebSocket Connection
To receive the response, connect to:
```
wss://anyquest-webhook-relay-production-863f.up.railway.app/ws?id={YOUR_UNIQUE_ID}
```

Use the same unique ID from your webhook URL.

### Response Message Format
```json
{
  "id": "your-unique-id",
  "content": "The LLM-generated response text..."
}
```

---

## Implementation Examples

### Example 1: Node.js/Express (Recommended)

```javascript
const axios = require('axios');
const FormData = require('form-data');
const WebSocket = require('ws');
const { randomUUID } = require('crypto');

// Store in environment variable!
const ANYQUEST_API_KEY = process.env.ANYQUEST_API_KEY || '84c0d5a342fc4a6880b4877384e5e3ae';
const ANYQUEST_API_URL = 'https://api.anyquest.ai/run';
const WEBHOOK_RELAY_BASE = 'https://anyquest-webhook-relay-production-863f.up.railway.app';

/**
 * Generate LLM summary for app ideas and feedback
 * @param {string[]} appIdeas - Array of app idea descriptions
 * @param {string[]} feedback - Array of user feedback
 * @returns {Promise<string>} - LLM-generated summary
 */
async function generateSummary(appIdeas, feedback) {
  // Step 1: Create unique ID for this request
  const uniqueId = randomUUID();

  // Step 2: Construct your prompt
  const prompt = buildPrompt(appIdeas, feedback);

  // Step 3: Submit to AnyQuest API
  const jobId = await submitPrompt(prompt, uniqueId);
  console.log('Submitted to AnyQuest, Job ID:', jobId);

  // Step 4: Wait for response via WebSocket
  const response = await waitForResponse(uniqueId);

  return response;
}

/**
 * Build the prompt from app ideas and feedback
 */
function buildPrompt(appIdeas, feedback) {
  const ideasText = appIdeas
    .map((idea, i) => `${i + 1}. ${idea}`)
    .join('\n');

  const feedbackText = feedback
    .map((fb, i) => `- ${fb}`)
    .join('\n');

  return `
Please analyze and summarize the following app ideas and user feedback.
Provide a concise summary highlighting key themes, overall sentiment, and actionable insights.

App Ideas:
${ideasText}

User Feedback:
${feedbackText}

Summary:
  `.trim();
}

/**
 * Submit prompt to AnyQuest API
 */
async function submitPrompt(prompt, uniqueId) {
  const formData = new FormData();
  formData.append('Prompt', prompt);
  formData.append('webhook', `${WEBHOOK_RELAY_BASE}/webhook/${uniqueId}`);

  const response = await axios.post(ANYQUEST_API_URL, formData, {
    headers: {
      'x-api-key': ANYQUEST_API_KEY,
      ...formData.getHeaders()
    }
  });

  return response.data.jobId;
}

/**
 * Wait for response via WebSocket
 */
function waitForResponse(uniqueId, timeoutMs = 120000) {
  return new Promise((resolve, reject) => {
    const wsUrl = `wss://anyquest-webhook-relay-production-863f.up.railway.app/ws?id=${uniqueId}`;
    const ws = new WebSocket(wsUrl);

    // Set timeout
    const timeout = setTimeout(() => {
      ws.close();
      reject(new Error('Response timeout after ' + (timeoutMs / 1000) + ' seconds'));
    }, timeoutMs);

    ws.on('open', () => {
      console.log('WebSocket connected, waiting for response...');
    });

    ws.on('message', (data) => {
      clearTimeout(timeout);
      const response = JSON.parse(data);
      ws.close();
      resolve(response.content);
    });

    ws.on('error', (error) => {
      clearTimeout(timeout);
      reject(new Error('WebSocket error: ' + error.message));
    });
  });
}

// ----- USAGE EXAMPLE -----

async function main() {
  const appIdeas = [
    "AI-powered task manager with natural language input",
    "Social media analytics dashboard for small businesses",
    "Collaborative code editor with real-time pair programming",
    "Fitness app with personalized workout recommendations"
  ];

  const feedback = [
    "Love the AI task manager idea! Would definitely use it.",
    "Analytics dashboard seems useful but crowded market",
    "Not sure there's demand for another code editor",
    "Fitness app sounds interesting if it's different from existing ones",
    "The task manager could be a winner if execution is good"
  ];

  try {
    console.log('Generating summary...');
    const summary = await generateSummary(appIdeas, feedback);

    console.log('\n=== SUMMARY ===');
    console.log(summary);
    console.log('===============\n');

  } catch (error) {
    console.error('Error generating summary:', error.message);
  }
}

// Run if executed directly
if (require.main === module) {
  main();
}

module.exports = { generateSummary, buildPrompt, submitPrompt, waitForResponse };
```

### Example 2: Express API Endpoint

Add this to your Express app to create an API endpoint:

```javascript
const express = require('express');
const { generateSummary } = require('./anyquest-client'); // From Example 1

const app = express();
app.use(express.json());

/**
 * POST /api/generate-summary
 * Body: { "appIdeas": [...], "feedback": [...] }
 */
app.post('/api/generate-summary', async (req, res) => {
  try {
    const { appIdeas, feedback } = req.body;

    // Validate input
    if (!Array.isArray(appIdeas) || !Array.isArray(feedback)) {
      return res.status(400).json({
        error: 'Invalid input: appIdeas and feedback must be arrays'
      });
    }

    // Generate summary
    const summary = await generateSummary(appIdeas, feedback);

    res.json({
      success: true,
      summary: summary
    });

  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

app.listen(3001, () => {
  console.log('Server running on http://localhost:3001');
});
```

**Usage:**
```bash
curl -X POST http://localhost:3001/api/generate-summary \
  -H "Content-Type: application/json" \
  -d '{
    "appIdeas": ["AI task manager", "Analytics dashboard"],
    "feedback": ["Love it!", "Interesting idea"]
  }'
```

### Example 3: Python Implementation

```python
import os
import requests
import json
import uuid
import websocket
from typing import List

# Store in environment variable!
ANYQUEST_API_KEY = os.getenv('ANYQUEST_API_KEY', '84c0d5a342fc4a6880b4877384e5e3ae')
ANYQUEST_API_URL = 'https://api.anyquest.ai/run'
WEBHOOK_RELAY_BASE = 'https://anyquest-webhook-relay-production-863f.up.railway.app'

def generate_summary(app_ideas: List[str], feedback: List[str]) -> str:
    """
    Generate LLM summary for app ideas and feedback

    Args:
        app_ideas: List of app idea descriptions
        feedback: List of user feedback

    Returns:
        LLM-generated summary text
    """
    # Create unique ID for this request
    unique_id = str(uuid.uuid4())

    # Build prompt
    prompt = build_prompt(app_ideas, feedback)

    # Submit to AnyQuest
    job_id = submit_prompt(prompt, unique_id)
    print(f'Submitted to AnyQuest, Job ID: {job_id}')

    # Wait for response
    response = wait_for_response(unique_id)

    return response

def build_prompt(app_ideas: List[str], feedback: List[str]) -> str:
    """Build the prompt from app ideas and feedback"""
    ideas_text = '\n'.join([f"{i+1}. {idea}" for i, idea in enumerate(app_ideas)])
    feedback_text = '\n'.join([f"- {fb}" for fb in feedback])

    return f"""
Please analyze and summarize the following app ideas and user feedback.
Provide a concise summary highlighting key themes, overall sentiment, and actionable insights.

App Ideas:
{ideas_text}

User Feedback:
{feedback_text}

Summary:
    """.strip()

def submit_prompt(prompt: str, unique_id: str) -> str:
    """Submit prompt to AnyQuest API"""
    webhook_url = f"{WEBHOOK_RELAY_BASE}/webhook/{unique_id}"

    files = {
        'Prompt': (None, prompt),
        'webhook': (None, webhook_url)
    }

    headers = {
        'x-api-key': ANYQUEST_API_KEY
    }

    response = requests.post(ANYQUEST_API_URL, files=files, headers=headers)
    response.raise_for_status()

    return response.json()['jobId']

def wait_for_response(unique_id: str, timeout: int = 120) -> str:
    """Wait for response via WebSocket"""
    ws_url = f"wss://anyquest-webhook-relay-production-863f.up.railway.app/ws?id={unique_id}"

    print('WebSocket connected, waiting for response...')
    ws = websocket.create_connection(ws_url, timeout=timeout)

    try:
        message = ws.recv()
        response_data = json.loads(message)
        return response_data['content']
    finally:
        ws.close()

# ----- USAGE EXAMPLE -----

if __name__ == '__main__':
    app_ideas = [
        "AI-powered task manager with natural language input",
        "Social media analytics dashboard for small businesses",
        "Collaborative code editor with real-time pair programming",
        "Fitness app with personalized workout recommendations"
    ]

    feedback = [
        "Love the AI task manager idea! Would definitely use it.",
        "Analytics dashboard seems useful but crowded market",
        "Not sure there's demand for another code editor",
        "Fitness app sounds interesting if it's different from existing ones",
        "The task manager could be a winner if execution is good"
    ]

    try:
        print('Generating summary...')
        summary = generate_summary(app_ideas, feedback)

        print('\n=== SUMMARY ===')
        print(summary)
        print('===============\n')

    except Exception as e:
        print(f'Error generating summary: {e}')
```

**Install dependencies:**
```bash
pip install requests websocket-client
```

### Example 4: Simple curl Test

```bash
#!/bin/bash

# Generate unique ID
UNIQUE_ID=$(uuidgen | tr '[:upper:]' '[:lower:]')

# Submit prompt
RESPONSE=$(curl -X POST https://api.anyquest.ai/run \
  -H "x-api-key: 84c0d5a342fc4a6880b4877384e5e3ae" \
  -F "Prompt=Summarize these app ideas: 1) AI task manager 2) Analytics dashboard. Feedback: Both look promising!" \
  -F "webhook=https://anyquest-webhook-relay-production-863f.up.railway.app/webhook/${UNIQUE_ID}" \
  --silent)

echo "API Response: $RESPONSE"
echo "Webhook ID: $UNIQUE_ID"
echo ""
echo "Connect to WebSocket to receive response:"
echo "wss://anyquest-webhook-relay-production-863f.up.railway.app/ws?id=${UNIQUE_ID}"
```

---

## Environment Configuration

### Required Environment Variables

**For Node.js (.env file):**
```env
ANYQUEST_API_KEY=84c0d5a342fc4a6880b4877384e5e3ae
```

**For Python (.env file):**
```env
ANYQUEST_API_KEY=84c0d5a342fc4a6880b4877384e5e3ae
```

### Security Best Practices
1. **Never commit API keys** to version control
2. Add `.env` to `.gitignore`
3. Use environment variables in production
4. Rotate API keys periodically
5. Only call from backend/server-side code (never expose in frontend)

---

## Error Handling

### Common Errors

**1. Invalid API Key**
```json
{
  "error": "Unauthorized",
  "status": 401
}
```
**Solution**: Verify your API key is correct

**2. Missing Required Field**
```json
{
  "error": "Bad Request",
  "message": "Missing required field: Prompt"
}
```
**Solution**: Ensure `Prompt` field is included (case-sensitive!)

**3. WebSocket Timeout**
```
Error: Response timeout after 120 seconds
```
**Solution**:
- Increase timeout for complex prompts
- Check AnyQuest API status
- Verify webhook relay service is accessible

**4. Network Error**
```
Error: connect ECONNREFUSED
```
**Solution**:
- Check internet connection
- Verify AnyQuest API endpoint is correct
- Check firewall settings

**5. Internal Server Error (500) - FormData Issue**
```json
{
  "timestamp": "2025-12-03T03:36:01.770+00:00",
  "status": 500,
  "error": "Internal Server Error",
  "path": "/run"
}
```
**Solution**:

**IMPORTANT**: Do NOT use `fetch` with `form-data` in Node.js server-side code. Use `axios` instead!

The native `fetch` API doesn't properly handle `FormData` from the `form-data` package in Node.js, leading to 500 errors from AnyQuest.

❌ **Don't do this:**
```javascript
const response = await fetch(ANYQUEST_API_URL, {
  method: 'POST',
  headers: {
    'x-api-key': ANYQUEST_API_KEY,
  },
  body: formData,  // This won't work properly!
});
```

✅ **Do this instead:**
```javascript
const response = await axios.post(ANYQUEST_API_URL, formData, {
  headers: {
    'x-api-key': ANYQUEST_API_KEY,
    ...formData.getHeaders(),  // Critical for proper content-type
  },
});
```

### Robust Error Handling Example

```javascript
async function generateSummaryWithRetry(appIdeas, feedback, maxRetries = 2) {
  let lastError;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      console.log(`Attempt ${attempt}/${maxRetries}...`);
      const summary = await generateSummary(appIdeas, feedback);
      return summary;

    } catch (error) {
      lastError = error;
      console.error(`Attempt ${attempt} failed:`, error.message);

      // Wait before retry (exponential backoff)
      if (attempt < maxRetries) {
        const delay = Math.pow(2, attempt) * 1000; // 2s, 4s, etc.
        console.log(`Retrying in ${delay/1000} seconds...`);
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  }

  throw new Error(`Failed after ${maxRetries} attempts: ${lastError.message}`);
}
```

---

## Performance & Timing

### Expected Response Times
- **API Submission**: < 1 second
- **LLM Processing**: 10-60 seconds (depends on prompt complexity)
- **Total Time**: 10-60 seconds typically

### Timeout Recommendations
- **Short prompts**: 30-60 seconds
- **Complex analysis**: 60-120 seconds
- **Production**: 120 seconds (2 minutes) recommended

### Concurrent Requests
You can submit multiple requests in parallel:

```javascript
async function generateMultipleSummaries(datasets) {
  const promises = datasets.map(({ appIdeas, feedback }) =>
    generateSummary(appIdeas, feedback)
  );

  return await Promise.all(promises);
}
```

---

## Testing Your Integration

### Quick Test Checklist
- [ ] API key is stored in environment variable
- [ ] Can successfully POST to AnyQuest API
- [ ] Receive valid `jobId` in response
- [ ] Can establish WebSocket connection
- [ ] Receive response within timeout period
- [ ] Can parse and use the content

### Test Script

```javascript
// test.js
const { generateSummary } = require('./anyquest-client');

async function test() {
  console.log('Testing AnyQuest integration...\n');

  const testIdeas = ['Test idea 1', 'Test idea 2'];
  const testFeedback = ['Looks good', 'Interesting'];

  try {
    const summary = await generateSummary(testIdeas, testFeedback);
    console.log('✓ SUCCESS');
    console.log('Summary:', summary);
    process.exit(0);
  } catch (error) {
    console.log('✗ FAILED');
    console.error('Error:', error.message);
    process.exit(1);
  }
}

test();
```

Run: `node test.js`

---

## Comparison: Direct vs AgentRelay

| Aspect | Direct Integration | Via AgentRelay |
|--------|-------------------|----------------|
| **Complexity** | Lower | Higher |
| **Dependencies** | AnyQuest API only | AnyQuest + AgentRelay |
| **API Key Storage** | Your app | agents.json |
| **Network Hops** | 1 (to AnyQuest) | 2 (to AgentRelay, then AnyQuest) |
| **Flexibility** | Single agent | Multiple agents |
| **Best For** | Single app, one agent | Multiple apps, many agents |

---

## Next Steps

1. **Copy the Node.js or Python example** into your application
2. **Set up environment variable** with your API key
3. **Test with simple data** first
4. **Implement error handling** for production
5. **Add logging** for debugging
6. **Consider retry logic** for reliability

---

## Summary

To integrate directly with AnyQuest for prompt execution:

1. **Submit**: POST to `https://api.anyquest.ai/run` with `Prompt` and `webhook` fields
2. **Authenticate**: Include `x-api-key` header with your API key
3. **Generate unique ID**: Use UUID for each request
4. **Connect WebSocket**: To webhook relay with your unique ID
5. **Receive**: LLM response via WebSocket message
6. **Display**: Parse `content` field and show in your app

This approach is simpler, faster, and requires no AgentRelay dependency!
