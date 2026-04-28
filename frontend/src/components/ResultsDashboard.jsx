import { useEffect, useState } from "react";

function barColor(val) {
  if (val >= 70) return "#1A9E6B";
  if (val >= 50) return "#C07C1A";
  return "#C0291A";
}
function fitLabel(val) {
  if (val >= 80) return "Great fit";
  if (val >= 60) return "Good fit";
  if (val >= 40) return "Partial fit";
  return "Low fit";
}
function scoreInfo(val) {
  if (val >= 75) return { label: "Strong match",   color: "#1A9E6B" };
  if (val >= 50) return { label: "Moderate match", color: "#C07C1A" };
  return             { label: "Needs work",       color: "#C0291A" };
}

function AnimatedBar({ value, color, delay = 0 }) {
  const [width, setWidth] = useState(0);
  useEffect(() => {
    const t = setTimeout(() => setWidth(value), delay);
    return () => clearTimeout(t);
  }, [value, delay]);
  return (
    <div style={{ height: 6, background: "#F0EFEB", borderRadius: 99, overflow: "hidden" }}>
      <div style={{
        height: "100%", borderRadius: 99,
        width: `${width}%`, background: color,
        transition: "width 1.2s cubic-bezier(0.16,1,0.3,1)"
      }} />
    </div>
  );
}

function ScoreRing({ score, color }) {
  const [animated, setAnimated] = useState(false);
  const circ = 301.6;
  const offset = animated ? circ - (score / 100) * circ : circ;
  useEffect(() => {
    const t = setTimeout(() => setAnimated(true), 150);
    return () => clearTimeout(t);
  }, []);
  return (
    <svg width="130" height="130" viewBox="0 0 130 130" style={{ display: "block", margin: "0 auto" }}>
      <circle cx="65" cy="65" r="48" fill="none" stroke="#E5E5E0" strokeWidth="9" />
      <circle cx="65" cy="65" r="48" fill="none"
        stroke={color} strokeWidth="9" strokeLinecap="round"
        strokeDasharray={circ} strokeDashoffset={offset}
        transform="rotate(-90 65 65)"
        style={{ transition: "stroke-dashoffset 1.3s cubic-bezier(0.16,1,0.3,1)" }}
      />
      <text x="65" y="59" textAnchor="middle" fontFamily="'DM Sans',sans-serif" fontSize="23" fontWeight="600" fill="#1A1917">
        {score}
      </text>
      <text x="65" y="77" textAnchor="middle" fontFamily="'DM Sans',sans-serif" fontSize="12" fill="#A09D96">
        out of 100
      </text>
    </svg>
  );
}

