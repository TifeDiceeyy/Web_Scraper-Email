#!/usr/bin/env python3
"""
Tests for email generation tools
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.generate_general_email import generate_general_email, parse_email_response
from tools.generate_specific_email import generate_specific_email


class TestEmailParsing:
    """Test email response parsing"""

    def test_parse_standard_format(self):
        """Test parsing standard SUBJECT: / BODY: format"""
        response = """SUBJECT: Test Subject

BODY:
This is the email body.
It has multiple lines.
"""
        subject, body = parse_email_response(response)
        assert subject == "Test Subject"
        assert "This is the email body" in body
        assert "multiple lines" in body

    def test_parse_fallback_format(self):
        """Test parsing when format is not perfect"""
        response = """Quick question about your business

Hi there, this is the body"""

        subject, body = parse_email_response(response)
        assert len(subject) > 0  # Should have some subject
        assert len(body) > 0  # Should have some body

    def test_parse_empty_response(self):
        """Test handling empty response"""
        response = ""

        subject, body = parse_email_response(response)
        # Should provide fallback
        assert len(subject) > 0
        assert len(body) > 0


class TestGeneralEmailGeneration:
    """Test general help email generation"""

    @patch('tools.generate_general_email.genai.Client')
    def test_generate_with_website_context(self, mock_client):
        """Test email generation with website context"""
        # Mock API response
        mock_response = Mock()
        mock_response.text = """SUBJECT: Quick question about Smile Dental

BODY:
Hi Smile Dental team,

I help dental practices with automation. What's your biggest operational challenge?

Best regards"""

        mock_client_instance = Mock()
        mock_client_instance.models.generate_content.return_value = mock_response
        mock_client.return_value = mock_client_instance

        # Test
        subject, body = generate_general_email(
            business_name="Smile Dental",
            business_type="Dentist",
            website_content="Family dentistry for 20 years"
        )

        assert "Smile Dental" in subject or "Smile Dental" in body
        assert len(subject) > 0
        assert len(body) > 0

    @patch('tools.generate_general_email.genai.Client')
    def test_generate_without_website(self, mock_client):
        """Test email generation without website context"""
        mock_response = Mock()
        mock_response.text = """SUBJECT: Question for you

BODY:
Hello!"""

        mock_client_instance = Mock()
        mock_client_instance.models.generate_content.return_value = mock_response
        mock_client.return_value = mock_client_instance

        subject, body = generate_general_email(
            business_name="Test Business",
            business_type="Restaurant"
        )

        assert len(subject) > 0
        assert len(body) > 0


class TestSpecificEmailGeneration:
    """Test specific automation email generation"""

    @patch('tools.generate_specific_email.genai.Client')
    def test_generate_with_automation_focus(self, mock_client):
        """Test email generation with specific automation"""
        mock_response = Mock()
        mock_response.text = """SUBJECT: Reduce no-shows by 30%

BODY:
Hi team,

Appointment reminders can reduce your no-shows significantly.

Interested in learning more?"""

        mock_client_instance = Mock()
        mock_client_instance.models.generate_content.return_value = mock_response
        mock_client.return_value = mock_client_instance

        subject, body = generate_specific_email(
            business_name="Smile Dental",
            business_type="Dentist",
            automation_focus="Appointment Reminders"
        )

        assert len(subject) > 0
        assert len(body) > 0
        # Should mention benefit or automation
        combined = (subject + body).lower()
        assert any(word in combined for word in ['reduce', 'appointment', 'reminder', 'no-show'])


class TestErrorHandling:
    """Test error handling in email generation"""

    def test_missing_api_key(self):
        """Test handling missing API key"""
        with patch.dict(os.environ, {'GEMINI_API_KEY': ''}, clear=True):
            with pytest.raises(ValueError, match="GEMINI_API_KEY"):
                generate_general_email("Test", "Dentist")

    @patch('tools.generate_general_email.genai.Client')
    def test_api_error_fallback(self, mock_client):
        """Test fallback email on API error"""
        # Mock API to raise error
        mock_client_instance = Mock()
        mock_client_instance.models.generate_content.side_effect = Exception("API Error")
        mock_client.return_value = mock_client_instance

        # Should return fallback instead of crashing
        subject, body = generate_general_email(
            business_name="Test Business",
            business_type="Restaurant"
        )

        assert len(subject) > 0
        assert len(body) > 0
        # Fallback should mention business name
        assert "Test Business" in subject or "Test Business" in body


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
