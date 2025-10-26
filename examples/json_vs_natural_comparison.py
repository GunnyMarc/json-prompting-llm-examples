"""
Module: examples/json_vs_natural_comparison.py
Description: Compare JSON prompting vs natural language prompting performance

This example demonstrates the differences in consistency, accuracy, and
usability between JSON-structured prompts and natural language prompts.

Usage:
    python examples/json_vs_natural_comparison.py

Requirements:
    - OPENAI_API_KEY in environment variables
    - Python 3.9+
"""

import os
import json
import time
from typing import Dict, List, Any
from dotenv import load_dotenv

try:
    from openai import OpenAI
except ImportError:
    print("OpenAI package not installed. Install with: pip install openai")
    exit(1)

load_dotenv()


class PromptingComparison:
    """Compare JSON vs Natural Language prompting approaches."""

    def __init__(self):
        """Initialize OpenAI client."""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")

    def classify_with_json(self, text: str) -> Dict[str, Any]:
        """
        Classify text using JSON-structured prompt.

        Args:
            text: Input text to classify

        Returns:
            Dictionary with classification results
        """
        schema = {
            "category": "string (one of: bug, feature, question, complaint)",
            "priority": "string (one of: low, medium, high, critical)",
            "sentiment": "string (one of: positive, negative, neutral)",
            "confidence": "number (0.0 to 1.0)"
        }

        prompt = f"""Classify the following customer feedback.

Input: "{text}"

Output format (JSON):
{json.dumps(schema, indent=2)}

Example:
{{
  "category": "bug",
  "priority": "high",
  "sentiment": "negative",
  "confidence": 0.92
}}

Return only valid JSON:"""

        start_time = time.time()
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        duration = time.time() - start_time

        result = json.loads(response.choices[0].message.content)
        result["processing_time"] = duration
        return result

    def classify_with_natural_language(self, text: str) -> str:
        """
        Classify text using natural language prompt.

        Args:
            text: Input text to classify

        Returns:
            String with classification results
        """
        prompt = f"""Please classify the following customer feedback.
Consider the category (bug, feature, question, or complaint),
priority level, sentiment, and your confidence level.

Feedback: "{text}"

Please provide your classification:"""

        start_time = time.time()
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        duration = time.time() - start_time

        return {
            "response": response.choices[0].message.content,
            "processing_time": duration
        }


def run_comparison():
    """Run comparison tests between JSON and natural language prompts."""
    print("=" * 80)
    print("JSON vs Natural Language Prompting Comparison")
    print("=" * 80)
    print()

    comparator = PromptingComparison()

    # Test cases
    test_cases = [
        "The app crashes every time I try to upload a photo. This is really frustrating!",
        "I would love to see a dark mode feature added to the app.",
        "How do I reset my password? Can't find the option anywhere.",
        "Your customer service is terrible! I've been waiting for 3 days!",
        "The new update is amazing! The UI is so much better now."
    ]

    for i, text in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print(f"Input: \"{text}\"")
        print("-" * 80)

        # JSON Prompting
        print("\n[JSON PROMPTING]")
        try:
            json_result = comparator.classify_with_json(text)
            print(json.dumps(json_result, indent=2))
            print(f"Parsing: ✓ Success")
            print(f"Time: {json_result['processing_time']:.2f}s")
        except Exception as e:
            print(f"Error: {e}")
            print(f"Parsing: ✗ Failed")

        # Natural Language Prompting
        print("\n[NATURAL LANGUAGE PROMPTING]")
        try:
            nl_result = comparator.classify_with_natural_language(text)
            print(nl_result["response"])
            print(f"Parsing: ? Manual parsing required")
            print(f"Time: {nl_result['processing_time']:.2f}s")
        except Exception as e:
            print(f"Error: {e}")

        print("-" * 80)


def run_consistency_test():
    """Test consistency across multiple runs."""
    print("\n" + "=" * 80)
    print("Consistency Test: Running same prompt 3 times")
    print("=" * 80)
    print()

    comparator = PromptingComparison()
    test_text = "The app is great but crashes sometimes."

    print(f"Input: \"{test_text}\"\n")

    # JSON results
    print("[JSON PROMPTING - 3 Runs]")
    json_results = []
    for i in range(3):
        result = comparator.classify_with_json(test_text)
        json_results.append(result)
        print(f"Run {i+1}: {json.dumps(result, indent=2)}")

    # Check consistency
    categories = [r["category"] for r in json_results]
    priorities = [r["priority"] for r in json_results]
    sentiments = [r["sentiment"] for r in json_results]

    print(f"\nConsistency Analysis:")
    print(f"  Categories: {categories} - {'✓ Consistent' if len(set(categories)) == 1 else '✗ Inconsistent'}")
    print(f"  Priorities: {priorities} - {'✓ Consistent' if len(set(priorities)) == 1 else '✗ Inconsistent'}")
    print(f"  Sentiments: {sentiments} - {'✓ Consistent' if len(set(sentiments)) == 1 else '✗ Inconsistent'}")


def display_summary():
    """Display comparison summary."""
    print("\n" + "=" * 80)
    print("Summary: JSON vs Natural Language Prompting")
    print("=" * 80)
    print()

    summary = """
    JSON PROMPTING ADVANTAGES:
    ✓ Structured output that's machine-readable
    ✓ Easy to parse and validate
    ✓ Consistent field names and formats
    ✓ Type safety and constraints
    ✓ Better for integration with other systems
    ✓ More reliable for batch processing

    NATURAL LANGUAGE PROMPTING ADVANTAGES:
    ✓ More flexible and expressive
    ✓ Better for exploratory tasks
    ✓ Can include nuanced explanations
    ✓ More natural for human readers
    ✓ Easier to debug and understand reasoning

    RECOMMENDATION:
    • Use JSON for: Data extraction, classification, structured generation
    • Use Natural Language for: Creative writing, explanations, conversations
    """

    print(summary)


def main():
    """Main execution function."""
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment variables")
        print("Please set it in your .env file or environment")
        return

    try:
        # Run comparison
        run_comparison()

        # Run consistency test
        run_consistency_test()

        # Display summary
        display_summary()

    except Exception as e:
        print(f"\nError occurred: {e}")
        print("\nPlease check:")
        print("1. Your OpenAI API key is valid")
        print("2. You have sufficient API credits")
        print("3. Your internet connection is stable")


if __name__ == "__main__":
    main()
