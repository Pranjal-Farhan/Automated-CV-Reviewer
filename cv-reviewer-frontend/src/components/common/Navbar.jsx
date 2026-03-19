import { useState, useRef, useEffect } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";
import { getInitials } from "../../utils/helpers";
import {
  Menu,
  X,
  LayoutDashboard,
  History,
  LogOut,
  ChevronDown,
  ExternalLink,
} from "lucide-react";

export default function Navbar() {
  const { user, isAuthenticated, logoutUser } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef(null);

  useEffect(() => {
    function handleClickOutside(e) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setDropdownOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // Close mobile menu on route change
  useEffect(() => {
    setMobileOpen(false);
    setDropdownOpen(false);
  }, [location.pathname]);

  const handleLogout = () => {
    logoutUser();
    setDropdownOpen(false);
    navigate("/");
  };

  return (
    <nav className="navbar">
      <div className="navbar__container">
        {/* Brand */}
        <Link to="/" className="navbar__brand">
          <svg className="navbar__logo" viewBox="0 0 40 40" fill="none">
            <rect width="40" height="40" rx="10" fill="url(#navLg)" />
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
              <linearGradient id="navLg" x1="0" y1="0" x2="40" y2="40">
                <stop stopColor="#6366f1" />
                <stop offset="1" stopColor="#8b5cf6" />
              </linearGradient>
            </defs>
          </svg>
          <span>CV Reviewer</span>
        </Link>

        {/* Desktop Links */}
        <div className="navbar__links">
          {isAuthenticated ? (
            <>
              <Link to="/dashboard" className="navbar__link">
                <LayoutDashboard size={16} />
                Dashboard
              </Link>
              <Link to="/history" className="navbar__link">
                <History size={16} />
                History
              </Link>

              {/* User Dropdown */}
              <div className="navbar__dropdown" ref={dropdownRef}>
                <button
                  className="navbar__user-btn"
                  onClick={() => setDropdownOpen((p) => !p)}
                >
                  {user?.avatar ? (
                    <img src={user.avatar} alt="" className="navbar__avatar" />
                  ) : (
                    <div className="navbar__avatar-placeholder">
                      {getInitials(user?.name)}
                    </div>
                  )}
                  <span className="navbar__user-name">{user?.name}</span>
                  <ChevronDown
                    size={14}
                    className={`navbar__chevron ${
                      dropdownOpen ? "navbar__chevron--open" : ""
                    }`}
                  />
                </button>

                {dropdownOpen && (
                  <div className="navbar__dropdown-menu">
                    <div className="navbar__dropdown-header">
                      <span className="navbar__dropdown-name">
                        {user?.name}
                      </span>
                      <span className="navbar__dropdown-email">
                        {user?.email}
                      </span>
                    </div>
                    <div className="navbar__dropdown-divider" />
                    <button
                      className="navbar__dropdown-item"
                      onClick={() => {
                        navigate("/dashboard");
                        setDropdownOpen(false);
                      }}
                    >
                      <LayoutDashboard size={16} />
                      Dashboard
                    </button>
                    <button
                      className="navbar__dropdown-item"
                      onClick={() => {
                        navigate("/history");
                        setDropdownOpen(false);
                      }}
                    >
                      <History size={16} />
                      History
                    </button>
                    <div className="navbar__dropdown-divider" />
                    <button
                      className="navbar__dropdown-item navbar__dropdown-item--danger"
                      onClick={handleLogout}
                    >
                      <LogOut size={16} />
                      Sign Out
                    </button>
                  </div>
                )}
              </div>
            </>
          ) : (
            <>
              <Link to="/login" className="navbar__link">
                Sign In
              </Link>
              <Link to="/register" className="btn btn--primary btn--sm">
                Get Started
              </Link>
            </>
          )}
        </div>

        {/* Mobile Toggle */}
        <button
          className="navbar__mobile-toggle"
          onClick={() => setMobileOpen((p) => !p)}
        >
          {mobileOpen ? <X size={22} /> : <Menu size={22} />}
        </button>
      </div>

      {/* Mobile Menu */}
      {mobileOpen && (
        <div className="navbar__mobile-menu">
          {isAuthenticated ? (
            <>
              <div className="navbar__mobile-user">
                {user?.avatar ? (
                  <img src={user.avatar} alt="" className="navbar__avatar" />
                ) : (
                  <div className="navbar__avatar-placeholder">
                    {getInitials(user?.name)}
                  </div>
                )}
                <div>
                  <div className="navbar__mobile-user-name">{user?.name}</div>
                  <div className="navbar__mobile-user-email">{user?.email}</div>
                </div>
              </div>
              <Link to="/dashboard" className="navbar__mobile-link">
                <LayoutDashboard size={18} /> Dashboard
              </Link>
              <Link to="/history" className="navbar__mobile-link">
                <History size={18} /> History
              </Link>
              <button
                className="navbar__mobile-link navbar__mobile-link--danger"
                onClick={handleLogout}
              >
                <LogOut size={18} /> Sign Out
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="navbar__mobile-link">
                Sign In
              </Link>
              <Link to="/register" className="navbar__mobile-link">
                Get Started
              </Link>
            </>
          )}
        </div>
      )}
    </nav>
  );
}
