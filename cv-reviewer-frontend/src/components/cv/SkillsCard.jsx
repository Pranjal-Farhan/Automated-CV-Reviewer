import { Star } from "lucide-react";

export default function SkillsCard({ data }) {
  if (!data) return null;

  // data can be:
  // - an array of strings: ["Python", "React"]
  // - an object: { technical: [...], soft: [...], languages: [...], tools: [...] }

  const isArray = Array.isArray(data);

  if (isArray && data.length === 0) return null;
  if (!isArray && typeof data === "object" && Object.keys(data).length === 0)
    return null;

  return (
    <div className="result-card">
      <div className="result-card__header">
        <div className="result-card__icon result-card__icon--skills">
          <Star size={24} />
        </div>
        <h3 className="result-card__title">Skills</h3>
      </div>
      <div className="result-card__body">
        {isArray ? (
          <div className="skills-tags">
            {data.map((skill, i) => (
              <span className="skill-tag" key={i}>
                {skill}
              </span>
            ))}
          </div>
        ) : (
          Object.entries(data).map(([category, skills]) => {
            if (!Array.isArray(skills) || skills.length === 0) return null;
            const tagClass =
              category.toLowerCase() === "technical"
                ? "skill-tag--technical"
                : category.toLowerCase() === "soft"
                ? "skill-tag--soft"
                : "";
            return (
              <div className="skills-group" key={category}>
                <div className="skills-group__label">
                  {category.replace(/_/g, " ")}
                </div>
                <div className="skills-tags">
                  {skills.map((skill, i) => (
                    <span className={`skill-tag ${tagClass}`} key={i}>
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
