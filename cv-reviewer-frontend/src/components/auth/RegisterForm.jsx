import { useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { authAPI } from "../../api/auth";
import { useAuth } from "../../hooks/useAuth";
import { useToast } from "../../hooks/useToast";
import GoogleAuthButton from "./GoogleAuthButton";
import { User, Mail, Lock, Eye, EyeOff, ArrowRight } from "lucide-react";

export default function RegisterForm() {
  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
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
    if (!form.name.trim()) errs.name = "Name is required";
    else if (form.name.trim().length < 2)
      errs.name = "Name must be at least 2 characters";
    if (!form.email.trim()) errs.email = "Email is required";
    else if (!/\S+@\S+\.\S+/.test(form.email)) errs.email = "Invalid email";
    if (!form.password) errs.password = "Password is required";
    else if (form.password.length < 6)
      errs.password = "Must be at least 6 characters";
    if (form.password !== form.confirmPassword)
      errs.confirmPassword = "Passwords do not match";
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    setLoading(true);
    try {
      const res = await authAPI.register({
        name: form.name.trim(),
        email: form.email.trim().toLowerCase(),
        password: form.password,
      });
      loginUser(res.data);
      addToast("Account created successfully!", "success");
      navigate(from, { replace: true });
    } catch (err) {
      const msg = err.response?.data?.detail || "Registration failed.";
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
      <GoogleAuthButton label="Sign up with Google" />

      <div className="auth-divider">
        <span>or create an account with email</span>
      </div>

      {errors.general && (
        <div className="auth-error-banner">{errors.general}</div>
      )}

      {/* Name */}
      <div className={`form-group ${errors.name ? "form-group--error" : ""}`}>
        <label className="form-label" htmlFor="reg-name">
          Full Name
        </label>
        <div className="form-input-wrapper">
          <User size={18} className="form-icon" />
          <input
            id="reg-name"
            type="text"
            className="form-input"
            placeholder="John Doe"
            value={form.name}
            onChange={handleChange("name")}
            autoComplete="name"
          />
        </div>
        {errors.name && <span className="form-error">{errors.name}</span>}
      </div>

      {/* Email */}
      <div className={`form-group ${errors.email ? "form-group--error" : ""}`}>
        <label className="form-label" htmlFor="reg-email">
          Email
        </label>
        <div className="form-input-wrapper">
          <Mail size={18} className="form-icon" />
          <input
            id="reg-email"
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
        <label className="form-label" htmlFor="reg-password">
          Password
        </label>
        <div className="form-input-wrapper">
          <Lock size={18} className="form-icon" />
          <input
            id="reg-password"
            type={showPassword ? "text" : "password"}
            className="form-input"
            placeholder="Min. 6 characters"
            value={form.password}
            onChange={handleChange("password")}
            autoComplete="new-password"
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

      {/* Confirm Password */}
      <div
        className={`form-group ${
          errors.confirmPassword ? "form-group--error" : ""
        }`}
      >
        <label className="form-label" htmlFor="reg-confirm">
          Confirm Password
        </label>
        <div className="form-input-wrapper">
          <Lock size={18} className="form-icon" />
          <input
            id="reg-confirm"
            type={showPassword ? "text" : "password"}
            className="form-input"
            placeholder="Re-enter password"
            value={form.confirmPassword}
            onChange={handleChange("confirmPassword")}
            autoComplete="new-password"
          />
        </div>
        {errors.confirmPassword && (
          <span className="form-error">{errors.confirmPassword}</span>
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
            Creating account...
          </>
        ) : (
          <>
            Create Account
            <ArrowRight size={18} />
          </>
        )}
      </button>

      <p className="auth-switch">
        Already have an account?{" "}
        <Link to="/login" state={location.state}>
          Sign in
        </Link>
      </p>
    </form>
  );
}
