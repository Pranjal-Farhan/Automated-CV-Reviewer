import { Upload, Settings, FileText } from "lucide-react";

const steps = [
  {
    icon: <Upload size={28} />,
    title: "1. Upload",
    text: "Drag & drop or browse for your CV in PDF or TXT format.",
    variant: "step-card__icon--1",
  },
  {
    icon: <Settings size={28} />,
    title: "2. AI Analyzes",
    text: "Our backend extracts text and sends it to Gemini AI for structured analysis.",
    variant: "step-card__icon--2",
  },
  {
    icon: <FileText size={28} />,
    title: "3. Get Results",
    text: "View a rich, structured breakdown of your skills, experience, and recommendations.",
    variant: "step-card__icon--3",
  },
];

export default function HowItWorks() {
  return (
    <section id="how-it-works" className="steps">
      <div className="steps__container">
        <h2 className="section-title">How It Works</h2>
        <p className="section-subtitle">
          Three simple steps to a smarter resume review.
        </p>
        <div className="steps__grid">
          {steps.map((step, i) => (
            <div className="step-card" key={i}>
              <div className={`step-card__icon ${step.variant}`}>
                {step.icon}
              </div>
              <h3 className="step-card__title">{step.title}</h3>
              <p className="step-card__text">{step.text}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
