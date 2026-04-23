const TYPE_CONFIG = {
  success: { icon: "✅", bg: "#f0fdf4", border: "#bbf7d0", color: "#15803d" },
  error:   { icon: "❌", bg: "#fef2f2", border: "#fecaca", color: "#b91c1c" },
  warning: { icon: "⚠️", bg: "#fffbeb", border: "#fde68a", color: "#92400e" },
  info:    { icon: "💡", bg: "#eff6ff", border: "#bfdbfe", color: "#1e40af" },
};

export default function Suggestions({ feedback }) {
  // Support both old string array and new typed feedback array
  const items = Array.isArray(feedback)
    ? feedback.map((f) =>
        typeof f === "string" ? { type: "info", text: f } : f
      )
    : [];

  return (
    <div className="card suggestions-card">
      <h3 className="card-title">Recruiter Feedback</h3>
      <div className="feedback-list">
        {items.map((item, i) => {
          const cfg = TYPE_CONFIG[item.type] || TYPE_CONFIG.info;
          return (
            <div
              key={i}
              className="feedback-item"
              style={{ background: cfg.bg, border: `1px solid ${cfg.border}` }}
            >
              <span className="feedback-icon">{cfg.icon}</span>
              <p className="feedback-text" style={{ color: cfg.color }}>{item.text}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
