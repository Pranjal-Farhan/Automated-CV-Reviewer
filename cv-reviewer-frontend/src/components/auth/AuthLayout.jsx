import { Link } from "react-router-dom";

export default function AuthLayout({ children, title, subtitle }) {
  return (
    <section className="auth-section">
      <div className="auth-container">
        {/* Brand */}
        <Link to="/" className="auth-brand">
          <svg viewBox="0 0 40 40" fill="none" width="44" height="44">
            <rect width="40" height="40" rx="10" fill="url(#authLg)" />
            <path
              d="M12 28V12h6a6 6 0 0 1 0 12h-6"
              stroke="#fff"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <path
              d="M20 20l8 8"
              stroke="#fff"
              strokeWidth="2.5"
              strokeLinecap="round"
            />
            <defs>
              <linearGradient id="authLg" x1="0" y1="0" x2="40" y2="40">
                <stop stopColor="#6366f1" />
                <stop offset="1" stopColor="#8b5cf6" />
              </linearGradient>
            </defs>
          </svg>
        </Link>

        <h1 className="auth-title">{title}</h1>
        <p className="auth-subtitle">{subtitle}</p>

        <div className="auth-card">{children}</div>
      </div>
    </section>
  );
}
