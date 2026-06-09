# ContractShield AI 🛡️
### AI Contract Copilot for Startup Founders

ContractShield AI is a multi-agent AI platform that analyzes contracts in seconds — identifying legal risks, checking compliance, explaining business impact in plain English, and recommending negotiation strategies. Built for startup founders who sign contracts without legal expertise.

---

## 🎯 Problem

Startup founders sign vendor agreements, SaaS contracts, and partnership deals without legal expertise. Hidden clauses — unlimited liability, auto-renewal traps, one-sided termination — can destroy a startup financially before it even scales.

**ContractShield AI solves this in seconds.**

---

## ⚡ Live Demo

> Paste any contract → Get a full risk report in under 10 seconds

---

## 🤖 How It Works

Four AI agents run concurrently using `asyncio.gather()`:

| Agent | Role | Output |
|-------|------|--------|
| Legal Risk Agent | Detects dangerous clauses | Risk score 0–10 + flagged clauses |
| Compliance Agent | Checks GDPR, data handling | Authorized / Not Authorized |
| Business Impact Agent | Translates findings to plain English | Key business concerns |
| Negotiation Agent | Suggests safer alternatives | Actionable negotiation moves |

A deterministic **Decision Engine** then routes the contract to one of three states:
- ✅ `APPROVED` — Safe to proceed
- ⚠️ `REVIEW RECOMMENDED` — Moderate risk, review before signing
- 🚨 `HIGH RISK ESCALATED` — Dangerous clauses, do not sign

---

## 🏗️ Architecture

```
Contract Upload
       │
       ▼
Input Validation (Pydantic)
       │
       ▼
Concurrent Multi-Agent Analysis (asyncio.gather)
       ├── Legal Risk Agent (Groq)
       └── Compliance Agent (Groq)
       │
       ▼
Sequential Agents (using Phase 1 findings)
       ├── Business Impact Agent (Groq)
       └── Negotiation Agent (Groq)
       │
       ▼
Decision Engine
       │
       ▼
MySQL Logging (Background Task)
       │
       ▼
Founder Dashboard
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React + Vite + Tailwind CSS |
| Backend | FastAPI + Python |
| AI | Groq API (llama-3.3-70b-versatile) |
| Database | MySQL |
| Concurrency | asyncio.gather() |
| Validation | Pydantic |
| Background Tasks | FastAPI BackgroundTasks |

---

## 🚀 Running Locally

### Backend
```bash
git clone https://github.com/techAsmita/contractshield-ai.git
cd contractshield-ai
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
```

Create `backend/.env`:
```
GROQ_API_KEY=your_groq_api_key
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=contractshield
```

```bash
uvicorn backend.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 📊 Error Handling

| Scenario | Response |
|----------|----------|
| Invalid input | 422 Unprocessable Entity |
| AI API failure | Retry 3x with exponential backoff → 503 |
| Parsing failure | Safe default: risk=10, authorized=false |
| Database failure | Transaction rollback → 500 |

---

## 👩‍💻 Built By

**Asmani Roy** — Computer Engineering, Thapar Institute of Engineering & Technology  
GitHub: [@techAsmita](https://github.com/techAsmita) | LinkedIn: [techasmita](https://linkedin.com/in/techasmita)

---

*Built for FlowZint AI Hackathon 2026 — Open Innovation Track*