import os
import json
from groq import Groq
from dotenv import load_dotenv
from backend.core.models import LegalRiskOutput, ClauseEvidence

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

LEGAL_RISK_PROMPT = """
You are an expert legal risk analyzer specializing in startup contracts.

Analyze the following contract text and identify:
1. Liability clauses (especially unlimited liability)
2. Indemnification clauses
3. Auto-renewal clauses
4. Termination clauses (especially one-sided)
5. Penalty clauses

Return ONLY a valid JSON object with exactly this structure, no explanation, no markdown:
{
  "risk_score": <float between 0 and 10>,
  "risk_explanation": "<one paragraph explaining the overall legal risk>",
  "flagged_clauses": ["<clause 1>", "<clause 2>"],
  "clause_evidence": [
    {
      "clause_name": "<short clause name>",
      "evidence": "<exact short quote or reference from the contract that triggered this finding>",
      "impact": "<one sentence on the business impact of this clause>"
    }
  ]
}

Rules:
- risk_score 0-3: Low risk, standard clauses
- risk_score 4-6: Medium risk, some concerning clauses
- risk_score 7-10: High risk, dangerous clauses present
- flagged_clauses should match the clause_name values in clause_evidence
- evidence should be a short direct quote or clear reference from the contract text
- impact should be plain English, not legalese
- Only include clauses that are actually problematic, not standard ones
- Be specific and accurate
"""

async def run_legal_agent(contract_text: str) -> LegalRiskOutput:
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": LEGAL_RISK_PROMPT},
                {"role": "user", "content": f"CONTRACT TEXT:\n\n{contract_text}"}
            ],
            temperature=0.1,
            max_tokens=1200,
            response_format={"type": "json_object"}
        )

        raw = response.choices[0].message.content
        data = json.loads(raw)

        clause_evidence = [
            ClauseEvidence(
                clause_name=item["clause_name"],
                evidence=item["evidence"],
                impact=item["impact"]
            )
            for item in data.get("clause_evidence", [])
        ]

        return LegalRiskOutput(
            risk_score=float(data["risk_score"]),
            risk_explanation=data["risk_explanation"],
            flagged_clauses=data["flagged_clauses"],
            clause_evidence=clause_evidence
        )

    except Exception:
        return LegalRiskOutput(
            risk_score=10.0,
            risk_explanation="Legal analysis failed. Manual review required.",
            flagged_clauses=["Unable to analyze — escalating for safety"],
            clause_evidence=[]
        )