"""
Test suite for JSON prompting examples.

This module contains comprehensive tests for all the JSON prompting examples
including validation, parsing, and edge cases.
"""

import json
import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any


class TestJSONValidation:
    """Test JSON schema validation and parsing."""

    def test_valid_json_parsing(self):
        """Test that valid JSON strings are parsed correctly."""
        json_str = '{"name": "John", "age": 30, "active": true}'
        result = json.loads(json_str)

        assert result["name"] == "John"
        assert result["age"] == 30
        assert result["active"] is True

    def test_invalid_json_raises_error(self):
        """Test that invalid JSON raises appropriate error."""
        invalid_json = '{"name": "John", age: 30}'  # Missing quotes

        with pytest.raises(json.JSONDecodeError):
            json.loads(invalid_json)

    def test_nested_json_structure(self):
        """Test parsing of nested JSON structures."""
        json_str = '''
        {
            "user": {
                "name": "Jane",
                "contact": {
                    "email": "jane@example.com",
                    "phone": "555-1234"
                }
            }
        }
        '''
        result = json.loads(json_str)

        assert result["user"]["name"] == "Jane"
        assert result["user"]["contact"]["email"] == "jane@example.com"

    def test_array_in_json(self):
        """Test parsing of arrays in JSON."""
        json_str = '{"tags": ["python", "ai", "json"], "count": 3}'
        result = json.loads(json_str)

        assert len(result["tags"]) == 3
        assert "python" in result["tags"]
        assert result["count"] == 3


class TestDataExtraction:
    """Test data extraction functionality."""

    @pytest.fixture
    def sample_invoice_data(self) -> Dict[str, Any]:
        """Provide sample invoice data for testing."""
        return {
            "invoice_number": "INV-2024-001",
            "invoice_date": "2024-01-15",
            "total": 1250.00,
            "currency": "USD",
            "line_items": [
                {
                    "description": "Service A",
                    "quantity": 1,
                    "unit_price": 1000.00,
                    "total": 1000.00
                },
                {
                    "description": "Service B",
                    "quantity": 5,
                    "unit_price": 50.00,
                    "total": 250.00
                }
            ]
        }

    def test_invoice_structure_validation(self, sample_invoice_data):
        """Test that invoice data has required fields."""
        required_fields = ["invoice_number", "invoice_date", "total", "line_items"]

        for field in required_fields:
            assert field in sample_invoice_data

    def test_invoice_line_items(self, sample_invoice_data):
        """Test invoice line items structure."""
        line_items = sample_invoice_data["line_items"]

        assert len(line_items) == 2
        assert all("description" in item for item in line_items)
        assert all("total" in item for item in line_items)

    def test_invoice_total_calculation(self, sample_invoice_data):
        """Test that invoice total matches line items sum."""
        line_items_total = sum(item["total"] for item in sample_invoice_data["line_items"])
        assert sample_invoice_data["total"] == line_items_total

    @pytest.fixture
    def sample_resume_data(self) -> Dict[str, Any]:
        """Provide sample resume data for testing."""
        return {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "skills": ["Python", "JavaScript", "React"],
            "experience": [
                {
                    "company": "Tech Corp",
                    "title": "Software Engineer",
                    "start_date": "2020-01",
                    "end_date": "Present"
                }
            ]
        }

    def test_resume_structure_validation(self, sample_resume_data):
        """Test that resume data has required fields."""
        required_fields = ["name", "email", "skills", "experience"]

        for field in required_fields:
            assert field in sample_resume_data

    def test_resume_experience_structure(self, sample_resume_data):
        """Test resume experience array structure."""
        experience = sample_resume_data["experience"]

        assert len(experience) > 0
        assert all("company" in exp for exp in experience)
        assert all("title" in exp for exp in experience)


class TestEmailSummarization:
    """Test email summarization functionality."""

    @pytest.fixture
    def sample_email_summary(self) -> Dict[str, Any]:
        """Provide sample email summary for testing."""
        return {
            "subject": "Project Update",
            "sender": "john@example.com",
            "key_points": [
                "Project is on schedule",
                "Budget approved",
                "Team expanded by 2 members"
            ],
            "action_items": [
                {
                    "task": "Review design mockups",
                    "owner": "Jane",
                    "deadline": "2024-01-20"
                }
            ],
            "urgency": "medium"
        }

    def test_email_summary_structure(self, sample_email_summary):
        """Test email summary has required fields."""
        required_fields = ["subject", "sender", "key_points", "action_items"]

        for field in required_fields:
            assert field in sample_email_summary

    def test_email_urgency_values(self, sample_email_summary):
        """Test that urgency is a valid value."""
        valid_urgencies = ["low", "medium", "high", "critical"]
        assert sample_email_summary["urgency"] in valid_urgencies

    def test_action_items_structure(self, sample_email_summary):
        """Test action items have required fields."""
        action_items = sample_email_summary["action_items"]

        assert len(action_items) > 0
        for item in action_items:
            assert "task" in item
            assert "owner" in item or item.get("owner") is None