export default function ResultsDashboard({ results, onReset }) {
  const [activeTab, setActiveTab] = useState("matched");

  const matchScore = Number(results.match_score ?? results.matchScore ?? 0);
  const matched    = results.matched_keywords   ?? results.matchedKeywords  ?? [];
  const missing    = results.missing_keywords   ?? results.missingKeywords  ?? [];
  const partial    = results.partial_keywords   ?? results.partialKeywords  ?? [];
  const inJD       = results.jd_keyword_count   ?? results.keywords_in_jd   ?? 0;
  const inResume   = results.resume_keyword_count ?? results.keywords_in_resume ?? 0;
  const breakdown  = results.breakdown ?? {};
  const feedback   = results.feedback  ?? [];

  const roleFitRaw = results.role_fit ?? results.roleFit ?? {};
  const roleScores = roleFitRaw.role_scores ?? roleFitRaw ?? {};
  const roleFit = Object.entries(roleScores)
    .map(([role, score]) => ({ role, score: Number(score) }))
    .sort((a, b) => b.score - a.score);

  const breakdownRows = [
    { label: "Skills",     weight: "40%", value: Number(breakdown.skills     ?? 0) },
    { label: "Projects",   weight: "30%", value: Number(breakdown.projects   ?? 0) },
    { label: "Tools",      weight: "20%", value: Number(breakdown.tools      ?? 0) },
    { label: "Experience", weight: "10%", value: Number(breakdown.experience ?? 0) },
  ];

  const { label: scoreLabel, color: scoreColor } = scoreInfo(matchScore);

  const chipMap = { matched, missing, partial };
  const tabs = [
    { key: "missing", label: `Missing (${missing.length})` },
    { key: "partial", label: `Partial (${partial.length})` },
    { key: "matched", label: `Matched (${matched.length})` },
  ];
  const chipStyle = {
    matched: { background: "#E6F7F1", color: "#0D6E48", border: "1px solid #A3DFC5", dot: "#1A9E6B" },
    missing: { background: "#FEE9E7", color: "#C0291A", border: "1px solid #F5A49D", dot: "#C0291A" },
    partial: { background: "#FEF3E2", color: "#92400E", border: "1px solid #F5C878", dot: "#C07C1A" },
  };
  const tipStyle = {
    success: { background: "#E6F7F1", border: "1px solid #A3DFC5", color: "#0D6E48" },
    info:    { background: "#EEF2FF", border: "1px solid #C7D2FE", color: "#3730A3" },
    tip:     { background: "#EEF2FF", border: "1px solid #C7D2FE", color: "#3730A3" },
    warning: { background: "#FEF3E2", border: "1px solid #F5C878", color: "#92400E" },
    warn:    { background: "#FEF3E2", border: "1px solid #F5C878", color: "#92400E" },
    error:   { background: "#FEE9E7", border: "1px solid #F5A49D", color: "#C0291A" },
    neutral: { background: "#F0EFEB", border: "1px solid rgba(0,0,0,0.08)", color: "#6B6860" },
  };

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=DM+Mono:wght@500&display=swap');
        .rm-root * { box-sizing: border-box; }
        .rm-chip { transition: transform 0.1s; cursor: default; }
        .rm-chip:hover { transform: scale(1.04); }
        .rm-role { transition: border-color 0.15s, box-shadow 0.15s; }
        .rm-role:hover { border-color: rgba(0,0,0,0.2) !important; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }
        .rm-tab:hover  { background: #F0EFEB !important; }
        .rm-back:hover { background: #F0EFEB !important; }
        @keyframes rmUp { from { opacity:0; transform:translateY(12px); } to { opacity:1; transform:none; } }
        .rm-card { animation: rmUp 0.4s ease both; }
        @media (max-width: 860px) {
          .rm-top-grid  { grid-template-columns: 1fr !important; }
          .rm-bot-grid  { grid-template-columns: 1fr !important; }
          .rm-role-grid { grid-template-columns: 1fr !important; }
        }
      `}</style>

      <div className="rm-root" style={{ fontFamily: "'DM Sans',sans-serif", background: "#F4F3EF", minHeight: "100vh", color: "#1A1917" }}>

        {/* NAV */}
        <nav style={{ background: "#fff", borderBottom: "1px solid rgba(0,0,0,0.08)", padding: "0 2rem", height: 56, display: "flex", alignItems: "center", justifyContent: "space-between", position: "sticky", top: 0, zIndex: 100 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
            <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
              <div style={{ width: 28, height: 28, background: "#4338CA", borderRadius: 7, display: "flex", alignItems: "center", justifyContent: "center" }}>
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                  <rect x="2" y="2" width="7" height="9" rx="1.5" stroke="white" strokeWidth="1.4"/>
                  <path d="M4.5 6h4M4.5 8h2.5" stroke="white" strokeWidth="1.2" strokeLinecap="round"/>
                  <circle cx="11.5" cy="11.5" r="2.5" stroke="white" strokeWidth="1.3"/>
                  <path d="M13.5 13.5L15 15" stroke="white" strokeWidth="1.3" strokeLinecap="round"/>
                </svg>
              </div>
              <span style={{ fontSize: 17, fontWeight: 600, color: "#4338CA" }}>ResumeMatch</span>
            </div>
            <div style={{ width: 1, height: 20, background: "rgba(0,0,0,0.14)" }} />
            <span style={{ fontSize: 13, color: "#A09D96" }}>Know your match before you apply</span>
          </div>
          <button className="rm-back" onClick={onReset}
            style={{ fontSize: 13, fontWeight: 500, color: "#6B6860", background: "transparent", border: "1px solid rgba(0,0,0,0.14)", borderRadius: 99, padding: "6px 16px", cursor: "pointer", fontFamily: "'DM Sans',sans-serif", transition: "background 0.15s" }}>
            ← Analyze another
          </button>
        </nav>

        {/* PAGE */}
        <div style={{ maxWidth: 1080, margin: "0 auto", padding: "2rem 1.5rem 3rem" }}>

          <div style={{ marginBottom: "1.75rem" }}>
            <h1 style={{ fontSize: 26, fontWeight: 600, marginBottom: 4 }}>Analysis complete</h1>
            <p style={{ fontSize: 14, color: "#6B6860" }}>Here's how your resume stacks up against the job</p>
          </div>

          {/* TOP ROW */}
          <div className="rm-top-grid" style={{ display: "grid", gridTemplateColumns: "300px 1fr", gap: "1rem", marginBottom: "1rem" }}>

            {/* SCORE CARD */}
            <div className="rm-card" style={{ ...S.card, animationDelay: "0.05s" }}>
              <div style={S.cardLabel}>Match score</div>

              <ScoreRing score={matchScore} color={scoreColor} />

              <div style={{ textAlign: "center", fontSize: 13, fontWeight: 600, color: scoreColor, margin: "0.75rem 0 1.5rem", display: "flex", alignItems: "center", justifyContent: "center", gap: 5 }}>
                <span style={{ width: 7, height: 7, borderRadius: "50%", background: scoreColor, display: "inline-block" }} />
                {scoreLabel}
              </div>

              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 8, marginBottom: "1.5rem" }}>
                {[
                  ["Keywords matched", matched.length],
                  ["In job desc.",     inJD],
                  ["In resume",        inResume],
                ].map(([lbl, val]) => (
                  <div key={lbl} style={{ background: "#F0EFEB", borderRadius: 8, padding: "10px 6px", textAlign: "center" }}>
                    <div style={{ fontSize: 20, fontWeight: 600 }}>{val}</div>
                    <div style={{ fontSize: 10, color: "#A09D96", marginTop: 2, lineHeight: 1.3 }}>{lbl}</div>
                  </div>
                ))}
              </div>

              <div style={{ fontSize: 10, fontWeight: 600, letterSpacing: "0.08em", textTransform: "uppercase", color: "#A09D96", marginBottom: 12 }}>
                Score breakdown
              </div>

              {breakdownRows.map((row, i) => {
                const c = barColor(row.value);
                return (
                  <div key={row.label} style={{ marginBottom: 12 }}>
                    <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
                      <span style={{ fontSize: 13, color: "#6B6860" }}>
                        {row.label} <span style={{ color: "#A09D96" }}>({row.weight})</span>
                      </span>
                      <span style={{ fontSize: 13, fontWeight: 600, color: c, fontFamily: "'DM Mono',monospace" }}>
                        {row.value.toFixed(1)}%
                      </span>
                    </div>
                    <AnimatedBar value={row.value} color={c} delay={200 + i * 80} />
                  </div>
                );
              })}
            </div>

            {/* KEYWORD CARD */}
            <div className="rm-card" style={{ ...S.card, animationDelay: "0.12s" }}>
              <div style={S.cardLabel}>Keyword analysis</div>
              <div style={{ display: "flex", gap: 6, marginBottom: "1.25rem" }}>
                {tabs.map(tab => (
                  <button key={tab.key} className="rm-tab" onClick={() => setActiveTab(tab.key)}
                    style={{
                      fontSize: 12, fontWeight: 500, padding: "5px 13px", borderRadius: 99,
                      border: "1px solid", cursor: "pointer", fontFamily: "'DM Sans',sans-serif", transition: "all 0.15s",
                      background:  activeTab === tab.key ? "#4338CA" : "transparent",
                      color:       activeTab === tab.key ? "#fff"    : "#6B6860",
                      borderColor: activeTab === tab.key ? "#4338CA" : "rgba(0,0,0,0.14)",
                    }}>
                    {tab.label}
                  </button>
                ))}
              </div>
              <div style={{ display: "flex", flexWrap: "wrap", gap: 7 }}>
                {chipMap[activeTab].length === 0
                  ? <p style={{ fontSize: 13, color: "#A09D96" }}>No keywords in this category.</p>
                  : chipMap[activeTab].map(kw => {
                      const cs = chipStyle[activeTab];
                      return (
                        <div key={kw} className="rm-chip"
                          style={{ fontSize: 12, fontWeight: 500, padding: "5px 11px", borderRadius: 99, display: "flex", alignItems: "center", gap: 5, background: cs.background, color: cs.color, border: cs.border }}>
                          <span style={{ width: 6, height: 6, borderRadius: "50%", background: cs.dot, flexShrink: 0 }} />
                          {kw}
                        </div>
                      );
                    })
                }
              </div>
            </div>
          </div>

          {/* BOTTOM ROW */}
          <div className="rm-bot-grid" style={{ display: "grid", gridTemplateColumns: "1fr 280px", gap: "1rem" }}>

            {/* ROLE FIT */}
            <div className="rm-card" style={{ ...S.card, animationDelay: "0.18s" }}>
              <div style={S.cardLabel}>Role fit</div>
              <div className="rm-role-grid" style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
                {roleFit.map((r, i) => {
                  const isBest = i === 0;
                  const c = barColor(r.score);
                  return (
                    <div key={r.role} className="rm-role"
                      style={{ border: isBest ? "1.5px solid #4338CA" : "1px solid rgba(0,0,0,0.08)", borderRadius: 10, padding: "1rem", background: isBest ? "#FAFAFE" : "#fff" }}>
                      {isBest && (
                        <span style={{ display: "inline-block", fontSize: 10, fontWeight: 600, letterSpacing: "0.05em", textTransform: "uppercase", background: "#EEF2FF", color: "#4338CA", borderRadius: 99, padding: "2px 9px", marginBottom: 8 }}>
                          Best fit
                        </span>
                      )}
                      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 6 }}>
                        <div style={{ fontSize: 13, fontWeight: 600, lineHeight: 1.3, maxWidth: 130 }}>{r.role}</div>
                        <div style={{ fontSize: 14, fontWeight: 600, color: c, fontFamily: "'DM Mono',monospace" }}>{r.score.toFixed(1)}%</div>
                      </div>
                      <AnimatedBar value={r.score} color={c} delay={300 + i * 60} />
                      <div style={{ fontSize: 11, fontWeight: 500, color: c, marginTop: 5 }}>{fitLabel(r.score)}</div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* RECOMMENDATIONS */}
            <div className="rm-card" style={{ ...S.card, animationDelay: "0.22s" }}>
              <div style={S.cardLabel}>Recommendations</div>
              <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                {feedback.length === 0
                  ? <p style={{ fontSize: 13, color: "#A09D96" }}>No recommendations available.</p>
                  : feedback.map((f, i) => {
                      const ts = tipStyle[f.type] || tipStyle.neutral;
                      return (
                        <div key={i} style={{ borderRadius: 8, padding: "13px 15px", fontSize: 13, lineHeight: 1.55, ...ts }}>
                          {f.head && (
                            <div style={{ fontSize: 11, fontWeight: 700, letterSpacing: "0.06em", textTransform: "uppercase", marginBottom: 4, opacity: 0.75 }}>
                              {f.head}
                            </div>
                          )}
                          {f.text}
                        </div>
                      );
                    })
                }
              </div>
            </div>

          </div>
        </div>

        <footer style={{ textAlign: "center", padding: "24px", color: "#A09D96", fontSize: 13 }}>
          Built with Python · Flask · spaCy · React
        </footer>
      </div>
    </>
  );
}

const S = {
  card:      { background: "#fff", border: "1px solid rgba(0,0,0,0.08)", borderRadius: 14, padding: "1.5rem" },
  cardLabel: { fontSize: 10, fontWeight: 600, letterSpacing: "0.09em", textTransform: "uppercase", color: "#A09D96", marginBottom: "1.25rem" },
};