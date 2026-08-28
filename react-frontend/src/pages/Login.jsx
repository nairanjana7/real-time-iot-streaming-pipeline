import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { ArrowRight, ShieldCheck } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import "./Auth.css";

export default function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");
    setLoading(true);

    try {
      await login(email, password);
      navigate("/app", { replace: true });
    } catch (err) {
      setError(err.message || "Unable to sign in.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="auth-page">
      <section className="auth-shell">
        <div className="auth-brand">
          <Link to="/" className="auth-logo">
            Predict<span>Guard</span>
          </Link>

          <p>AI-powered predictive maintenance platform</p>
        </div>

        <div className="auth-card">
          <div className="auth-icon">
            <ShieldCheck size={24} />
          </div>

          <h1>Welcome back</h1>

          <p className="auth-subtitle">
            Sign in to access your PredictGuard workspace.
          </p>

          <form onSubmit={handleSubmit}>
            <label htmlFor="email">Email address</label>

            <input
              id="email"
              type="email"
              placeholder="admin@company.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />

            <label htmlFor="password">Password</label>

            <input
              id="password"
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />

            {error && (
              <div className="auth-error">
                {error}
              </div>
            )}

            <button
              type="submit"
              className="auth-submit"
              disabled={loading}
            >
              {loading ? "Signing in..." : "Sign in"}
              {!loading && <ArrowRight size={18} />}
            </button>
          </form>

          <div className="auth-divider">
            <span>New to PredictGuard?</span>
          </div>

          <Link to="/signup" className="auth-secondary">
            Create a company account
          </Link>
        </div>

        <Link to="/" className="auth-back">
          ← Back to PredictGuard
        </Link>
      </section>
    </main>
  );
}
