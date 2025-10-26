"""
Module: examples/content_generation.py
Description: Generate structured content using JSON prompting

This example demonstrates how to use JSON prompting to generate various
types of content including blog posts, marketing copy, and social media posts.

Usage:
    python examples/content_generation.py

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


class ContentGenerator:
    """Generate structured content using JSON prompting."""

    def __init__(self):
        """Initialize OpenAI client."""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")

    def generate_blog_post(self, topic: str, target_audience: str, tone: str) -> Dict[str, Any]:
        """
        Generate a structured blog post.

        Args:
            topic: Blog post topic
            target_audience: Target audience description
            tone: Desired tone (professional, casual, technical, etc.)

        Returns:
            Dictionary with structured blog post content
        """
        schema = {
            "metadata": {
                "title": "string (catchy, SEO-friendly title)",
                "slug": "string (URL-friendly slug)",
                "meta_description": "string (150-160 characters)",
                "keywords": ["array of 5-10 SEO keywords"],
                "estimated_reading_time": "string (e.g., '5 min read')",
                "target_audience": "string",
                "tone": "string"
            },
            "content": {
                "hook": "string (engaging opening paragraph)",
                "sections": [
                    {
                        "heading": "string (H2 section heading)",
                        "content": "string (section content)",
                        "key_takeaway": "string (main point of section)"
                    }
                ],
                "conclusion": "string (summarizing paragraph)",
                "call_to_action": "string (CTA for readers)"
            },
            "seo": {
                "featured_image_suggestions": ["array of image descriptions"],
                "internal_link_opportunities": ["array of related topics"],
                "social_media_snippets": {
                    "twitter": "string (280 chars max)",
                    "linkedin": "string (150 words max)",
                    "facebook": "string (100 words max)"
                }
            }
        }

        prompt = f"""Create a structured blog post about: {topic}

Target Audience: {target_audience}
Tone: {tone}

Output Format (JSON):
{json.dumps(schema, indent=2)}

Requirements:
- Title should be attention-grabbing and SEO-optimized
- Include 4-6 main sections with clear headings
- Each section should have a key takeaway
- Meta description must be 150-160 characters
- Provide actionable content
- Include strong CTA

Return only valid JSON:"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)

    def generate_marketing_copy(self, product: str, benefits: list, audience: str) -> Dict[str, Any]:
        """
        Generate marketing copy for a product.

        Args:
            product: Product name/description
            benefits: List of key product benefits
            audience: Target audience description

        Returns:
            Dictionary with structured marketing content
        """
        schema = {
            "product_name": "string",
            "headline": "string (attention-grabbing, 10-15 words)",
            "subheadline": "string (supporting headline, 15-25 words)",
            "value_proposition": "string (clear unique value, 2-3 sentences)",
            "features_benefits": [
                {
                    "feature": "string (product feature)",
                    "benefit": "string (how it helps customer)",
                    "icon_suggestion": "string (icon that represents this)"
                }
            ],
            "social_proof": {
                "testimonial_template": "string (template for customer quote)",
                "stat_callouts": ["array of compelling statistics to highlight"]
            },
            "cta": {
                "primary": "string (main call-to-action)",
                "secondary": "string (alternative CTA)",
                "urgency_element": "string (create FOMO/urgency)"
            },
            "objection_handlers": [
                {
                    "objection": "string (potential customer concern)",
                    "response": "string (how to address it)"
                }
            ]
        }

        prompt = f"""Create marketing copy for the following product:

Product: {product}
Key Benefits: {', '.join(benefits)}
Target Audience: {audience}

Output Format (JSON):
{json.dumps(schema, indent=2)}

Requirements:
- Focus on benefits, not just features
- Address customer pain points
- Create urgency without being pushy
- Include 4-6 feature/benefit pairs
- Address common objections
- Strong, clear CTAs

Return only valid JSON:"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)

    def generate_social_media_content(self, topic: str, platform: str, goal: str) -> Dict[str, Any]:
        """
        Generate social media content.

        Args:
            topic: Content topic
            platform: Social media platform (twitter, linkedin, instagram, etc.)
            goal: Content goal (engagement, awareness, conversions, etc.)

        Returns:
            Dictionary with social media content variations
        """
        schema = {
            "platform": "string",
            "topic": "string",
            "goal": "string",
            "posts": [
                {
                    "version": "string (A, B, C for A/B testing)",
                    "content": "string (main post text)",
                    "character_count": "integer",
                    "hashtags": ["array of relevant hashtags"],
                    "emojis": ["array of suggested emojis"],
                    "visual_suggestions": "string (image/video description)",
                    "best_posting_time": "string (recommended time)",
                    "expected_engagement": "string (low, medium, high)"
                }
            ],
            "engagement_hooks": {
                "question": "string (question to drive comments)",
                "poll_option": {
                    "question": "string",
                    "options": ["array of 2-4 poll options"]
                },
                "controversy": "string (thought-provoking statement)"
            },
            "caption_variations": [
                "array of 3 different caption styles (formal, casual, humorous)"
            ]
        }

        prompt = f"""Create social media content for:

