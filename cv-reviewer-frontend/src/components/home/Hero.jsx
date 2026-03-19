import { Link } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";
import { ArrowRight } from "lucide-react";

export default function Hero() {
  const { isAuthenticated } = useAuth();

  return (
    <header className="hero">
      <div className="hero__container">
        <div className="hero__badge">
          <span className="hero__badge-dot" />
          Powered by Google Gemini 2.5 Flash
        </div>
        <h1 className="hero__title">
          Analyze Your Resume
          <br />
          with <span className="hero__title--gradient">AI Precision</span>
        </h1>
        <p className="hero__subtitle">
          Upload your CV and receive an instant, structured analysis covering
          skills, experience, education, and actionable recommendations — all
          powered by advanced AI.
        </p>
        <Link
          to={isAuthenticated ? "/dashboard" : "/register"}
          className="hero__cta"
        >
          {isAuthenticated ? "Go to Dashboard" : "Get Started Free"}
          <ArrowRight size={20} />
        </Link>
      </div>
    </header>
  );
}
