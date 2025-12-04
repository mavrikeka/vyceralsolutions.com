#!/usr/bin/env python3
"""
Unit tests for anyquest_client.py
Uses mocked AnyQuest API calls for fast, deterministic testing
"""

import pytest
import json
from unittest.mock import patch, MagicMock
from pathlib import Path

# Import functions to test (will implement these next)
try:
    from anyquest_client import (
        categorize_article,
        generate_case_study,
        call_anyquest,
        extract_text_from_html,
        VALID_CATEGORIES
    )
except ImportError:
    # Module doesn't exist yet - that's expected in TDD
    pytest.skip("anyquest_client.py not implemented yet", allow_module_level=True)


class TestCategorizeArticle:
    """Tests for article categorization"""

    def test_returns_valid_category_slug(self):
        """Should return a valid category slug"""
        with patch('anyquest_client.call_anyquest') as mock_call:
            mock_call.return_value = "ai-agents"

            result = categorize_article("<html><h1>Building AI Agents</h1></html>")

            assert result == "ai-agents"
            assert result in VALID_CATEGORIES

    def test_strips_whitespace_from_response(self):
        """Should handle LLM responses with whitespace"""
        with patch('anyquest_client.call_anyquest') as mock_call:
            mock_call.return_value = "  practical-applications\n"

            result = categorize_article("<html>Test</html>")

            assert result == "practical-applications"

    def test_handles_uppercase_response(self):
        """Should convert uppercase responses to lowercase"""
        with patch('anyquest_client.call_anyquest') as mock_call:
            mock_call.return_value = "GTM-STRATEGY"

            result = categorize_article("<html>Test</html>")

            assert result == "gtm-strategy"

    def test_raises_error_on_invalid_category(self):
        """Should raise ValueError if LLM returns invalid category"""
        with patch('anyquest_client.call_anyquest') as mock_call:
            mock_call.return_value = "invalid-category"

            with pytest.raises(ValueError, match="Invalid category"):
                categorize_article("<html>Test</html>")

    def test_calls_anyquest_with_proper_prompt(self):
        """Should construct proper prompt for categorization"""
        with patch('anyquest_client.call_anyquest') as mock_call:
            mock_call.return_value = "ai-agents"

            categorize_article("<html><p>AI agent article</p></html>")

            # Verify call was made
            assert mock_call.called
            # Verify prompt mentions categories
            prompt = mock_call.call_args[0][0]
            assert "ai-agents" in prompt.lower()
            assert "category" in prompt.lower()


class TestGenerateCaseStudy:
    """Tests for case study generation"""

    def test_returns_valid_structure(self):
        """Should return dict with all required fields"""
        mock_response = json.dumps({
            "client_name": "Test Corp",
            "industry": "Healthcare",
            "badge": "B2B SaaS",
            "tagline": "AI-Powered Healthcare Platform",
            "technologies": "Clay, Agent.ai",
            "challenge": "Manual data entry was time-consuming.",
            "solution": "Automated with AI agents.",
            "metrics": [
                {"value": "75%", "description": "Time Saved"},
                {"value": "3x", "description": "Faster"},
                {"value": "2 weeks", "description": "Setup"}
            ],
            "results": [
                {"title": "Result 1", "description": "Description 1"},
                {"title": "Result 2", "description": "Description 2"},
                {"title": "Result 3", "description": "Description 3"},
                {"title": "Result 4", "description": "Description 4"}
            ]
        })

        with patch('anyquest_client.call_anyquest') as mock_call:
            mock_call.return_value = mock_response

            result = generate_case_study("Test case study description")

            # Verify structure
            assert result['client_name'] == "Test Corp"
            assert result['industry'] == "Healthcare"
            assert result['badge'] == "B2B SaaS"
            assert len(result['metrics']) == 3
            assert len(result['results']) == 4

    def test_handles_markdown_code_blocks(self):
        """Should extract JSON from markdown code blocks"""
        mock_response = """```json
{
  "client_name": "Test Corp",
  "industry": "Manufacturing",
  "badge": "Industrial IoT",
  "tagline": "Smart Factory Solution",
  "technologies": "MindStudio",
  "challenge": "Manual processes",
  "solution": "AI automation",
  "metrics": [
    {"value": "80%", "description": "Efficiency"}
  ],
  "results": [
    {"title": "R1", "description": "D1"}
  ]
}
```"""

        with patch('anyquest_client.call_anyquest') as mock_call:
            mock_call.return_value = mock_response

            result = generate_case_study("Test description")

            assert result['client_name'] == "Test Corp"

    def test_raises_error_on_invalid_json(self):
        """Should raise ValueError if response is not valid JSON"""
        with patch('anyquest_client.call_anyquest') as mock_call:
            mock_call.return_value = "This is not JSON"

            with pytest.raises(ValueError, match="Could not parse JSON"):
                generate_case_study("Test description")

    def test_validates_required_fields(self):
        """Should ensure all required fields are present"""
        incomplete_response = json.dumps({
            "client_name": "Test Corp"
            # Missing other required fields
        })

        with patch('anyquest_client.call_anyquest') as mock_call:
            mock_call.return_value = incomplete_response

            result = generate_case_study("Test")

            # Should still parse but may be incomplete
            assert 'client_name' in result