class TestContentGeneration:
    """Test content generation functionality."""

    @pytest.fixture
    def sample_blog_post(self) -> Dict[str, Any]:
        """Provide sample blog post for testing."""
        return {
            "metadata": {
                "title": "Getting Started with JSON",
                "slug": "getting-started-json",
                "keywords": ["json", "tutorial", "programming"],
                "estimated_reading_time": "5 min"
            },
            "content": {
                "hook": "JSON is everywhere in modern web development...",
                "sections": [
                    {
                        "heading": "What is JSON?",
                        "content": "JSON stands for...",
                        "key_takeaway": "JSON is a data format"
                    }
                ],
                "conclusion": "Now you know the basics..."
            }
        }

    def test_blog_post_metadata(self, sample_blog_post):
        """Test blog post metadata structure."""
        metadata = sample_blog_post["metadata"]

        assert "title" in metadata
        assert "slug" in metadata
        assert "keywords" in metadata
        assert isinstance(metadata["keywords"], list)

    def test_blog_post_sections(self, sample_blog_post):
        """Test blog post sections structure."""
        sections = sample_blog_post["content"]["sections"]

        assert len(sections) > 0
        for section in sections:
            assert "heading" in section
            assert "content" in section

    def test_slug_format(self, sample_blog_post):
        """Test that slug is URL-friendly."""
        slug = sample_blog_post["metadata"]["slug"]

        assert " " not in slug
        assert slug.islower() or "-" in slug


class TestReasoningTasks:
    """Test reasoning tasks functionality."""

    @pytest.fixture
    def sample_math_solution(self) -> Dict[str, Any]:
        """Provide sample math solution for testing."""
        return {
            "problem": "If x + 5 = 10, what is x?",
            "problem_type": "algebra",
            "steps": [
                {
                    "step_number": 1,
                    "description": "Subtract 5 from both sides",
                    "calculation": "x + 5 - 5 = 10 - 5",
                    "result": "x = 5"
                }
            ],
            "final_answer": "5"
        }

    def test_math_solution_structure(self, sample_math_solution):
        """Test math solution has required fields."""
        required_fields = ["problem", "steps", "final_answer"]

        for field in required_fields:
            assert field in sample_math_solution

    def test_math_steps_order(self, sample_math_solution):
        """Test that math steps are in order."""
        steps = sample_math_solution["steps"]
        step_numbers = [step["step_number"] for step in steps]

        assert step_numbers == sorted(step_numbers)

    @pytest.fixture
    def sample_ethical_analysis(self) -> Dict[str, Any]:
        """Provide sample ethical analysis for testing."""
        return {
            "dilemma": "Should AI replace human jobs?",
            "stakeholders": [
                {
                    "name": "Workers",
                    "interests": ["Job security", "Income"]
                },
                {
                    "name": "Companies",
                    "interests": ["Efficiency", "Cost reduction"]
                }
            ],
            "ethical_frameworks": [
                {
                    "framework": "utilitarianism",
                    "analysis": "Consider greatest good...",
                    "recommended_action": "Gradual transition with retraining"
                }
            ]
        }

    def test_ethical_analysis_structure(self, sample_ethical_analysis):
        """Test ethical analysis has required fields."""
        required_fields = ["dilemma", "stakeholders", "ethical_frameworks"]

        for field in required_fields:
            assert field in sample_ethical_analysis

    def test_stakeholders_structure(self, sample_ethical_analysis):
        """Test stakeholders have required fields."""
        stakeholders = sample_ethical_analysis["stakeholders"]

        assert len(stakeholders) > 0
        for stakeholder in stakeholders:
            assert "name" in stakeholder
            assert "interests" in stakeholder


