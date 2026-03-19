import { Briefcase } from "lucide-react";

export default function ExperienceCard({ data }) {
  if (!data) return null;

  // data can be:
  // - an array of objects: [{ title, company, dates, description }, ...]
  // - a string

  if (typeof data === "string") {
    return (
      <div className="result-card">
        <div className="result-card__header">
          <div className="result-card__icon result-card__icon--experience">
            <Briefcase size={24} />
          </div>
          <h3 className="result-card__title">Experience</h3>
        </div>
        <div className="result-card__body">
          <p className="summary-text">{data}</p>
        </div>
      </div>
    );
  }

  if (!Array.isArray(data) || data.length === 0) return null;

  return (
    <div className="result-card">
      <div className="result-card__header">
        <div className="result-card__icon result-card__icon--experience">
          <Briefcase size={24} />
        </div>
        <h3 className="result-card__title">Experience</h3>
      </div>
      <div className="result-card__body">
        {data.map((item, i) => (
          <div className="timeline-item" key={i}>
            <div className="timeline-item__title">
              {item.title || item.role || item.position || "Position"}
            </div>
            {(item.company || item.organization) && (
              <div className="timeline-item__subtitle">
                {item.company || item.organization}
              </div>
            )}
            {(item.dates || item.date || item.period || item.duration) && (
              <div className="timeline-item__date">
                {item.dates || item.date || item.period || item.duration}
              </div>
            )}
            {(item.description || item.details || item.summary) && (
              <div className="timeline-item__desc">
                {item.description || item.details || item.summary}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
