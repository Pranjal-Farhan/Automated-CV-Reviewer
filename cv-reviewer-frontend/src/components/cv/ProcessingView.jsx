import { useEffect, useState } from "react";

const STEPS = [
  "File uploaded",
  "Extracting text",
  "AI analysis in progress",
  "Finalizing results",
];

export default function ProcessingView({ status, progress }) {
  const [activeStep, setActiveStep] = useState(0);

  useEffect(() => {
    if (progress < 20) setActiveStep(0);
    else if (progress < 40) setActiveStep(1);
    else if (progress < 80) setActiveStep(2);
    else setActiveStep(3);
  }, [progress]);

  return (
    <section className="processing">
      <div className="processing__container">
        <div className="processing__card">
          <div className="processing__spinner">
            <div className="spinner" />
          </div>
          <h2 className="processing__title">Analyzing Your CV...</h2>
          <p className="processing__text">
            Our AI is reviewing your resume. This usually takes 15–30 seconds.
          </p>

          <div className="processing__progress">
            <div className="progress-bar">
              <div
                className="progress-bar__fill"
                style={{ width: `${Math.min(progress, 100)}%` }}
              />
            </div>
            <span className="processing__status">
              {status === "uploading" ? "Uploading..." : "Processing..."}
            </span>
          </div>

          <div className="processing__steps">
            {STEPS.map((label, i) => {
              let cls = "proc-step";
              if (i < activeStep) cls += " proc-step--done";
              else if (i === activeStep) cls += " proc-step--active";
              return (
                <div className={cls} key={i}>
                  <div
                    className={`proc-step__dot ${
                      i === activeStep ? "proc-step__dot--active" : ""
                    }`}
                  />
                  <span>{label}</span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </section>
  );
}
