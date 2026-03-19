import { useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { authAPI } from "../../api/auth";
import { useAuth } from "../../hooks/useAuth";
import { useToast } from "../../hooks/useToast";
import GoogleAuthButton from "./GoogleAuthButton";
import { Mail, Lock, Eye, EyeOff, ArrowRight } from "lucide-react";

export default function LoginForm() {
  const [form, setForm] = useState({ email: "", password: "" });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});

  const { loginUser } = useAuth();
  const { addToast } = useToast();
  const navigate = useNavigate();
  const location = useLocation();

  const from = location.state?.from?.pathname || "/dashboard";

  const validate = () => {
    const errs = {};
    if (!form.email.trim()) errs.email = "Email is required";
    else if (!/\S+@\S+\.\S+/.test(form.email)) errs.email = "Invalid email";
    if (!form.password) errs.password = "Password is required";
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    setLoading(true);
    try {
      const res = await authAPI.login({
        email: form.email.trim().toLowerCase(),
        password: form.password,
      });
      loginUser(res.data);
      addToast("Welcome back!", "success");
      navigate(from, { replace: true });
    } catch (err) {
      const msg =
        err.response?.data?.detail || "Login failed. Please try again.";
      addToast(msg, "error");
      setErrors({ general: msg });
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (field) => (e) => {
    setForm((prev) => ({ ...prev, [field]: e.target.value }));
    if (errors[field]) setErrors((prev) => ({ ...prev, [field]: null }));
  };

  return (
    <form className="auth-form" onSubmit={handleSubmit} noValidate>
      <GoogleAuthButton label="Sign in with Google" />

      <div className="auth-divider">
        <span>or sign in with email</span>
      </div>

      {errors.general && (
        <div className="auth-error-banner">{errors.general}</div>
      )}

      {/* Email */}
      <div className={`form-group ${errors.email ? "form-group--error" : ""}`}>
        <label className="form-label" htmlFor="login-email">
          Email
        </label>
        <div className="form-input-wrapper">
          <Mail size={18} className="form-icon" />
          <input
            id="login-email"
            type="email"
            className="form-input"
            placeholder="you@example.com"
            value={form.email}
            onChange={handleChange("email")}
            autoComplete="email"
          />
        </div>
        {errors.email && <span className="form-error">{errors.email}</span>}
      </div>

      {/* Password */}
      <div
        className={`form-group ${errors.password ? "form-group--error" : ""}`}
      >
        <label className="form-label" htmlFor="login-password">
          Password
        </label>
        <div className="form-input-wrapper">
          <Lock size={18} className="form-icon" />
          <input
            id="login-password"
            type={showPassword ? "text" : "password"}
            className="form-input"
            placeholder="••••••••"
            value={form.password}
            onChange={handleChange("password")}
            autoComplete="current-password"
          />
          <button
            type="button"
            className="form-toggle-password"
            onClick={() => setShowPassword((p) => !p)}
            tabIndex={-1}
          >
            {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
          </button>
        </div>
        {errors.password && (
          <span className="form-error">{errors.password}</span>
        )}
      </div>

      <button
        type="submit"
        className="btn btn--primary btn--full"
        disabled={loading}
      >
        {loading ? (
          <>
            <div className="btn-spinner" />
            Signing in...
          </>
        ) : (
          <>
            Sign In
            <ArrowRight size={18} />
          </>
        )}
      </button>

      <p className="auth-switch">
        Don&apos;t have an account?{" "}
        <Link to="/register" state={location.state}>
          Sign up
        </Link>
      </p>
    </form>
  );
}
