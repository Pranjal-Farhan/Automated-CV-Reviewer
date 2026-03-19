import { useNavigate } from "react-router-dom";
import { parseAnalysis, formatDate } from "../../utils/helpers";
import CandidateCard from "./CandidateCard";
import SkillsCard from "./SkillsCard";
import ExperienceCard from "./ExperienceCard";
import EducationCard from "./EducationCard";
import SummaryCard from "./SummaryCard";
import RawResponse from "./RawResponse";
import { Download, Plus, FileText, Calendar } from "lucide-react";

function ProjectsCard({ data }) {
  if (!data || !Array.isArray(data) || data.length === 0) return null;

  return (
    <div className="result-card">
      <div className="result-card__header">
        <div
          className="result-card__icon"
          style={{
            background: "rgba(244, 114, 182, 0.15)",
            color: "var(--clr-accent-pink)",
          }}
        >
          <svg
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z" />
            <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z" />
          </svg>
        </div>
        <h3 className="result-card__title">Projects</h3>
      </div>
      <div className="result-card__body">
        {data.map((proj, i) => (
          <div className="timeline-item" key={i}>
            <div className="timeline-item__title">
              {proj.name || proj.title || "Project"}
            </div>
            {proj.description && (
              <div className="timeline-item__desc">{proj.description}</div>
            )}
            {proj.skills &&
              Array.isArray(proj.skills) &&
              proj.skills.length > 0 && (
                <div className="skills-tags" style={{ marginTop: "8px" }}>
                  {proj.skills.map((skill, j) => (
                    <span className="skill-tag skill-tag--technical" key={j}>
                      {skill}
                    </span>
                  ))}
                </div>
              )}
          </div>
        ))}
      </div>
    </div>
  );
}

