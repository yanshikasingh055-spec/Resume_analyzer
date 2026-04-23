import { useEffect, useState } from "react";

function getScoreColor(score) {
  if (score >= 75) return "#22c55e";
  if (score >= 50) return "#f59e0b";
  return "#ef4444";
}

function getScoreLabel(score) {
  if (score >= 85) return "Excellent match";
  if (score >= 75) return "Strong match";
  if (score >= 55) return "Moderate match";
  if (score >= 35) return "Weak match";
  return "Low match";
}

function SectionBar({ label, value, color }) {
  const [animated, setAnimated] = useState(0);
  useEffect(() => {
    const t = setTimeout(() => setAnimated(value), 100);
    return () => clearTimeout(t);
  }, [value]);

  return (
    <div className="section-bar">
      <div className="section-bar-header">
        <span className="section-bar-label">{label}</span>
        <span className="section-bar-value" style={{ color }}>{value}%</span>
      </div>
      <div className="section-bar-track">
        <div
          className="section-bar-fill"
          style={{
            width: `${animated}%`,
            background: color,
            transition: "width 0.8s cubic-bezier(0.4,0,0.2,1)",
          }}
        />
      </div>
    </div>
  );
}

export default function ScoreCard({ score, breakdown, resumeKeywords, jdKeywords, matchedCount }) {
  const [animatedScore, setAnimatedScore] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setAnimatedScore((prev) => {
        if (prev >= score) { clearInterval(timer); return score; }
        return Math.min(prev + 2, score);
      });
    }, 20);
    return () => clearInterval(timer);
  }, [score]);

  const color = getScoreColor(score);
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (animatedScore / 100) * circumference;

  const sections = breakdown ? [
    { label: "Skills match", value: breakdown.skills, weight: "40%" },
    { label: "Projects match", value: breakdown.projects, weight: "30%" },
    { label: "Tools match", value: breakdown.tools, weight: "20%" },
    { label: "Experience match", value: breakdown.experience, weight: "10%" },
  ] : [];

  return (
    <div className="card score-card">
      <h3 className="card-title">Match Score</h3>

      <div className="score-circle-wrap">
        <svg width="140" height="140" viewBox="0 0 140 140">
          <circle cx="70" cy="70" r={radius} fill="none" stroke="#e5e7eb" strokeWidth="10" />
          <circle
            cx="70" cy="70" r={radius}
            fill="none" stroke={color} strokeWidth="10"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            transform="rotate(-90 70 70)"
            style={{ transition: "stroke-dashoffset 0.05s linear" }}
          />
          <text x="70" y="64" textAnchor="middle" dominantBaseline="central"
            fontSize="28" fontWeight="700" fill={color}>{animatedScore}</text>
          <text x="70" y="88" textAnchor="middle" fontSize="12" fill="#9ca3af">out of 100</text>
        </svg>
        <div className="score-label" style={{ color }}>{getScoreLabel(score)}</div>
      </div>

      <div className="score-stats">
        <div className="stat">
          <span className="stat-value">{matchedCount}</span>
          <span className="stat-label">Keywords matched</span>
        </div>
        <div className="stat-divider" />
        <div className="stat">
          <span className="stat-value">{jdKeywords}</span>
          <span className="stat-label">In job description</span>
        </div>
        <div className="stat-divider" />
        <div className="stat">
          <span className="stat-value">{resumeKeywords}</span>
          <span className="stat-label">In your resume</span>
        </div>
      </div>

      {sections.length > 0 && (
        <div className="breakdown-section">
          <p className="breakdown-title">Score breakdown</p>
          {sections.map((s) => (
            <SectionBar
              key={s.label}
              label={`${s.label} (${s.weight})`}
              value={s.value}
              color={getScoreColor(s.value)}
            />
          ))}
        </div>
      )}
    </div>
  );
}
