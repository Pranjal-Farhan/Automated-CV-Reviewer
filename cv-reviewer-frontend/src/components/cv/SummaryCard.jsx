import { Info } from "lucide-react";

export default function SummaryCard({ summary, recommendations, score }) {
  if (!summary && !recommendations) return null;

  return (
    <div className="result-card">
      <div className="result-card__header">
        <div className="result-card__icon result-card__icon--summary">
          <Info size={24} />
        </div>
        <h3 className="result-card__title">Summary &amp; Recommendations</h3>
      </div>
      <div className="result-card__body">
        {score !== undefined && score !== null && (
          <div className="score-badge">
            <span className="score-badge__label">Overall Score</span>
            <span className="score-badge__value">{score}/10</span>
          </div>
        )}

        {summary && <p className="summary-text">{summary}</p>}

        {recommendations &&
          Array.isArray(recommendations) &&
          recommendations.length > 0 && (
            <>
              <h4 className="recommendations-title">Recommendations</h4>
              <ul className="recommendation-list">
                {recommendations.map((rec, i) => (
                  <li key={i}>{rec}</li>
                ))}
              </ul>
            </>
          )}

        {recommendations && typeof recommendations === "string" && (
          <p className="summary-text">{recommendations}</p>
        )}
      </div>
    </div>
  );
}
