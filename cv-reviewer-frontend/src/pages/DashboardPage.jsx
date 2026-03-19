import { useAuth } from "../hooks/useAuth";
import { useCVUpload } from "../hooks/useCVUpload";
import Dropzone from "../components/cv/Dropzone";
import ProcessingView from "../components/cv/ProcessingView";

export default function DashboardPage() {
  const { user } = useAuth();
  const { uploading, status, progress, error, upload, reset } = useCVUpload();

  const isProcessing =
    status === "uploading" || status === "pending" || status === "processing";

  return (
    <section className="dashboard">
      <div className="dashboard__container">
        {/* Welcome Header */}
        <div className="dashboard__header">
          <div>
            <h1 className="dashboard__title">
              Welcome back, {user?.name?.split(" ")[0] || "there"}!
            </h1>
            <p className="dashboard__subtitle">
              Upload a CV to get an AI-powered analysis.
            </p>
          </div>
        </div>

        {/* Show Processing or Upload */}
        {isProcessing ? (
          <ProcessingView status={status} progress={progress} />
        ) : (
          <div className="dashboard__upload">
            <h2 className="section-title">Upload Your CV</h2>
            <p className="section-subtitle">
              Accepted formats: PDF, TXT — Max 10 MB
            </p>
            <Dropzone onUpload={upload} uploading={uploading} />

            {error && (
              <div
                className="message message--error"
                style={{ marginTop: 16, maxWidth: 640, marginInline: "auto" }}
              >
                <span>{error}</span>
                <button
                  className="btn btn--outline btn--sm"
                  onClick={reset}
                  style={{ marginLeft: "auto" }}
                >
                  Try Again
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </section>
  );
}
