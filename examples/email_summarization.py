"""
Module: examples/email_summarization.py
Description: Demonstrate three different approaches to email summarization using JSON

This example shows how to use JSON prompting for email summarization with
different output formats: bullet points, executive summary, and action items.

Usage:
    python examples/email_summarization.py

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


class EmailSummarizer:
    """Summarize emails using different JSON-structured approaches."""

    def __init__(self):
        """Initialize OpenAI client."""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")

    def summarize_bullet_points(self, email_text: str) -> Dict[str, Any]:
        """
        Summarize email as structured bullet points.

        Args:
            email_text: Raw email content

        Returns:
            Dictionary with categorized bullet points
        """
        schema = {
            "subject": "string",
            "sender": "string",
            "key_points": ["array of strings (main points from email)"],
            "decisions_made": ["array of strings (any decisions mentioned)"],
            "questions_raised": ["array of strings (questions that need answers)"],
            "next_steps": ["array of strings (proposed actions)"],
            "people_mentioned": ["array of strings (names mentioned)"],
            "urgency": "string (low, medium, high, critical)"
        }

        prompt = f"""Summarize the following email as structured bullet points.

Email:
{email_text}

Output Format (JSON):
{json.dumps(schema, indent=2)}

Instructions:
- Extract main points as concise bullet points
- Identify any decisions that were made
- List questions that need answering
- Note proposed next steps or action items
- List people mentioned (first and last names)
- Assess urgency based on language and content

Return only valid JSON:"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)

    def summarize_executive(self, email_text: str) -> Dict[str, Any]:
        """
        Create executive summary of email.

        Args:
            email_text: Raw email content

        Returns:
            Dictionary with executive summary
        """
        schema = {
            "subject": "string",
            "sender": "string",
            "one_line_summary": "string (10-15 words)",
            "executive_summary": "string (2-3 sentences)",
            "business_impact": "string (potential impact on business)",
            "recommended_action": "string (what recipient should do)",
            "deadline": "string or null (any mentioned deadlines)",
            "priority": "string (low, medium, high, critical)",
            "requires_response": "boolean",
            "estimated_reading_time": "string (e.g., '2 minutes')"
        }

        prompt = f"""Create an executive summary of the following email.

Email:
{email_text}

Output Format (JSON):
{json.dumps(schema, indent=2)}

Instructions:
- Provide a concise one-line summary
- Write 2-3 sentence executive summary
- Assess business impact
- Recommend specific action for recipient
- Identify any deadlines mentioned
- Estimate reading time for original email

Return only valid JSON:"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)

    def extract_action_items(self, email_text: str) -> Dict[str, Any]:
        """
        Extract actionable items from email.

        Args:
            email_text: Raw email content

        Returns:
            Dictionary with structured action items
        """
        schema = {
            "subject": "string",
            "sender": "string",
            "action_items": [
                {
                    "task": "string (specific task description)",
                    "owner": "string (person responsible) or null",
                    "deadline": "string or null (YYYY-MM-DD format if mentioned)",
                    "priority": "string (low, medium, high)",
                    "status": "string (pending, in_progress, completed)",
                    "dependencies": ["array of strings (what this depends on)"]
                }
            ],
            "follow_ups_required": ["array of strings"],
            "information_needed": ["array of strings (missing info to proceed)"],
            "stakeholders": ["array of strings (people who should be informed)"]
        }

        prompt = f"""Extract all action items and follow-ups from the following email.

Email:
{email_text}

Output Format (JSON):
{json.dumps(schema, indent=2)}

Instructions:
- Identify specific, actionable tasks
- Determine who is responsible (if mentioned)
- Extract deadlines in YYYY-MM-DD format
- Assess priority of each task
- Note any dependencies between tasks
- List information still needed
- Identify stakeholders who should be kept informed

Return only valid JSON:"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)


def demo_bullet_points():
    """Demonstrate bullet point summarization."""
    print("=" * 80)
    print("Approach 1: Bullet Point Summary")
    print("=" * 80)
    print()

    sample_email = """
    From: Sarah Johnson <sarah.johnson@company.com>
    To: Project Team <team@company.com>
    Subject: Q4 Project Status Update and Next Steps

    Hi Team,

    I wanted to share an update on our Q4 project progress and outline our
    next steps.

    First, great work everyone! We've completed the initial design phase and
    received positive feedback from stakeholders. The prototype has been
    approved with minor revisions requested by Marketing.

    However, we're running about one week behind schedule due to the API
    integration issues we encountered last month. The Dev team has resolved
    most of these, but we need to do additional testing before proceeding.

    Key decisions from yesterday's meeting:
    1. We'll extend the testing phase by one week
    2. Marketing will provide revised copy by Friday
    3. We're moving the launch date from Nov 15 to Nov 22

    Action items:
    - John: Complete API testing by this Friday
    - Maria: Review updated designs and provide feedback by Wed
    - Everyone: Please update your task status in Jira by EOD

    Questions for the team:
    - Do we need additional resources for the extended testing phase?
    - Should we notify external partners about the new launch date?

    Let's discuss these items in our standup tomorrow. Please reach out if
    you have any concerns.

    Thanks,
    Sarah
    """

    summarizer = EmailSummarizer()

    print("Original Email:")
    print(sample_email)
    print("\n" + "-" * 80 + "\n")

    print("Structured Summary:")
    result = summarizer.summarize_bullet_points(sample_email)
    print(json.dumps(result, indent=2))
    print()


