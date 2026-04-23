function getRoleBar(score) {
  if (score >= 70) return { color: "#22c55e", label: "Great fit" };
  if (score >= 45) return { color: "#f59e0b", label: "Partial fit" };
  return { color: "#ef4444", label: "Low fit" };
}

export default function RoleFit({ roleFit }) {
  if (!roleFit || !roleFit.role_scores) return null;

  const { role_scores, best_fit_roles } = roleFit;
  const sorted = Object.entries(role_scores).sort((a, b) => b[1] - a[1]);

  return (
    <div className="card role-fit-card">
      <h3 className="card-title">🧠 Role Fit Insight</h3>

      <div className="role-best-fit">
        <p className="role-best-label">You are best suited for:</p>
        <div className="role-best-tags">
          {best_fit_roles.length > 0
            ? best_fit_roles.map((role) => (
                <span key={role} className="role-tag good">✔ {role}</span>
              ))
            : <span className="role-tag neutral">Analyzing profile…</span>}
        </div>
      </div>

      <div className="role-bars">
        {sorted.map(([role, score]) => {
          const { color, label } = getRoleBar(score);
          const isBest = best_fit_roles.includes(role);
          return (
            <div key={role} className={`role-bar-row ${isBest ? "role-highlight" : ""}`}>
              <div className="role-bar-header">
                <span className="role-bar-name">{role}</span>
                <span className="role-bar-pct" style={{ color }}>{score}%</span>
              </div>
              <div className="role-bar-track">
                <div
                  className="role-bar-fill"
                  style={{ width: `${score}%`, background: color }}
                />
              </div>
              <span className="role-bar-label" style={{ color }}>{label}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
