import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { ArrowRight, Building2 } from "lucide-react";
import { registerCompany } from "../services/api";
import "./Auth.css";

export default function Signup() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    company_name: "",
    industry: "",
    admin_name: "",
    admin_email: "",
    password: "",
  });

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (event) => {
    const { name, value } = event.target;

    setForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");
    setLoading(true);

    try {
      await registerCompany(form);

      navigate("/login", {
        replace: true,
        state: {
          registered: true,
          email: form.admin_email,
        },
      });
    } catch (err) {
      setError(
        err.message || "Unable to create company account."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="auth-page">
      <section className="auth-shell auth-shell-wide">
        <div className="auth-brand">
          <Link to="/" className="auth-logo">
            Predict<span>Guard</span>
          </Link>

          <p>AI-powered predictive maintenance platform</p>
        </div>

        <div className="auth-card">
          <div className="auth-icon">
            <Building2 size={24} />
          </div>

          <h1>Create your workspace</h1>

          <p className="auth-subtitle">
            Register your company and start monitoring
            industrial assets with PredictGuard.
          </p>

          <form onSubmit={handleSubmit}>
            <label htmlFor="company_name">
              Company name
            </label>

            <input
              id="company_name"
              name="company_name"
              type="text"
              placeholder="Acme Manufacturing"
              value={form.company_name}
              onChange={handleChange}
              required
            />

            <label htmlFor="industry">
              Industry
            </label>

            <select
              id="industry"
              name="industry"
              value={form.industry}
              onChange={handleChange}
              required
            >
              <option value="">Select your industry</option>
              <option value="Manufacturing">
                Manufacturing
              </option>
              <option value="Automotive">
                Automotive
              </option>
              <option value="Energy">
                Energy
              </option>
              <option value="Pharmaceutical">
                Pharmaceutical
              </option>
              <option value="Food & Beverage">
                Food & Beverage
              </option>
              <option value="Other">Other</option>
            </select>

            <label htmlFor="admin_name">
              Administrator name
            </label>

            <input
              id="admin_name"
              name="admin_name"
              type="text"
              placeholder="Admin name"
              value={form.admin_name}
              onChange={handleChange}
              required
            />

            <label htmlFor="admin_email">
              Administrator email
            </label>

            <input
              id="admin_email"
              name="admin_email"
              type="email"
              placeholder="admin@company.com"
              value={form.admin_email}
              onChange={handleChange}
              required
            />

            <label htmlFor="password">
              Password
            </label>

            <input
              id="password"
              name="password"
              type="password"
              placeholder="Create a secure password"
              value={form.password}
              onChange={handleChange}
              minLength={8}
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
              {loading
                ? "Creating workspace..."
                : "Create workspace"}

              {!loading && <ArrowRight size={18} />}
            </button>
          </form>

          <div className="auth-divider">
            <span>Already have an account?</span>
          </div>

          <Link to="/login" className="auth-secondary">
            Sign in instead
          </Link>
        </div>

        <Link to="/" className="auth-back">
          ← Back to PredictGuard
        </Link>
      </section>
    </main>
  );
}
