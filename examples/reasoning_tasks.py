"""
Module: examples/reasoning_tasks.py
Description: Demonstrate complex reasoning tasks using JSON prompting

This example shows how JSON prompting can structure multi-step reasoning
including mathematical problem-solving, logical reasoning, and ethical analysis.

Usage:
    python examples/reasoning_tasks.py

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


class ReasoningEngine:
    """Perform complex reasoning tasks using structured JSON prompting."""

    def __init__(self):
        """Initialize OpenAI client."""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")

    def solve_math_problem(self, problem: str) -> Dict[str, Any]:
        """
        Solve a mathematical problem with step-by-step reasoning.

        Args:
            problem: Mathematical problem description

        Returns:
            Dictionary with structured solution
        """
        schema = {
            "problem": "string (restated problem)",
            "problem_type": "string (algebra, geometry, calculus, etc.)",
            "given_information": ["array of known values/facts"],
            "what_to_find": "string (what we're solving for)",
            "approach": "string (strategy to solve the problem)",
            "steps": [
                {
                    "step_number": "integer",
                    "description": "string (what this step does)",
                    "calculation": "string (actual calculation)",
                    "result": "string (result of this step)",
                    "reasoning": "string (why we do this step)"
                }
            ],
            "final_answer": "string (the final numerical answer)",
            "verification": "string (how to verify the answer is correct)",
            "alternative_methods": ["array of other ways to solve this"]
        }

        prompt = f"""Solve the following mathematical problem step by step.

Problem: {problem}

Output Format (JSON):
{json.dumps(schema, indent=2)}

Requirements:
- Show every step of your reasoning
- Explain why each step is necessary
- Provide clear calculations
- Verify your answer
- Suggest alternative solution methods

Return only valid JSON:"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)

    def logical_reasoning(self, scenario: str) -> Dict[str, Any]:
        """
        Perform logical reasoning analysis.

        Args:
            scenario: Logical reasoning scenario

        Returns:
            Dictionary with structured logical analysis
        """
        schema = {
            "scenario": "string (restated scenario)",
            "premises": ["array of given statements/facts"],
            "logical_type": "string (deductive, inductive, abductive)",
            "reasoning_chain": [
                {
                    "step": "integer",
                    "statement": "string (logical statement)",
                    "justification": "string (why this follows)",
                    "logical_rule": "string (rule applied, e.g., modus ponens)"
                }
            ],
            "conclusion": "string (final logical conclusion)",
            "validity": "string (valid or invalid)",
            "soundness": "string (sound or unsound)",
            "assumptions": ["array of underlying assumptions"],
            "potential_fallacies": [
                {
                    "fallacy": "string (name of fallacy)",
                    "explanation": "string (how it might apply)"
                }
            ],
            "counterarguments": ["array of potential objections"]
        }

        prompt = f"""Analyze the logical reasoning in the following scenario.

Scenario: {scenario}

Output Format (JSON):
{json.dumps(schema, indent=2)}

Requirements:
- Identify all premises
- Show clear reasoning chain
- Apply formal logical rules
- Assess validity and soundness
- Identify assumptions
- Check for logical fallacies
- Consider counterarguments

Return only valid JSON:"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)

    def ethical_analysis(self, dilemma: str) -> Dict[str, Any]:
        """
        Analyze an ethical dilemma from multiple perspectives.

        Args:
            dilemma: Ethical dilemma description

        Returns:
            Dictionary with multi-perspective ethical analysis
        """
        schema = {
            "dilemma": "string (restated dilemma)",
            "stakeholders": [
                {
                    "name": "string (stakeholder or group)",
                    "interests": ["array of their interests"],
                    "potential_impact": "string (how they're affected)"
                }
            ],
            "ethical_frameworks": [
                {
                    "framework": "string (e.g., utilitarianism, deontology, virtue ethics)",
                    "analysis": "string (analysis from this perspective)",
                    "recommended_action": "string (what this framework suggests)",
                    "strengths": ["array of strong points"],
                    "weaknesses": ["array of limitations"]
                }
            ],
            "key_ethical_principles": ["array of relevant principles"],
            "potential_actions": [
                {
                    "action": "string (possible course of action)",
                    "pros": ["array of advantages"],
                    "cons": ["array of disadvantages"],
                    "ethical_score": "integer (1-10)",
                    "practical_score": "integer (1-10)"
                }
            ],
            "recommendation": {
                "suggested_action": "string (recommended course of action)",
                "justification": "string (why this is recommended)",
                "implementation_considerations": ["array of practical factors"],
                "potential_unintended_consequences": ["array of risks"]
            }
        }

        prompt = f"""Analyze the following ethical dilemma from multiple ethical perspectives.

