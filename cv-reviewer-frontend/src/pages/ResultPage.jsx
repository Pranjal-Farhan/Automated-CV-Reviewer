import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { cvAPI } from "../api/cv";
import { useToast } from "../hooks/useToast";
import ResultsView from "../components/cv/ResultsView";
import ProcessingView from "../components/cv/ProcessingView";

export default function ResultPage() {
  const { jobId } = useParams();
  const navigate = useNavigate();
  const { addToast } = useToast();

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [polling, setPolling] = useState(false);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    let intervalId = null;
    let startTime = Date.now();
    let cancelled = false;

    const fetchResult = async () => {
      try {
        const res = await cvAPI.getResult(jobId);
        if (cancelled) return;

        const result = res.data;
        setData(result);

        if (result.status === "completed") {
          setLoading(false);
          setPolling(false);
          if (intervalId) clearInterval(intervalId);
          setProgress(100);
        } else if (result.status === "failed") {
          setLoading(false);
          setPolling(false);
          if (intervalId) clearInterval(intervalId);
          setError(result.error || "Analysis failed.");
          addToast("Analysis failed", "error");
        } else {
          // Still processing — start polling if not already
          setLoading(false);
          setPolling(true);
          const elapsed = Date.now() - startTime;
          setProgress(Math.min(85, (elapsed / 120000) * 100));

          if (!intervalId) {
            intervalId = setInterval(async () => {
              try {
                const pollRes = await cvAPI.getResult(jobId);
                if (cancelled) return;
                setData(pollRes.data);
                const pElapsed = Date.now() - startTime;
                setProgress(Math.min(85, (pElapsed / 120000) * 100));

                if (pollRes.data.status === "completed") {
                  clearInterval(intervalId);
                  intervalId = null;
                  setPolling(false);
                  setProgress(100);
                } else if (pollRes.data.status === "failed") {
                  clearInterval(intervalId);
                  intervalId = null;
                  setPolling(false);
                  setError(pollRes.data.error || "Analysis failed.");
                }

                // Timeout after 2 minutes
                if (Date.now() - startTime > 120000) {
                  clearInterval(intervalId);
                  intervalId = null;
                  setPolling(false);
                  setError("Analysis timed out. Please try again.");
                }
              } catch (err) {
                console.error("Poll error:", err);
              }
            }, 2500);
          }
        }
      } catch (err) {
        if (cancelled) return;
        setLoading(false);
        if (err.response?.status === 404) {
          setError("Job not found.");
        } else if (err.response?.status === 403) {
          setError("You do not have access to this result.");
          addToast("Access denied", "error");
        } else {
          setError("Failed to load result.");
        }
      }
    };

    fetchResult();

    return () => {
      cancelled = true;
      if (intervalId) clearInterval(intervalId);
    };
  }, [jobId, addToast]);

  // Loading spinner
  if (loading) {
    return (
      <div className="page-loader">
        <div className="spinner" />
        <p>Loading result...</p>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <section className="error-page">
        <div className="error-page__container">
          <div className="error-page__card">
            <h2>Something Went Wrong</h2>
            <p>{error}</p>
            <div className="error-page__actions">
              <button
                className="btn btn--primary"
                onClick={() => navigate("/dashboard")}
              >
                Back to Dashboard
              </button>
              <button
                className="btn btn--outline"
                onClick={() => navigate("/history")}
              >
                View History
              </button>
            </div>
          </div>
        </div>
      </section>
    );
  }

  // Still processing
  if (polling || (data && data.status !== "completed")) {
    return (
      <ProcessingView
        status={data?.status || "processing"}
        progress={progress}
      />
    );
  }

  // Completed
  return <ResultsView data={data} />;
}
