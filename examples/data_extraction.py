"""
Module: examples/data_extraction.py
Description: Extract structured data from various document types using JSON prompting

This example demonstrates how to use JSON prompting to extract structured
data from invoices, resumes, and product reviews with high accuracy.

Usage:
    python examples/data_extraction.py

Requirements:
    - OPENAI_API_KEY in environment variables
    - Python 3.9+
"""

import os
import json
from typing import Dict, Any
from dotenv import load_dotenv

try:
    from openai import OpenAI
except ImportError:
    print("OpenAI package not installed. Install with: pip install openai")
    exit(1)

load_dotenv()


class DataExtractor:
    """Extract structured data from various document types."""

    def __init__(self):
        """Initialize OpenAI client."""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")

    def extract_invoice_data(self, invoice_text: str) -> Dict[str, Any]:
        """
        Extract structured data from invoice text.

        Args:
            invoice_text: Raw invoice text

        Returns:
            Dictionary containing extracted invoice data
        """
        schema = {
            "invoice_number": "string",
            "invoice_date": "string (ISO 8601 format: YYYY-MM-DD)",
            "due_date": "string (ISO 8601 format: YYYY-MM-DD)",
            "vendor_name": "string",
            "vendor_address": "string or null",
            "customer_name": "string",
            "customer_address": "string or null",
            "subtotal": "number",
            "tax": "number",
            "total": "number",
            "currency": "string (3-letter code, e.g., USD)",
            "line_items": [
                {
                    "description": "string",
                    "quantity": "number",
                    "unit_price": "number",
                    "total": "number"
                }
            ]
        }

        prompt = f"""Extract structured data from the following invoice.

Invoice Text:
{invoice_text}

Output Format (JSON):
{json.dumps(schema, indent=2)}

Instructions:
- Use null for any field not found in the invoice
- Dates must be in ISO 8601 format (YYYY-MM-DD)
- All monetary values should be numeric (no currency symbols)
- Line items should be an array of objects

Return only valid JSON:"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)

    def extract_resume_data(self, resume_text: str) -> Dict[str, Any]:
        """
        Extract structured data from resume text.

        Args:
            resume_text: Raw resume text

        Returns:
            Dictionary containing extracted resume data
        """
        schema = {
            "name": "string",
            "email": "string or null",
            "phone": "string or null",
            "location": "string or null",
            "summary": "string or null",
            "skills": ["array of strings"],
            "experience": [
                {
                    "company": "string",
                    "title": "string",
                    "start_date": "string (YYYY-MM or YYYY)",
                    "end_date": "string (YYYY-MM or YYYY) or 'Present'",
                    "description": "string",
                    "achievements": ["array of strings"]
                }
            ],
            "education": [
                {
                    "institution": "string",
                    "degree": "string",
                    "field": "string or null",
                    "graduation_date": "string (YYYY-MM or YYYY) or null"
                }
            ],
            "certifications": ["array of strings or empty array"]
        }

        prompt = f"""Extract structured data from the following resume.

Resume Text:
{resume_text}

Output Format (JSON):
{json.dumps(schema, indent=2)}

Instructions:
- Use null for fields not found
- Skills should be individual strings in an array
- Experience should be ordered from most recent to oldest
- Extract key achievements as bullet points
- Use 'Present' for current positions

