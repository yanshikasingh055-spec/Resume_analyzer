import ScoreCard from "./ScoreCard";
import KeywordGap from "./KeywordGap";
import Suggestions from "./Suggestions";
import RoleFit from "./RoleFit";

export default function ResultsDashboard({ results, onReset }) {
  return (
    <div className="results-dashboard">
      <div className="results-header">
        <div>
          <h2>Analysis complete</h2>
          <p className="results-sub">Here's how your resume stacks up against the job</p>
        </div>
        <button className="reset-btn" onClick={onReset}>← Analyze another</button>
      </div>

      {/* Row 1: Score + Keywords */}
      <div className="results-grid">
        <ScoreCard
          score={results.match_score}
          breakdown={results.breakdown}
          resumeKeywords={results.resume_keyword_count}
          jdKeywords={results.jd_keyword_count}
          matchedCount={results.matched_keywords.length}
        />
        <KeywordGap
          matched={results.matched_keywords}
          missing={results.missing_keywords}
        />
      </div>

      {/* Row 2: Role Fit + Feedback */}
      <div className="results-grid-bottom">
        <RoleFit roleFit={results.role_fit} />
        <Suggestions feedback={results.feedback || results.suggestions} />
      </div>
    </div>
  );
}
