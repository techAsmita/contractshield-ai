from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class ContractStatus(str, Enum):
    APPROVED = "APPROVED"
    REVIEW_RECOMMENDED = "REVIEW_RECOMMENDED"
    HIGH_RISK_ESCALATED = "HIGH_RISK_ESCALATED"


class ContractInput(BaseModel):
    contract_text: str = Field(..., min_length=50, description="Raw contract text to analyze")
    founder_name: Optional[str] = Field(None, description="Name of the founder submitting")
    contract_title: str = Field(..., min_length=1, description="Title or name of the contract")


class ClauseEvidence(BaseModel):
    clause_name: str
    evidence: str
    impact: str


class LegalRiskOutput(BaseModel):
    risk_score: float = Field(..., ge=0, le=10)
    risk_explanation: str
    flagged_clauses: list[str]
    clause_evidence: list[ClauseEvidence]


class ComplianceOutput(BaseModel):
    is_authorized: bool
    compliance_findings: str
    violation_list: list[str]


class BusinessImpactOutput(BaseModel):
    impact_summary: str
    key_concerns: list[str]


class NegotiationOutput(BaseModel):
    suggestions: list[str]
    safer_alternatives: list[str]


class ContractAnalysisResult(BaseModel):
    contract_title: Optional[str]
    founder_name: Optional[str]
    legal_risk: LegalRiskOutput
    compliance: ComplianceOutput
    business_impact: BusinessImpactOutput
    negotiation: NegotiationOutput
    final_status: ContractStatus
    decision_reason: str