def demo_executive_summary():
    """Demonstrate executive summary."""
    print("=" * 80)
    print("Approach 2: Executive Summary")
    print("=" * 80)
    print()

    sample_email = """
    From: Michael Chen <mchen@vendorcorp.com>
    To: Jennifer Martinez <jmartinez@company.com>
    Subject: Urgent: Contract Renewal Decision Needed by End of Week

    Dear Jennifer,

    I hope this email finds you well. I'm reaching out regarding your
    company's software license agreement, which is set to expire on
    October 31st.

    We've prepared a renewal proposal with several enhancements:
    - 20% discount on annual licensing fees (down from $50K to $40K)
    - Inclusion of our new Analytics Pro module at no additional cost
    - Extended support hours (24/7 instead of business hours only)
    - Dedicated account manager

    This offer is part of our Q4 promotion and is only available if we
    receive confirmation by Friday, October 27th. After this date, the
    standard pricing of $50K will apply.

    Given that your team has 50+ active users relying on our platform daily,
    any interruption in service could significantly impact your operations.
    I'd hate for your team to experience downtime during your busy season.

    I'm available for a call this week to discuss any questions or concerns.
    I can also arrange a demo of the Analytics Pro module if you'd like to
    see it in action before deciding.

    Please let me know how you'd like to proceed. I need a decision by
    Friday to lock in this pricing.

    Best regards,
    Michael Chen
    Senior Account Executive
    VendorCorp
    """

    summarizer = EmailSummarizer()

    print("Original Email:")
    print(sample_email)
    print("\n" + "-" * 80 + "\n")

    print("Executive Summary:")
    result = summarizer.summarize_executive(sample_email)
    print(json.dumps(result, indent=2))
    print()


def demo_action_items():
    """Demonstrate action item extraction."""
    print("=" * 80)
    print("Approach 3: Action Item Extraction")
    print("=" * 80)
    print()

    sample_email = """
    From: David Park <dpark@company.com>
    To: Product Team <product@company.com>
    Subject: Action Items from Client Feedback Session

    Team,

    Thanks for joining today's client feedback session. Here's what we need
    to do based on their input:

    HIGH PRIORITY:
    1. Fix the login timeout issue - this is affecting multiple clients.
       Tom, can you investigate and have a fix ready by next Tuesday?

    2. Add export functionality to reports - clients specifically mentioned
       needing CSV and PDF options. Lisa, please work with Design on the UI
       for this. Target: Sprint 24 (starting Nov 1)

    3. Update the API documentation - it's currently outdated and causing
       confusion. Sam, please coordinate with Engineering to get this done
       by end of month.

    MEDIUM PRIORITY:
    4. Improve mobile responsiveness on the dashboard - we'll need designs
       from the UX team before Dev can start. Rachel, can you work with
       Alex on mockups? No hard deadline but would be good to have for Q1.

    5. Consider adding SSO integration - several clients asked about this.
       This is a bigger lift, so let's discuss feasibility in next week's
       planning meeting.

    FOLLOW-UPS:
    - I need to schedule a follow-up call with Acme Corp by next Friday
    - We should send a survey to all beta users for additional feedback
    - Legal needs to review the new terms of service before we can proceed
      with the enterprise features

    BLOCKERS:
    - The API fix depends on the infrastructure upgrade (DevOps is working on it)
    - We're waiting on final approval from Finance for the additional contractor budget

    Please update your progress in Monday's standup. Let me know if you need
    any clarification on your tasks.

    David
    """

    summarizer = EmailSummarizer()

    print("Original Email:")
    print(sample_email)
    print("\n" + "-" * 80 + "\n")

    print("Extracted Action Items:")
    result = summarizer.extract_action_items(sample_email)
    print(json.dumps(result, indent=2))
    print()


def main():
    """Main execution function."""
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment variables")
        print("Please set it in your .env file or environment")
        return

    try:
        # Demonstrate three approaches
        demo_bullet_points()
        demo_executive_summary()
        demo_action_items()

        print("=" * 80)
        print("Email Summarization Complete!")
        print("=" * 80)
        print()
        print("Three Approaches Comparison:")
        print()
        print("1. BULLET POINTS:")
        print("   • Best for: Quick reference and meeting notes")
        print("   • Structure: Categorized lists of key information")
        print("   • Use case: Daily email triage, team updates")
        print()
        print("2. EXECUTIVE SUMMARY:")
        print("   • Best for: Leadership and decision-makers")
        print("   • Structure: Concise overview with business impact")
        print("   • Use case: Priority assessment, quick decisions")
        print()
        print("3. ACTION ITEMS:")
        print("   • Best for: Task management and project tracking")
        print("   • Structure: Detailed tasks with owners and deadlines")
        print("   • Use case: Project management, accountability tracking")
        print()

    except Exception as e:
        print(f"\nError occurred: {e}")
        print("\nPlease check:")
        print("1. Your OpenAI API key is valid")
        print("2. You have sufficient API credits")
        print("3. Your internet connection is stable")


if __name__ == "__main__":
    main()
