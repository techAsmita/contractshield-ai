import aiomysql
import os
import json
from dotenv import load_dotenv

load_dotenv()

async def get_connection():
    return await aiomysql.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        db=os.getenv("MYSQL_DB", "contractshield"),
        autocommit=True
    )

async def log_analysis(result):
    conn = None
    try:
        conn = await get_connection()
        async with conn.cursor() as cursor:
            await cursor.execute("""
                INSERT INTO contract_analyses (
                    contract_title,
                    founder_name,
                    risk_score,
                    is_authorized,
                    final_status,
                    decision_reason,
                    flagged_clauses,
                    violation_list,
                    business_impact_summary,
                    negotiation_suggestions
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                result.contract_title,
                result.founder_name,
                result.legal_risk.risk_score,
                result.compliance.is_authorized,
                result.final_status.value,
                result.decision_reason,
                json.dumps(result.legal_risk.flagged_clauses),
                json.dumps(result.compliance.violation_list),
                result.business_impact.impact_summary,
                json.dumps(result.negotiation.suggestions)
            ))
    except Exception as e:
        print(f"Database logging failed: {e}")
    finally:
        if conn:
            conn.close()