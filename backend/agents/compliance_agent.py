import os
import json
from groq import Groq
from dotenv import load_dotenv
from backend.core.models import ComplianceOutput

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

COMPLIANCE_PROMPT = """
You are an expert regulatory compliance inspector specializing in startup contracts.

Analyze the following contract text and check for:
1. Privacy language and data protection clauses
2. Data handling obligations
3. GDPR-related concerns
4. Security commitments
5. Any missing compliance safeguards

Return ONLY a valid JSON object with exactly this structure, no explanation, no markdown:
{
  "is_authorized": <true or false>,
  "compliance_findings": "<one paragraph summarizing compliance status>",
  "violation_list": ["<violation 1>", "<violation 2>"]
}

Rules:
- is_authorized = true if the contract has no ACTIVE violations (sharing data without consent, no deletion rights, hidden data monetization)
- is_authorized = false ONLY if the contract actively violates data protection (e.g. sharing data without consent, no deletion clause, unlimited data retention)
- Missing GDPR language alone is NOT enough to fail — only active violations fail
- If contract is a simple service agreement with basic confidentiality, mark is_authorized = true
- violation_list should only contain ACTUAL violations found, not missing clauses
- If no violations found, return an empty list for violation_list
- Be proportionate — a freelance design contract is not the same as a data processing agreement
"""

async def run_compliance_agent(contract_text: str) -> ComplianceOutput:
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": COMPLIANCE_PROMPT},
                {"role": "user", "content": f"CONTRACT TEXT:\n\n{contract_text}"}
            ],
            temperature=0.1,
            max_tokens=800,
            response_format={"type": "json_object"}
        )

        raw = response.choices[0].message.content
        data = json.loads(raw)

        return ComplianceOutput(
            is_authorized=bool(data["is_authorized"]),
            compliance_findings=data["compliance_findings"],
            violation_list=data["violation_list"]
        )

    except Exception:
        # Safe default on failure
        return ComplianceOutput(
            is_authorized=False,
            compliance_findings="Compliance analysis failed. Manual review required.",
            violation_list=["Unable to analyze — escalating for safety"]
        )