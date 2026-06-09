from backend.core.models import (
    LegalRiskOutput,
    ComplianceOutput,
    ContractStatus
)


def run_decision_engine(
    legal: LegalRiskOutput,
    compliance: ComplianceOutput
) -> tuple[ContractStatus, str]:
    
    high_risk = legal.risk_score >= 7
    not_authorized = not compliance.is_authorized

    if high_risk and not_authorized:
        status = ContractStatus.HIGH_RISK_ESCALATED
        reason = (
            f"Contract flagged on both legal and compliance grounds. "
            f"Legal risk score is {legal.risk_score}/10 and compliance authorization failed. "
            f"Immediate escalation required before signing."
        )

    elif high_risk:
        status = ContractStatus.HIGH_RISK_ESCALATED
        reason = (
            f"Contract flagged due to high legal risk score of {legal.risk_score}/10. "
            f"Dangerous clauses detected that require legal review before signing."
        )

    elif not_authorized:
        status = ContractStatus.HIGH_RISK_ESCALATED
        reason = (
            f"Contract failed compliance authorization. "
            f"Regulatory violations detected that must be resolved before signing."
        )

    elif legal.risk_score >= 4:
        status = ContractStatus.REVIEW_RECOMMENDED
        reason = (
            f"Contract has a moderate legal risk score of {legal.risk_score}/10. "
            f"No critical violations found but review is recommended before signing."
        )

    else:
        status = ContractStatus.APPROVED
        reason = (
            f"Contract passed legal and compliance checks. "
            f"Legal risk score is {legal.risk_score}/10 with no major violations found. "
            f"Relatively safe to proceed."
        )

    return status, reason