Topic: {topic}
Platform: {platform}
Goal: {goal}

Output Format (JSON):
{json.dumps(schema, indent=2)}

Requirements:
- Create 3 versions for A/B testing
- Follow platform character limits
- Include strategic hashtags (not too many)
- Suggest engaging visuals
- Include hooks to drive engagement
- Optimize for platform algorithm

Return only valid JSON:"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)


def demo_blog_post():
    """Demonstrate blog post generation."""
    print("=" * 80)
    print("Content Type 1: Blog Post Generation")
    print("=" * 80)
    print()

    generator = ContentGenerator()

    topic = "Best practices for remote team collaboration"
    audience = "Tech startup managers and team leads"
    tone = "professional but approachable"

    print(f"Topic: {topic}")
    print(f"Audience: {audience}")
    print(f"Tone: {tone}")
    print("\n" + "-" * 80 + "\n")

    result = generator.generate_blog_post(topic, audience, tone)
    print("Generated Blog Post:")
    print(json.dumps(result, indent=2))
    print()


def demo_marketing_copy():
    """Demonstrate marketing copy generation."""
    print("=" * 80)
    print("Content Type 2: Marketing Copy Generation")
    print("=" * 80)
    print()

    generator = ContentGenerator()

    product = "AI-powered project management tool"
    benefits = [
        "Automated task prioritization",
        "Real-time team collaboration",
        "Intelligent deadline predictions",
        "Integration with 100+ tools"
    ]
    audience = "Small to medium-sized business owners"

    print(f"Product: {product}")
    print(f"Benefits: {', '.join(benefits)}")
    print(f"Audience: {audience}")
    print("\n" + "-" * 80 + "\n")

    result = generator.generate_marketing_copy(product, benefits, audience)
    print("Generated Marketing Copy:")
    print(json.dumps(result, indent=2))
    print()


def demo_social_media():
    """Demonstrate social media content generation."""
    print("=" * 80)
    print("Content Type 3: Social Media Content Generation")
    print("=" * 80)
    print()

    generator = ContentGenerator()

    topic = "Launching our new productivity feature"
    platform = "LinkedIn"
    goal = "Drive sign-ups for beta program"

    print(f"Topic: {topic}")
    print(f"Platform: {platform}")
    print(f"Goal: {goal}")
    print("\n" + "-" * 80 + "\n")

    result = generator.generate_social_media_content(topic, platform, goal)
    print("Generated Social Media Content:")
    print(json.dumps(result, indent=2))
    print()


def main():
    """Main execution function."""
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment variables")
        print("Please set it in your .env file or environment")
        return

    try:
        # Demonstrate different content types
        demo_blog_post()
        demo_marketing_copy()
        demo_social_media()

        print("=" * 80)
        print("Content Generation Complete!")
        print("=" * 80)
        print()
        print("Benefits of JSON Prompting for Content Generation:")
        print("  ✓ Consistent structure across all content pieces")
        print("  ✓ Easy to template and reuse")
        print("  ✓ SEO metadata automatically included")
        print("  ✓ Multiple variations for A/B testing")
        print("  ✓ Clear separation of content and metadata")
        print("  ✓ Integration-ready (CMS, social media schedulers)")
        print()
        print("Use Cases:")
        print("  • Content marketing at scale")
        print("  • Multi-platform campaign creation")
        print("  • Automated content calendars")
        print("  • SEO-optimized article generation")
        print("  • Social media scheduling tools")
        print()

    except Exception as e:
        print(f"\nError occurred: {e}")
        print("\nPlease check:")
        print("1. Your OpenAI API key is valid")
        print("2. You have sufficient API credits")
        print("3. Your internet connection is stable")


if __name__ == "__main__":
    main()