function QuickStatsCard({ data }) {
  if (!data || typeof data !== "object") return null;

  const stats = Object.entries(data).filter(
    ([, val]) => val !== null && val !== undefined
  );
  if (stats.length === 0) return null;

  return (
    <div className="result-card">
      <div className="result-card__header">
        <div
          className="result-card__icon"
          style={{
            background: "rgba(56, 189, 248, 0.15)",
            color: "var(--clr-accent-blue)",
          }}
        >
          <svg
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <path d="M18 20V10" />
            <path d="M12 20V4" />
            <path d="M6 20v-6" />
          </svg>
        </div>
        <h3 className="result-card__title">Quick Stats</h3>
      </div>
      <div className="result-card__body">
        <div className="candidate-grid">
          {stats.map(([key, value]) => (
            <div className="candidate-field" key={key}>
              <span className="candidate-field__label">
                {key.replace(/_/g, " ")}
              </span>
              <span
                className="candidate-field__value"
                style={{
                  fontSize: "1.25rem",
                  fontWeight: 700,
                  color: "var(--clr-primary-light)",
                }}
              >
                {String(value)}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default function ResultsView({ data }) {
  const navigate = useNavigate();

  const analysis = parseAnalysis(data?.analysis_result);

  const handleDownload = () => {
    const content = JSON.stringify(data?.analysis_result, null, 2);
    const blob = new Blob([content], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `cv-analysis-report.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  console.log("Raw analysis_result:", data?.analysis_result);
  console.log("Parsed analysis:", analysis);

  if (!analysis) {
    return (
      <div className="results">
        <div className="results__container">
          <div className="result-card">
            <p className="summary-text">No analysis data available.</p>
          </div>
        </div>
      </div>
    );
  }

  // If we only got raw text (parsing failed completely)
  if (analysis.raw && Object.keys(analysis).length === 1) {
    return (
      <div className="results">
        <div className="results__container">
          <div className="results__header">
            <div>
              <h2 className="section-title" style={{ textAlign: "left" }}>
                Analysis Complete
              </h2>
              <div className="results__meta">
                {data?.filename && (
                  <span className="results__meta-item">
                    <FileText size={14} />
                    {data.filename}
                  </span>
                )}
                {data?.created_at && (
                  <span className="results__meta-item">
                    <Calendar size={14} />
                    {formatDate(data.created_at)}
                  </span>
                )}
              </div>
            </div>
            <div className="results__actions">
              <button className="btn btn--outline" onClick={handleDownload}>
                <Download size={18} />
                Download Report
              </button>
              <button
                className="btn btn--primary"
                onClick={() => navigate("/dashboard")}
              >
                <Plus size={18} />
                New Upload
              </button>
            </div>
          </div>
          <div className="result-card">
            <div className="result-card__header">
              <h3 className="result-card__title">AI Analysis</h3>
            </div>
            <div className="result-card__body">
              <pre
                style={{
                  whiteSpace: "pre-wrap",
                  wordBreak: "break-word",
                  fontSize: "0.9375rem",
                  lineHeight: "1.7",
                  color: "var(--clr-text-muted)",
                }}
              >
                {analysis.raw}
              </pre>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Extract fields flexibly
  const candidate =
    analysis.candidate_info ||
    analysis.candidate_information ||
    analysis.candidate ||
    analysis.personal_info ||
    analysis.personal_information ||
    analysis.contact_info ||
    analysis.contact ||
    null;
  const skills =
    analysis.skills ||
    analysis.technical_skills ||
    analysis.skill_set ||
    analysis.key_skills ||
    null;
  const experience =
    analysis.experience ||
    analysis.work_experience ||
    analysis.professional_experience ||
    analysis.employment_history ||
    analysis.employment ||
    null;
  const education =
    analysis.education ||
    analysis.academic_background ||
    analysis.qualifications ||
    analysis.educational_background ||
    null;
  const projects = analysis.projects || analysis.project_list || null;
  const summary =
    analysis.summary ||
    analysis.overall_summary ||
    analysis.profile_summary ||
    analysis.overview ||
    analysis.professional_summary ||
    analysis.overall_assessment ||
    null;
  const recommendations =
    analysis.recommendations ||
    analysis.suggestions ||
    analysis.improvements ||
    analysis.feedback ||
    analysis.areas_for_improvement ||
    null;
  const score =
    analysis.score || analysis.overall_score || analysis.rating || null;
  const quickStats =
    analysis.quick_stats || analysis.quickStats || analysis.stats || null;

  const hasStructuredData =
    candidate ||
    skills ||
    experience ||
    education ||
    summary ||
    recommendations ||
    projects;

  return (
    <section className="results">
      <div className="results__container">
        <div className="results__header">
          <div>
            <h2 className="section-title" style={{ textAlign: "left" }}>
              Analysis Complete
            </h2>
            <div className="results__meta">
              {data?.filename && (
                <span className="results__meta-item">
                  <FileText size={14} />
                  {data.filename}
                </span>
              )}
              {data?.created_at && (
                <span className="results__meta-item">
                  <Calendar size={14} />
                  {formatDate(data.created_at)}
                </span>
              )}
            </div>
          </div>
          <div className="results__actions">
            <button className="btn btn--outline" onClick={handleDownload}>
              <Download size={18} />
              Download Report
            </button>
            <button
              className="btn btn--primary"
              onClick={() => navigate("/dashboard")}
            >
              <Plus size={18} />
              New Upload
            </button>
          </div>
        </div>

        {hasStructuredData ? (
          <>
            <CandidateCard data={candidate} />
            <div className="results__grid">
              <SkillsCard data={skills} />
              <ExperienceCard data={experience} />
              <EducationCard data={education} />
              <ProjectsCard data={projects} />
              <SummaryCard
                summary={summary}
                recommendations={recommendations}
                score={score}
              />
              <QuickStatsCard data={quickStats} />
            </div>
          </>
        ) : (
          <div className="results__grid">
            {Object.entries(analysis).map(([key, value]) => {
              if (key === "raw") return null;
              return (
                <div className="result-card" key={key}>
                  <div className="result-card__header">
                    <h3 className="result-card__title">
                      {key
                        .replace(/_/g, " ")
                        .replace(/\b\w/g, (c) => c.toUpperCase())}
                    </h3>
                  </div>
                  <div className="result-card__body">
                    {typeof value === "string" ? (
                      <p className="summary-text">{value}</p>
                    ) : Array.isArray(value) ? (
                      <div className="skills-tags">
                        {value.map((item, i) => (
                          <span className="skill-tag" key={i}>
                            {typeof item === "string"
                              ? item
                              : JSON.stringify(item)}
                          </span>
                        ))}
                      </div>
                    ) : typeof value === "object" && value !== null ? (
                      <pre
                        style={{
                          whiteSpace: "pre-wrap",
                          fontSize: "0.875rem",
                          color: "var(--clr-text-muted)",
                        }}
                      >
                        {JSON.stringify(value, null, 2)}
                      </pre>
                    ) : (
                      <p className="summary-text">{String(value)}</p>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}

        <RawResponse data={analysis} />
      </div>
    </section>
  );
}
