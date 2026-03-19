import { UserCircle } from "lucide-react";

export default function CandidateCard({ data }) {
  if (!data || typeof data !== "object") return null;

  // data might have: name, email, phone, location, linkedin, summary, etc.
  const fields = Object.entries(data).filter(
    ([, val]) => val && typeof val !== "object"
  );

  if (fields.length === 0) return null;

  return (
    <div className="result-card result-card--candidate">
      <div className="result-card__header">
        <div className="result-card__icon result-card__icon--candidate">
          <UserCircle size={24} />
        </div>
        <h3 className="result-card__title">Candidate Information</h3>
      </div>
      <div className="result-card__body">
        <div className="candidate-grid">
          {fields.map(([key, value]) => (
            <div className="candidate-field" key={key}>
              <span className="candidate-field__label">
                {key.replace(/_/g, " ")}
              </span>
              <span className="candidate-field__value">{String(value)}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