Return only valid JSON:"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)

    def extract_review_data(self, review_text: str) -> Dict[str, Any]:
        """
        Extract structured analysis from product review.

        Args:
            review_text: Raw product review text

        Returns:
            Dictionary containing extracted review analysis
        """
        schema = {
            "overall_rating": "integer (1-5)",
            "sentiment": "string (positive, negative, or neutral)",
            "aspects": {
                "quality": {
                    "rating": "integer (1-5) or null",
                    "comments": "string or null"
                },
                "value": {
                    "rating": "integer (1-5) or null",
                    "comments": "string or null"
                },
                "service": {
                    "rating": "integer (1-5) or null",
                    "comments": "string or null"
                }
            },
            "pros": ["array of strings"],
            "cons": ["array of strings"],
            "recommendation": "boolean",
            "key_themes": ["array of strings"],
            "summary": "string (1-2 sentences)"
        }

        prompt = f"""Analyze the following product review and extract structured information.

Review Text:
{review_text}

Output Format (JSON):
{json.dumps(schema, indent=2)}

Instructions:
- Infer overall rating from the text if not explicitly stated
- Extract pros and cons as separate points
- Identify 3-5 key themes
- Provide a brief 1-2 sentence summary
- Use null for aspects not mentioned

Return only valid JSON:"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)


def demo_invoice_extraction():
    """Demonstrate invoice data extraction."""
    print("=" * 80)
    print("Invoice Data Extraction")
    print("=" * 80)
    print()

    sample_invoice = """
    INVOICE

    Invoice #: INV-2024-001
    Date: January 15, 2024
    Due Date: February 15, 2024

    From:
    Acme Corporation
    123 Business St
    New York, NY 10001

    To:
    John Smith Consulting
    456 Client Ave
    Los Angeles, CA 90001

    Items:
    1. Web Development Services - 40 hours @ $150/hr = $6,000.00
    2. UI/UX Design - 20 hours @ $120/hr = $2,400.00
    3. Project Management - 10 hours @ $100/hr = $1,000.00

    Subtotal: $9,400.00
    Tax (8.5%): $799.00
    Total: $10,199.00

    Payment Terms: Net 30
    """

    extractor = DataExtractor()

    print("Sample Invoice:")
    print(sample_invoice)
    print("\n" + "-" * 80 + "\n")

    print("Extracted Data:")
    result = extractor.extract_invoice_data(sample_invoice)
    print(json.dumps(result, indent=2))
    print()


def demo_resume_extraction():
    """Demonstrate resume data extraction."""
    print("=" * 80)
    print("Resume Data Extraction")
    print("=" * 80)
    print()

    sample_resume = """
    JANE DOE
    jane.doe@email.com | (555) 123-4567 | San Francisco, CA

    PROFESSIONAL SUMMARY
    Experienced software engineer with 8+ years building scalable web applications.
    Specialized in Python, React, and cloud infrastructure.

    SKILLS
    Python, JavaScript, React, Node.js, AWS, Docker, Kubernetes, PostgreSQL,
    MongoDB, Redis, Git, CI/CD, Agile/Scrum

    EXPERIENCE

    Senior Software Engineer | Tech Innovations Inc. | Jan 2020 - Present
    - Led development of microservices architecture serving 1M+ users
    - Reduced API response time by 40% through optimization
    - Mentored team of 5 junior developers

    Software Engineer | StartupXYZ | Jun 2017 - Dec 2019
    - Built RESTful APIs using Python/Flask and PostgreSQL
    - Implemented automated testing pipeline, improving code coverage to 85%
    - Collaborated with product team on feature prioritization

    Junior Developer | Digital Solutions Co. | Aug 2015 - May 2017
    - Developed frontend components using React and Redux
    - Fixed bugs and improved application performance
    - Participated in code reviews and daily standups

    EDUCATION

    B.S. in Computer Science | University of California, Berkeley | 2015
    Minor in Mathematics

    CERTIFICATIONS
    - AWS Certified Solutions Architect
    - Certified Kubernetes Administrator
    """

    extractor = DataExtractor()

    print("Sample Resume:")
    print(sample_resume)
    print("\n" + "-" * 80 + "\n")

    print("Extracted Data:")
    result = extractor.extract_resume_data(sample_resume)
    print(json.dumps(result, indent=2))
    print()


def demo_review_extraction():
    """Demonstrate product review analysis."""
    print("=" * 80)
    print("Product Review Analysis")
    print("=" * 80)
    print()

    sample_review = """
    I've been using this laptop for 3 months now and I'm really impressed!
    The build quality is excellent - it feels premium and sturdy. The
    performance is outstanding for the price point. I can easily run
    multiple applications simultaneously without any lag.

    The battery life is phenomenal - I get a full 8-9 hours of actual work
    time, which is rare for laptops in this category. The keyboard is
    comfortable to type on for extended periods.

    However, there are a few downsides. The trackpad is a bit too sensitive
    for my liking, and I sometimes trigger clicks accidentally. The speakers
    are just okay - they're fine for video calls but not great for music.
    Also, it does run a bit warm when doing intensive tasks.

    Customer service was responsive when I had a question about the warranty.
    Overall, I would definitely recommend this to anyone looking for a solid
    work laptop that won't break the bank. It's an excellent value for money.
    """

    extractor = DataExtractor()

    print("Sample Review:")
    print(sample_review)
    print("\n" + "-" * 80 + "\n")

    print("Extracted Analysis:")
    result = extractor.extract_review_data(sample_review)
    print(json.dumps(result, indent=2))
    print()


def main():
    """Main execution function."""
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment variables")
        print("Please set it in your .env file or environment")
        return

    try:
        # Run demonstrations
        demo_invoice_extraction()
        demo_resume_extraction()
        demo_review_extraction()

        print("=" * 80)
        print("Data Extraction Complete!")
        print("=" * 80)
        print()
        print("Key Benefits of JSON Prompting for Data Extraction:")
        print("  ✓ Consistent structure across all extractions")
        print("  ✓ Easy validation and error checking")
        print("  ✓ Direct integration with databases and APIs")
        print("  ✓ Type safety (numbers, dates, booleans)")
        print("  ✓ Handles missing data with null values")
        print()

    except Exception as e:
        print(f"\nError occurred: {e}")
        print("\nPlease check:")
        print("1. Your OpenAI API key is valid")
        print("2. You have sufficient API credits")
        print("3. Your internet connection is stable")


if __name__ == "__main__":
    main()