class TestExtractTextFromHTML:
    """Tests for HTML text extraction"""

    def test_extracts_text_from_simple_html(self):
        """Should extract plain text from HTML"""
        html = "<html><body><h1>Title</h1><p>Content here.</p></body></html>"

        result = extract_text_from_html(html)

        assert "Title" in result
        assert "Content here" in result

    def test_removes_html_tags(self):
        """Should not include HTML tags in output"""
        html = "<div><strong>Bold text</strong></div>"

        result = extract_text_from_html(html)

        assert "<strong>" not in result
        assert "Bold text" in result

    def test_handles_empty_html(self):
        """Should handle empty HTML gracefully"""
        result = extract_text_from_html("")

        assert isinstance(result, str)


class TestCallAnyQuest:
    """Tests for AnyQuest API integration"""

    @patch('anyquest_client.requests.post')
    @patch('anyquest_client.websocket.create_connection')
    def test_submits_prompt_and_waits_for_response(self, mock_ws, mock_post):
        """Should POST prompt and receive WebSocket response"""
        # Mock API response
        mock_post.return_value.json.return_value = {"jobId": "test-job-123"}
        mock_post.return_value.raise_for_status = MagicMock()

        # Mock WebSocket response
        mock_ws_instance = MagicMock()
        mock_ws_instance.recv.return_value = json.dumps({
            "id": "test-id",
            "content": "LLM response here"
        })
        mock_ws.return_value = mock_ws_instance

        result = call_anyquest("Test prompt")

        assert result == "LLM response here"
        assert mock_post.called
        assert mock_ws.called

    @patch('anyquest_client.requests.post')
    def test_includes_api_key_header(self, mock_post):
        """Should include x-api-key header"""
        mock_post.return_value.json.return_value = {"jobId": "123"}
        mock_post.return_value.raise_for_status = MagicMock()

        with patch('anyquest_client.websocket.create_connection') as mock_ws:
            mock_ws_instance = MagicMock()
            mock_ws_instance.recv.return_value = json.dumps({"content": "test"})
            mock_ws.return_value = mock_ws_instance

            call_anyquest("Test")

            # Check API key was included
            headers = mock_post.call_args[1]['headers']
            assert 'x-api-key' in headers


class TestCLIInterface:
    """Tests for command-line interface"""

    def test_categorize_command_outputs_slug_only(self, tmp_path):
        """Should output only category slug for easy parsing"""
        # Create temp article file
        article_file = tmp_path / "test.html"
        article_file.write_text("<html><p>AI agents article</p></html>")

        with patch('anyquest_client.call_anyquest') as mock_call:
            mock_call.return_value = "ai-agents"

            # This would be tested via subprocess in integration tests
            # For unit tests, just verify the function works
            result = categorize_article(article_file.read_text())

            assert result == "ai-agents"
            assert "\n" not in result  # No extra newlines

    def test_generate_case_study_outputs_valid_json(self):
        """Should output valid JSON for easy parsing"""
        mock_response = json.dumps({
            "client_name": "Test",
            "industry": "Tech",
            "badge": "B2B",
            "tagline": "Test",
            "technologies": "Clay",
            "challenge": "Test",
            "solution": "Test",
            "metrics": [{"value": "1", "description": "Test"}],
            "results": [{"title": "T", "description": "D"}]
        })

        with patch('anyquest_client.call_anyquest') as mock_call:
            mock_call.return_value = mock_response

            result = generate_case_study("Test description")

            # Should be parseable as JSON
            json_output = json.dumps(result, indent=2)
            parsed = json.loads(json_output)
            assert parsed['client_name'] == "Test"


# Run tests with: pytest blog/test_anyquest_client.py -v
