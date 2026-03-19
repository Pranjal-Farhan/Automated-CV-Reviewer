import { GraduationCap } from "lucide-react";

export default function EducationCard({ data }) {
  if (!data) return null;

  if (typeof data === "string") {
    return (
      <div className="result-card">
        <div className="result-card__header">
          <div className="result-card__icon result-card__icon--education">
            <GraduationCap size={24} />
          </div>
          <h3 className="result-card__title">Education</h3>
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
        <div className="result-card__icon result-card__icon--education">
          <GraduationCap size={24} />
        </div>
        <h3 className="result-card__title">Education</h3>
      </div>
      <div className="result-card__body">
        {data.map((item, i) => (
          <div className="timeline-item" key={i}>
            <div className="timeline-item__title">
              {item.degree || item.title || item.qualification || "Degree"}
            </div>
            {(item.institution || item.school || item.university) && (
              <div className="timeline-item__subtitle">
                {item.institution || item.school || item.university}
              </div>
            )}
            {(item.dates || item.date || item.year || item.period) && (
              <div className="timeline-item__date">
                {item.dates || item.date || item.year || item.period}
              </div>
            )}
            {(item.details || item.description || item.gpa) && (
              <div className="timeline-item__desc">
                {item.details ||
                  item.description ||
                  (item.gpa ? `GPA: ${item.gpa}` : "")}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
