import os
import json
from groq import Groq
from dotenv import load_dotenv
from backend.core.models import NegotiationOutput

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

NEGOTIATION_PROMPT = """
You are an expert contract negotiation advisor for startup founders.

You will receive a contract along with its legal and compliance risk findings.
Your job is to generate specific, actionable negotiation recommendations
that a founder can bring back to the other party.

Return ONLY a valid JSON object with exactly this structure, no explanation, no markdown:
{
  "suggestions": ["<suggestion 1>", "<suggestion 2>", "<suggestion 3>"],
  "safer_alternatives": ["<alternative 1>", "<alternative 2>", "<alternative 3>"]
}

Rules:
- suggestions should be specific negotiation moves the founder can make
- safer_alternatives should be concrete clause rewrites or replacements
- Write in plain English, not legalese
- Examples of good suggestions:
  "Request a liability cap equal to 12 months of contract value"
  "Negotiate a 30-day termination notice period instead of 7 days"
  "Ask for explicit data deletion clause upon contract termination"
- Examples of good safer_alternatives:
  "Replace unlimited liability with: liability capped at total fees paid in last 12 months"
  "Replace auto-renewal with: contract requires written confirmation to renew"
- Be specific to the actual contract risks found, not generic advice
"""

async def run_negotiation_agent(
    contract_text: str,
    legal_findings: str,
    compliance_findings: str
) -> NegotiationOutput:
    try:
        combined_input = f"""
CONTRACT TEXT:
{contract_text}

LEGAL RISK FINDINGS:
{legal_findings}

COMPLIANCE FINDINGS:
{compliance_findings}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": NEGOTIATION_PROMPT},
                {"role": "user", "content": combined_input}
            ],
            temperature=0.2,
            max_tokens=800,
            response_format={"type": "json_object"}
        )

        raw = response.choices[0].message.content
        data = json.loads(raw)

        return NegotiationOutput(
            suggestions=data["suggestions"],
            safer_alternatives=data["safer_alternatives"]
        )

    except Exception:
        return NegotiationOutput(
            suggestions=["Unable to generate suggestions — escalating for safety"],
            safer_alternatives=["Unable to generate alternatives — escalating for safety"]
        )