import { useState } from "react";

const StatusBadge = ({ status }) => {
  const styles = {
    APPROVED: "bg-green-500/20 text-green-400 border border-green-500/30",
    REVIEW_RECOMMENDED: "bg-yellow-500/20 text-yellow-400 border border-yellow-500/30",
    HIGH_RISK_ESCALATED: "bg-red-500/20 text-red-400 border border-red-500/30",
  };
  const labels = {
    APPROVED: "✅ Approved",
    REVIEW_RECOMMENDED: "⚠️ Review Recommended",
    HIGH_RISK_ESCALATED: "🚨 High Risk — Escalated",
  };
  return (
    <span className={`px-4 py-2 rounded-full text-sm font-semibold ${styles[status]}`}>
      {labels[status]}
    </span>
  );
};

const RiskMeter = ({ score }) => {
  const color = score >= 7 ? "bg-red-500" : score >= 4 ? "bg-yellow-500" : "bg-green-500";
  return (
    <div className="w-full">
      <div className="flex justify-between mb-2">
        <span className="text-slate-400 text-sm">Risk Score</span>
        <span className="text-white font-bold text-lg">{score} / 10</span>
      </div>
      <div className="w-full bg-slate-700 rounded-full h-3">
        <div
          className={`h-3 rounded-full transition-all duration-1000 ${color}`}
          style={{ width: `${score * 10}%` }}
        />
      </div>
    </div>
  );
};

const Card = ({ title, children }) => (
  <div className="bg-slate-800/60 border border-slate-700/50 rounded-2xl p-6">
    <h3 className="text-slate-300 font-semibold text-sm uppercase tracking-wider mb-4">{title}</h3>
    {children}
  </div>
);