class TestAssemblyAIIntegration:
    """Test AssemblyAI integration functionality."""

    @pytest.fixture
    def sample_diarization_result(self) -> Dict[str, Any]:
        """Provide sample speaker diarization result."""
        return {
            "metadata": {
                "num_speakers_detected": 2,
                "total_words": 150
            },
            "speaker_segments": [
                {
                    "speaker": "A",
                    "text": "Hello, how are you?",
                    "start_time": 0,
                    "end_time": 2000,
                    "confidence": 0.95
                },
                {
                    "speaker": "B",
                    "text": "I'm doing well, thanks!",
                    "start_time": 2100,
                    "end_time": 4000,
                    "confidence": 0.92
                }
            ],
            "speaker_statistics": {
                "A": {
                    "total_duration_ms": 5000,
                    "num_segments": 3,
                    "speaking_time_percentage": 55.0
                },
                "B": {
                    "total_duration_ms": 4000,
                    "num_segments": 2,
                    "speaking_time_percentage": 45.0
                }
            }
        }

    def test_diarization_metadata(self, sample_diarization_result):
        """Test diarization metadata structure."""
        metadata = sample_diarization_result["metadata"]

        assert "num_speakers_detected" in metadata
        assert metadata["num_speakers_detected"] > 0

    def test_speaker_segments(self, sample_diarization_result):
        """Test speaker segments structure."""
        segments = sample_diarization_result["speaker_segments"]

        assert len(segments) > 0
        for segment in segments:
            assert "speaker" in segment
            assert "text" in segment
            assert "start_time" in segment
            assert "end_time" in segment

    def test_speaker_statistics(self, sample_diarization_result):
        """Test speaker statistics structure."""
        stats = sample_diarization_result["speaker_statistics"]

        assert len(stats) > 0
        for speaker, data in stats.items():
            assert "total_duration_ms" in data
            assert "num_segments" in data
            assert data["speaking_time_percentage"] >= 0
            assert data["speaking_time_percentage"] <= 100


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_json_object(self):
        """Test handling of empty JSON object."""
        json_str = '{}'
        result = json.loads(json_str)

        assert result == {}
        assert isinstance(result, dict)

    def test_null_values(self):
        """Test handling of null values in JSON."""
        json_str = '{"name": "John", "email": null, "age": 30}'
        result = json.loads(json_str)

        assert result["name"] == "John"
        assert result["email"] is None
        assert result["age"] == 30

    def test_empty_arrays(self):
        """Test handling of empty arrays."""
        json_str = '{"tags": [], "items": []}'
        result = json.loads(json_str)

        assert result["tags"] == []
        assert len(result["tags"]) == 0

    def test_unicode_characters(self):
        """Test handling of unicode characters."""
        json_str = '{"name": "José", "city": "São Paulo"}'
        result = json.loads(json_str)

        assert result["name"] == "José"
        assert result["city"] == "São Paulo"

    def test_large_numbers(self):
        """Test handling of large numbers."""
        json_str = '{"amount": 999999999999, "small": 0.0000001}'
        result = json.loads(json_str)

        assert result["amount"] == 999999999999
        assert result["small"] == 0.0000001

    def test_deeply_nested_structure(self):
        """Test handling of deeply nested structures."""
        json_str = '''
        {
            "level1": {
                "level2": {
                    "level3": {
                        "value": "deep"
                    }
                }
            }
        }
        '''
        result = json.loads(json_str)

        assert result["level1"]["level2"]["level3"]["value"] == "deep"


class TestMockAPIResponses:
    """Test with mocked API responses."""

    @patch('openai.OpenAI')
    def test_mock_openai_response(self, mock_client):
        """Test with mocked OpenAI response."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = '{"result": "success"}'

        mock_client.return_value.chat.completions.create.return_value = mock_response

        # Simulate API call
        response_text = mock_response.choices[0].message.content
        result = json.loads(response_text)

        assert result["result"] == "success"

    def test_mock_validation_success(self):
        """Test successful validation with mock data."""
        mock_data = {
            "name": "Test",
            "value": 100,
            "active": True
        }

        # Validate required fields
        required_fields = ["name", "value"]
        validation_passed = all(field in mock_data for field in required_fields)

        assert validation_passed is True

    def test_mock_validation_failure(self):
        """Test validation failure with mock data."""
        mock_data = {
            "name": "Test",
            # Missing required 'value' field
            "active": True
        }

        required_fields = ["name", "value"]
        validation_passed = all(field in mock_data for field in required_fields)

        assert validation_passed is False


# Pytest configuration
@pytest.fixture(autouse=True)
def reset_environment():
    """Reset environment before each test."""
    yield
    # Cleanup code here if needed


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
