import os
import json
from groq import Groq
from dotenv import load_dotenv
from backend.core.models import BusinessImpactOutput

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

BUSINESS_IMPACT_PROMPT = """
You are a business advisor specializing in helping startup founders understand
the real-world consequences of contract clauses in plain English.

You will receive legal and compliance findings about a contract.
Your job is to translate those findings into clear business language
that a non-legal founder can immediately understand.

Return ONLY a valid JSON object with exactly this structure, no explanation, no markdown:
{
  "impact_summary": "<one paragraph explaining the overall business impact in plain English>",
  "key_concerns": ["<concern 1>", "<concern 2>", "<concern 3>"]
}

Rules:
- Write as if explaining to a first-time founder, not a lawyer
- Be direct about financial, operational, and reputational risks
- key_concerns should be short, punchy one-liners
- Examples of good key_concerns:
  "This clause may expose your startup to costs exceeding the contract value"
  "Vendor can terminate with 24 hours notice, risking your operations"
  "Auto-renewal locks you in for another year without warning"
- Be specific, not generic
"""

async def run_business_impact_agent(
    contract_text: str,
    legal_findings: str,
    compliance_findings: str
) -> BusinessImpactOutput:
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
                {"role": "system", "content": BUSINESS_IMPACT_PROMPT},
                {"role": "user", "content": combined_input}
            ],
            temperature=0.2,
            max_tokens=800,
            response_format={"type": "json_object"}
        )

        raw = response.choices[0].message.content
        data = json.loads(raw)

        return BusinessImpactOutput(
            impact_summary=data["impact_summary"],
            key_concerns=data["key_concerns"]
        )

    except Exception:
        return BusinessImpactOutput(
            impact_summary="Business impact analysis failed. Manual review required.",
            key_concerns=["Unable to analyze — escalating for safety"]
        )