Dilemma: {dilemma}

Output Format (JSON):
{json.dumps(schema, indent=2)}

Requirements:
- Identify all stakeholders and their interests
- Analyze from at least 3 ethical frameworks
- Consider practical implications
- Evaluate multiple possible actions
- Provide balanced recommendation
- Acknowledge complexity and trade-offs

Return only valid JSON:"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)


def demo_math_problem():
    """Demonstrate mathematical problem-solving."""
    print("=" * 80)
    print("Reasoning Type 1: Mathematical Problem-Solving")
    print("=" * 80)
    print()

    engine = ReasoningEngine()

    problem = """A train leaves Station A traveling at 60 mph. Two hours later,
    another train leaves Station A traveling in the same direction at 75 mph.
    How long will it take the second train to catch up with the first train?"""

    print("Problem:")
    print(problem)
    print("\n" + "-" * 80 + "\n")

    result = engine.solve_math_problem(problem)
    print("Step-by-Step Solution:")
    print(json.dumps(result, indent=2))
    print()


def demo_logical_reasoning():
    """Demonstrate logical reasoning."""
    print("=" * 80)
    print("Reasoning Type 2: Logical Reasoning")
    print("=" * 80)
    print()

    engine = ReasoningEngine()

    scenario = """All software engineers at the company know Python.
    Sarah is a software engineer at the company.
    Some people who know Python also know JavaScript.
    Everyone who knows JavaScript can build web applications.
    What can we conclude about Sarah?"""

    print("Scenario:")
    print(scenario)
    print("\n" + "-" * 80 + "\n")

    result = engine.logical_reasoning(scenario)
    print("Logical Analysis:")
    print(json.dumps(result, indent=2))
    print()


def demo_ethical_analysis():
    """Demonstrate ethical dilemma analysis."""
    print("=" * 80)
    print("Reasoning Type 3: Ethical Analysis")
    print("=" * 80)
    print()

    engine = ReasoningEngine()

    dilemma = """A self-driving car company has discovered a bug in their software
    that could potentially cause accidents in rare weather conditions (heavy fog).
    The bug affects 100,000 vehicles currently on the road. Fixing the bug requires
    a software update that will temporarily disable certain convenience features
    for 2 weeks, frustrating customers. The company estimates the bug might cause
    1-2 accidents per year across all vehicles. Issuing a recall would cost $50
    million and damage the company's reputation, potentially leading to layoffs.
    What should the company do?"""

    print("Ethical Dilemma:")
    print(dilemma)
    print("\n" + "-" * 80 + "\n")

    result = engine.ethical_analysis(dilemma)
    print("Ethical Analysis:")
    print(json.dumps(result, indent=2))
    print()


def main():
    """Main execution function."""
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment variables")
        print("Please set it in your .env file or environment")
        return

    try:
        # Demonstrate different reasoning types
        demo_math_problem()
        demo_logical_reasoning()
        demo_ethical_analysis()

        print("=" * 80)
        print("Complex Reasoning Complete!")
        print("=" * 80)
        print()
        print("Benefits of JSON Prompting for Reasoning Tasks:")
        print()
        print("  ✓ TRANSPARENT REASONING:")
        print("    - Every step is explicitly documented")
        print("    - Easy to identify where reasoning goes wrong")
        print("    - Can verify each step independently")
        print()
        print("  ✓ STRUCTURED ANALYSIS:")
        print("    - Multiple perspectives clearly separated")
        print("    - Systematic evaluation of options")
        print("    - Consistent framework application")
        print()
        print("  ✓ AUDITABLE DECISIONS:")
        print("    - Clear trail of logic and assumptions")
        print("    - Stakeholders can review reasoning")
        print("    - Supports accountability and compliance")
        print()
        print("  ✓ REUSABLE PATTERNS:")
        print("    - Same structure for similar problems")
        print("    - Easy to template and automate")
        print("    - Facilitates comparison across cases")
        print()
        print("Use Cases:")
        print("  • Educational tools (showing work)")
        print("  • Decision support systems")
        print("  • Ethical review boards")
        print("  • Quality assurance and verification")
        print("  • Research and analysis")
        print("  • Explainable AI systems")
        print()

    except Exception as e:
        print(f"\nError occurred: {e}")
        print("\nPlease check:")
        print("1. Your OpenAI API key is valid")
        print("2. You have sufficient API credits")
        print("3. Your internet connection is stable")


if __name__ == "__main__":
    main()
