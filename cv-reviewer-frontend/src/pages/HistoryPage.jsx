import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { cvAPI } from "../api/cv";
import { useToast } from "../hooks/useToast";
import { formatDate, getStatusColor } from "../utils/helpers";
import {
  History,
  FileText,
  ArrowRight,
  AlertCircle,
  CheckCircle,
  Clock,
  XCircle,
  RefreshCw,
} from "lucide-react";

export default function HistoryPage() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { addToast } = useToast();

  const fetchHistory = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await cvAPI.getHistory();
      setJobs(res.data.jobs || []);
    } catch (err) {
      const msg = err.response?.data?.detail || "Failed to load history.";
      setError(msg);
      addToast(msg, "error");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const getStatusIcon = (status) => {
    switch (status) {
      case "completed":
        return <CheckCircle size={16} />;
      case "processing":
      case "pending":
        return <Clock size={16} />;
      case "failed":
        return <XCircle size={16} />;
      default:
        return <AlertCircle size={16} />;
    }
  };

  return (
    <section className="history-page">
      <div className="history-page__container">
        <div className="history-page__header">
          <div>
            <h1 className="history-page__title">
              <History size={28} />
              Analysis History
            </h1>
            <p className="history-page__subtitle">
              View all your past CV analyses.
            </p>
          </div>
          <button
            className="btn btn--outline"
            onClick={fetchHistory}
            disabled={loading}
          >
            <RefreshCw size={16} className={loading ? "spin-animation" : ""} />
            Refresh
          </button>
        </div>

        {/* Loading */}
        {loading && (
          <div className="page-loader" style={{ minHeight: "300px" }}>
            <div className="spinner" />
            <p>Loading history...</p>
          </div>
        )}

        {/* Error */}
        {!loading && error && (
          <div className="message message--error">
            <AlertCircle size={18} />
            <span>{error}</span>
          </div>
        )}

        {/* Empty State */}
        {!loading && !error && jobs.length === 0 && (
          <div className="history-empty">
            <FileText size={48} className="history-empty__icon" />
            <h3>No analyses yet</h3>
            <p>Upload your first CV to get started!</p>
            <Link
              to="/dashboard"
              className="btn btn--primary"
              style={{ marginTop: 16 }}
            >
              Upload CV
            </Link>
          </div>
        )}

        {/* Job List */}
        {!loading && !error && jobs.length > 0 && (
          <div className="history-list">
            {jobs.map((job) => (
              <Link
                to={job.status === "completed" ? `/result/${job.job_id}` : "#"}
                key={job.job_id}
                className={`history-card ${
                  job.status !== "completed" ? "history-card--disabled" : ""
                }`}
              >
                <div className="history-card__left">
                  <div className="history-card__file-icon">
                    <FileText size={22} />
                  </div>
                  <div className="history-card__info">
                    <span className="history-card__filename">
                      {job.filename || "Unknown file"}
                    </span>
                    <span className="history-card__date">
                      {formatDate(job.created_at)}
                    </span>
                  </div>
                </div>
                <div className="history-card__right">
                  <span
                    className="history-card__status"
                    style={{ color: getStatusColor(job.status) }}
                  >
                    {getStatusIcon(job.status)}
                    {job.status}
                  </span>
                  {job.status === "completed" && (
                    <ArrowRight size={18} className="history-card__arrow" />
                  )}
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}