export default function App() {
  const [contractText, setContractText] = useState("");
  const [founderName, setFounderName] = useState("");
  const [contractTitle, setContractTitle] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const analyze = async () => {
    if (!contractTitle.trim()) {
      setError("Please enter a contract title.");
      return;
    }
    if (contractText.trim().length < 50) {
      setError("Please enter at least 50 characters of contract text.");
      return;
    }
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/v1/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contract_text: contractText,
          founder_name: founderName || null,
          contract_title: contractTitle,
        }),
      });

      if (!response.ok) throw new Error("Analysis failed. Please try again.");
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white">
      {/* Header */}
      <div className="border-b border-slate-800 px-6 py-4 flex items-center gap-3">
        <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center text-sm font-bold">CS</div>
        <span className="font-semibold text-lg">ContractShield AI</span>
        <span className="text-slate-500 text-sm ml-2">AI Contract Copilot for Startup Founders</span>
      </div>

      <div className="max-w-5xl mx-auto px-6 py-10">
        {/* Input Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Analyze Your Contract</h1>
          <p className="text-slate-400">Paste your contract below. Our AI agents will identify risks, check compliance, and suggest improvements in seconds.</p>
        </div>

        <div className="grid grid-cols-2 gap-4 mb-4">
          <input
            className="bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-blue-500"
            placeholder="Your name (optional)"
            value={founderName}
            onChange={e => setFounderName(e.target.value)}
          />
          <input
            className="bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-blue-500"
            placeholder="Contract title *"
            value={contractTitle}
            onChange={e => setContractTitle(e.target.value)}
          />
        </div>

        <textarea
          className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 resize-none mb-4"
          rows={8}
          placeholder="Paste your contract text here..."
          value={contractText}
          onChange={e => setContractText(e.target.value)}
        />

        {error && <p className="text-red-400 text-sm mb-4">{error}</p>}

        <button
          onClick={analyze}
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-500 disabled:bg-slate-700 disabled:text-slate-500 text-white font-semibold py-4 rounded-xl transition-all duration-200 text-lg"
        >
          {loading ? "Analyzing contract — all agents running..." : "Analyze Contract"}
        </button>

        {/* Results */}
        {result && (
          <div className="mt-10 space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold">{result.contract_title || "Contract Analysis"}</h2>
                {result.founder_name && <p className="text-slate-400 text-sm mt-1">Submitted by {result.founder_name}</p>}
              </div>
              <StatusBadge status={result.final_status} />
            </div>

            {/* Decision Reason */}
            <div className="bg-slate-800/60 border border-slate-700/50 rounded-2xl p-6">
              <p className="text-slate-300">{result.decision_reason}</p>
            </div>

            {/* Risk + Compliance Row */}
            <div className="grid grid-cols-2 gap-4">
              <Card title="Legal Risk Analysis">
                <RiskMeter score={result.legal_risk.risk_score} />
                <p className="text-slate-400 text-sm mt-4">{result.legal_risk.risk_explanation}</p>
                <div className="mt-4 flex flex-wrap gap-2">
                  {result.legal_risk.flagged_clauses.map((clause, i) => (
                    <span key={i} className="bg-red-500/10 text-red-400 border border-red-500/20 px-3 py-1 rounded-full text-xs">{clause}</span>
                  ))}
                </div>
              </Card>

              <Card title="Compliance Status">
                <div className={`text-2xl font-bold mb-3 ${result.compliance.is_authorized ? "text-green-400" : "text-red-400"}`}>
                  {result.compliance.is_authorized ? "✅ Authorized" : "❌ Not Authorized"}
                </div>
                <p className="text-slate-400 text-sm">{result.compliance.compliance_findings}</p>
                <div className="mt-4 flex flex-wrap gap-2">
                  {result.compliance.violation_list.map((v, i) => (
                    <span key={i} className="bg-orange-500/10 text-orange-400 border border-orange-500/20 px-3 py-1 rounded-full text-xs">{v}</span>
                  ))}
                </div>
              </Card>
            </div>

            {/* Clause Evidence */}
            {result.legal_risk.clause_evidence && result.legal_risk.clause_evidence.length > 0 && (
              <Card title="Clause Evidence">
                <div className="space-y-4">
                  {result.legal_risk.clause_evidence.map((item, i) => (
                    <div key={i} className="bg-slate-700/30 rounded-xl p-4 border border-slate-600/30">
                      <div className="flex items-center gap-2 mb-2">
                        <span className="bg-red-500/20 text-red-400 border border-red-500/20 px-2 py-0.5 rounded text-xs font-semibold">{item.clause_name}</span>
                      </div>
                      <div className="mb-2">
                        <span className="text-slate-500 text-xs uppercase tracking-wider">Evidence</span>
                        <p className="text-slate-300 text-sm mt-1 italic border-l-2 border-slate-600 pl-3">"{item.evidence}"</p>
                      </div>
                      <div>
                        <span className="text-slate-500 text-xs uppercase tracking-wider">Impact</span>
                        <p className="text-yellow-400 text-sm mt-1">{item.impact}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </Card>
            )}

            {/* Business Impact */}
            <Card title="Business Impact">
              <p className="text-slate-300 mb-4">{result.business_impact.impact_summary}</p>
              <div className="space-y-2">
                {result.business_impact.key_concerns.map((concern, i) => (
                  <div key={i} className="flex items-start gap-3 bg-slate-700/30 rounded-xl px-4 py-3">
                    <span className="text-yellow-400 mt-0.5">⚠️</span>
                    <span className="text-slate-300 text-sm">{concern}</span>
                  </div>
                ))}
              </div>
            </Card>

            {/* Negotiation */}
            <div className="grid grid-cols-2 gap-4">
              <Card title="Negotiation Suggestions">
                <div className="space-y-2">
                  {result.negotiation.suggestions.map((s, i) => (
                    <div key={i} className="flex items-start gap-3 bg-slate-700/30 rounded-xl px-4 py-3">
                      <span className="text-blue-400 mt-0.5">→</span>
                      <span className="text-slate-300 text-sm">{s}</span>
                    </div>
                  ))}
                </div>
              </Card>

              <Card title="Safer Alternatives">
                <div className="space-y-2">
                  {result.negotiation.safer_alternatives.map((a, i) => (
                    <div key={i} className="flex items-start gap-3 bg-slate-700/30 rounded-xl px-4 py-3">
                      <span className="text-green-400 mt-0.5">✓</span>
                      <span className="text-slate-300 text-sm">{a}</span>
                    </div>
                  ))}
                </div>
              </Card>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}