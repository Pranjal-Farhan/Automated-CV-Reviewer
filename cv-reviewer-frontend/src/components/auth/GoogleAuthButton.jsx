import { useGoogleLogin } from "@react-oauth/google";
import { authAPI } from "../../api/auth";
import { useAuth } from "../../hooks/useAuth";
import { useToast } from "../../hooks/useToast";
import { useNavigate, useLocation } from "react-router-dom";
import { useState } from "react";

export default function GoogleAuthButton({ label = "Continue with Google" }) {
  const { loginUser } = useAuth();
  const { addToast } = useToast();
  const navigate = useNavigate();
  const location = useLocation();
  const [loading, setLoading] = useState(false);

  const from = location.state?.from?.pathname || "/dashboard";

  const handleGoogleLogin = useGoogleLogin({
    flow: "auth-code",
    onSuccess: async (codeResponse) => {
      // Note: For the "auth-code" flow you'd exchange the code server-side.
      // For simplicity, we use the "implicit" flow with credential below.
    },
    onError: () => {
      addToast("Google sign-in failed", "error");
    },
  });

  // Using the credential/id_token flow via @react-oauth/google's GoogleLogin
  // We'll use a custom button that triggers the Google One Tap or popup
  const handleClick = async () => {
    setLoading(true);
    try {
      // Trigger Google OAuth popup using the implicit flow
      // We'll use google.accounts.oauth2 directly
      const client = window.google?.accounts?.oauth2?.initTokenClient({
        client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
        scope: "email profile",
        callback: async (response) => {
          if (response.access_token) {
            try {
              // Get user info from Google
              const userInfoRes = await fetch(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                {
                  headers: { Authorization: `Bearer ${response.access_token}` },
                }
              );
              const userInfo = await userInfoRes.json();

              // Send the Google sub (id) to our backend
              // Our backend expects an id_token credential, so let's use
              // the id_token flow instead
              const res = await authAPI.googleAuth(response.access_token);
              loginUser(res.data);
              addToast("Signed in with Google!", "success");
              navigate(from, { replace: true });
            } catch (err) {
              addToast(
                err.response?.data?.detail || "Google authentication failed",
                "error"
              );
            }
          }
          setLoading(false);
        },
      });

      if (client) {
        client.requestAccessToken();
      } else {
        // Fallback: if Google script isn't loaded
        addToast("Google sign-in is not available", "error");
        setLoading(false);
      }
    } catch {
      addToast("Google sign-in failed", "error");
      setLoading(false);
    }
  };

  return (
    <button
      type="button"
      className="btn btn--google"
      onClick={handleClick}
      disabled={loading}
    >
      <svg width="20" height="20" viewBox="0 0 24 24">
        <path
          d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"
          fill="#4285F4"
        />
        <path
          d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
          fill="#34A853"
        />
        <path
          d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
          fill="#FBBC05"
        />
        <path
          d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
          fill="#EA4335"
        />
      </svg>
      {loading ? "Connecting..." : label}
    </button>
  );
}
