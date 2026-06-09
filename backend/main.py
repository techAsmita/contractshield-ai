import asyncio
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from dotenv import load_dotenv

from backend.core.models import ContractInput, ContractAnalysisResult
from backend.core.decision_engine import run_decision_engine
from backend.core.database import log_analysis
from backend.agents.legal_agent import run_legal_agent
from backend.agents.compliance_agent import run_compliance_agent
from backend.agents.business_impact_agent import run_business_impact_agent
from backend.agents.negotiation_agent import run_negotiation_agent

load_dotenv()

app = FastAPI(
    title="ContractShield AI",
    description="AI Contract Copilot for Startup Founders",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "ContractShield AI is live"}


@app.post("/api/v1/analyze", response_model=ContractAnalysisResult)
async def analyze_contract(payload: ContractInput, background_tasks: BackgroundTasks):

    # Phase 1: Run Legal and Compliance agents concurrently
    legal_result, compliance_result = await asyncio.gather(
        run_legal_agent(payload.contract_text),
        run_compliance_agent(payload.contract_text)
    )

    # Phase 2: Run Business Impact and Negotiation agents concurrently
    business_result, negotiation_result = await asyncio.gather(
        run_business_impact_agent(
            payload.contract_text,
            legal_result.risk_explanation,
            compliance_result.compliance_findings
        ),
        run_negotiation_agent(
            payload.contract_text,
            legal_result.risk_explanation,
            compliance_result.compliance_findings
        )
    )

    # Phase 3: Decision engine
    final_status, decision_reason = run_decision_engine(legal_result, compliance_result)

    # Phase 4: Build result
    result = ContractAnalysisResult(
        contract_title=payload.contract_title,
        founder_name=payload.founder_name,
        legal_risk=legal_result,
        compliance=compliance_result,
        business_impact=business_result,
        negotiation=negotiation_result,
        final_status=final_status,
        decision_reason=decision_reason
    )

    # Phase 5: Log to MySQL in background (non-blocking)
    background_tasks.add_task(log_analysis, result)

    return result