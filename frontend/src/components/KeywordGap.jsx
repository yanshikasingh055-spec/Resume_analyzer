import { useState } from "react";

export default function KeywordGap({ matched, missing, partial = [] }) {
  const [activeTab, setActiveTab] = useState("missing");

  const tabs = [
    { key: "missing", label: `Missing (${missing.length})`, color: "#ef4444" },
    { key: "partial", label: `Partial (${partial.length})`, color: "#f59e0b" },
    { key: "matched", label: `Matched (${matched.length})`, color: "#22c55e" },
  ];

  return (
    <div className="card keyword-card">
      <h3 className="card-title">Keyword Analysis</h3>

      <div className="tab-row">
        {tabs.map((t) => (
          <button
            key={t.key}
            className={`tab-btn ${activeTab === t.key ? "active" : ""}`}
            style={activeTab === t.key ? { background: t.color, borderColor: t.color } : {}}
            onClick={() => setActiveTab(t.key)}
          >
            {t.label}
          </button>
        ))}
      </div>

      <div className="keyword-list">
        {activeTab === "missing" && (
          missing.length > 0
            ? missing.map((kw, i) => (
                <span key={i} className="keyword-tag missing">🔴 {kw}</span>
              ))
            : <p className="empty-state">✅ No missing keywords! Great job.</p>
        )}

        {activeTab === "partial" && (
          partial.length > 0
            ? partial.map((kw, i) => (
                <span key={i} className="keyword-tag partial">🟡 {kw}</span>
              ))
            : <p className="empty-state">No partially matched keywords.</p>
        )}

        {activeTab === "matched" && (
          matched.length > 0
            ? matched.map((kw, i) => (
                <span key={i} className="keyword-tag matched">🟢 {kw}</span>
              ))
            : <p className="empty-state">No keyword matches found yet.</p>
        )}
      </div>

      {activeTab === "missing" && missing.length > 0 && (
        <p className="keyword-tip">
          💡 Add these to your Skills section or weave them naturally into project descriptions.
        </p>
      )}
      {activeTab === "partial" && partial.length > 0 && (
        <p className="keyword-tip">
          🟡 These are partially matched — consider using the exact terms from the job description.
        </p>
      )}
    </div>
  );
}
