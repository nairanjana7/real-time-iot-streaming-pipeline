import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  ArrowRight,
  CheckCircle2,
  ChevronRight,
  Factory,
  Gauge,
  Menu,
  Network,
  ShieldCheck,
  Sparkles,
  X,
  Zap,
} from "lucide-react";
import "./LandingPage.css";

const stats = [
  { value: "1,200+", label: "Connected Machines" },
  { value: "25M+", label: "Telemetry Events" },
  { value: "99.9%", label: "Platform Availability" },
  { value: "50+", label: "Industrial Customers" },
];

const capabilities = [
  {
    icon: Gauge,
    title: "Real-time Monitoring",
    text: "Observe machine health, operating conditions, and production telemetry from a single control layer.",
  },
  {
    icon: Sparkles,
    title: "Predictive Intelligence",
    text: "Machine-learning models identify abnormal operating patterns before they become costly failures.",
  },
  {
    icon: ShieldCheck,
    title: "Explainable Predictions",
    text: "Understand why a machine is at risk with transparent risk factors and actionable recommendations.",
  },
  {
    icon: Zap,
    title: "Real-time Alerts",
    text: "Surface critical machine conditions quickly so maintenance teams can act before downtime occurs.",
  },
];

const industries = [
  "Manufacturing",
  "Automotive",
  "Energy",
  "Process Industry",
];

function LandingPage() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const navigate = useNavigate();

  const scrollTo = (id) => {
    document.getElementById(id)?.scrollIntoView({
      behavior: "smooth",
    });
    setMobileMenuOpen(false);
  };

  return (
    <div className="landing-page">
      {/* NAVBAR */}
      <header className="landing-nav">
        <div className="nav-container">
          <button
            className="brand"
            onClick={() => scrollTo("overview")}
            aria-label="PredictGuard home"
          >
            <span className="brand-mark">
              <span />
              <span />
              <span />
            </span>
            <span className="brand-name">PredictGuard</span>
          </button>

          <nav className={`desktop-nav ${mobileMenuOpen ? "mobile-open" : ""}`}>
            <button onClick={() => scrollTo("overview")}>Overview</button>
            <button onClick={() => scrollTo("about")}>About</button>
            <button onClick={() => scrollTo("how-it-works")}>
              How It Works
            </button>
            <button onClick={() => scrollTo("features")}>Features</button>
            <button onClick={() => scrollTo("demo")}>Demo</button>
            <button onClick={() => scrollTo("pricing")}>Pricing</button>
          </nav>

          <div className="nav-actions">
            <button
		className="login-button"
	        onClick={() => navigate("/login")}
	      >
	        Login
             </button>
            <button
              className="primary-button nav-cta"
              onClick={() => navigate("/signup")}
            >
              Get Started
              <ArrowRight size={16} />
            </button>
          </div>

          <button
            className="mobile-menu-button"
            onClick={() => setMobileMenuOpen((value) => !value)}
            aria-label="Toggle navigation"
          >
            {mobileMenuOpen ? <X size={22} /> : <Menu size={22} />}
          </button>
        </div>
      </header>

      {/* HERO */}
      <main>
        <section id="overview" className="hero-section">
          <div className="hero-container">
            <div className="hero-copy">
              <div className="eyebrow">
                <span className="eyebrow-dot" />
                INDUSTRIAL PREDICTIVE INTELLIGENCE
              </div>

              <h1>
                Predict machine failures
                <span> before they disrupt production.</span>
              </h1>

              <p className="hero-description">
                PredictGuard turns industrial telemetry into actionable
                intelligence, helping maintenance teams detect abnormal
                conditions, understand machine risk, and act before downtime.
              </p>

              <div className="hero-actions">
               <button
                 className="primary-button large-button"
                 onClick={() => navigate("/signup")}
               >
                 Get Started
                 <ArrowRight size={18} />
               </button>

                <button
                  className="secondary-button large-button"
                  onClick={() => scrollTo("demo")}
                >
                  View Demo
                  <ChevronRight size={18} />
                </button>
              </div>

              <div className="hero-note">
                <CheckCircle2 size={16} />
                Built for modern industrial environments
              </div>
            </div>

            <div className="hero-visual">
              <div className="visual-window">
                <div className="window-header">
                  <div className="window-dots">
                    <span />
                    <span />
                    <span />
                  </div>
                  <span className="window-title">PredictGuard / Overview</span>
                  <span className="window-live">
                    <span />
                    LIVE
                  </span>
                </div>

                <div className="dashboard-preview">
                  <div className="preview-heading">
                    <div>
                      <span>Production Floor</span>
                      <strong>Machine Health</strong>
                    </div>
                    <div className="preview-date">Real-time</div>
                  </div>

                  <div className="preview-metrics">
                    <div>
                      <span>Connected</span>
                      <strong>24</strong>
                    </div>
                    <div>
                      <span>Normal</span>
                      <strong>19</strong>
                    </div>
                    <div>
                      <span>Warning</span>
                      <strong>3</strong>
                    </div>
                    <div>
                      <span>Critical</span>
                      <strong>2</strong>
                    </div>
                  </div>

                  <div className="machine-list">
                    <div className="machine-list-header">
                      <span>Machine</span>
                      <span>Status</span>
                      <span>Temperature</span>
                      <span>Risk</span>
                    </div>

                    <div className="machine-row">
                      <strong>CNC-001</strong>
                      <span className="status normal">NORMAL</span>
                      <span>32.5°C</span>
                      <span>0.3%</span>
                    </div>

                    <div className="machine-row">
                      <strong>CNC-002</strong>
                      <span className="status normal">NORMAL</span>
                      <span>34.1°C</span>
                      <span>1.1%</span>
                    </div>

                    <div className="machine-row">
                      <strong>CNC-003</strong>
                      <span className="status warning">WARNING</span>
                      <span>41.8°C</span>
                      <span>18.4%</span>
                    </div>

                    <div className="machine-row">
                      <strong>CNC-004</strong>
                      <span className="status critical">CRITICAL</span>
                      <span>39.6°C</span>
                      <span>99.7%</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="visual-label">
                <span className="label-line" />
                Real-time machine intelligence
              </div>
            </div>
          </div>
        </section>

        {/* STATS */}
        <section className="stats-section">
          <div className="stats-container">
            {stats.map((stat) => (
              <div className="stat-item" key={stat.label}>
                <strong>{stat.value}</strong>
                <span>{stat.label}</span>
              </div>
            ))}
          </div>
        </section>

        {/* ABOUT */}
        <section id="about" className="content-section about-section">
          <div className="section-container two-column">
            <div>
              <div className="section-eyebrow">WHY PREDICTGUARD</div>
              <h2>
                Move from reactive maintenance to
                <span> predictive decisions.</span>
              </h2>
            </div>

            <div className="section-copy">
              <p>
                Industrial equipment generates enormous amounts of operational
                data. PredictGuard transforms that data into a continuous view
                of machine health.
              </p>
              <p>
                Instead of waiting for equipment to fail, maintenance teams can
                identify abnormal behavior, investigate risk factors, and
                prioritize the machines that need attention.
              </p>

              <button className="text-button">
                Discover PredictGuard
                <ArrowRight size={17} />
              </button>
            </div>
          </div>
        </section>

        {/* HOW IT WORKS */}
        <section id="how-it-works" className="dark-section">
          <div className="section-container">
            <div className="section-heading centered">
              <div className="section-eyebrow light">HOW IT WORKS</div>
              <h2>
                From machine telemetry to
                <span> maintenance intelligence.</span>
              </h2>
              <p>
                PredictGuard connects your production environment to a
                continuous intelligence pipeline.
              </p>
            </div>

            <div className="process-grid">
              <div className="process-card">
                <span className="process-number">01</span>
                <Network size={25} />
                <h3>Connect</h3>
                <p>
                  Connect machines, sensors, PLCs, gateways, and industrial
                  systems.
                </p>
              </div>

              <div className="process-card">
                <span className="process-number">02</span>
                <Zap size={25} />
                <h3>Stream</h3>
                <p>
                  Collect and process machine telemetry continuously through a
                  reliable ingestion layer.
                </p>
              </div>

              <div className="process-card">
                <span className="process-number">03</span>
                <Sparkles size={25} />
                <h3>Analyze</h3>
                <p>
                  Machine-learning models analyze operating conditions and
                  identify abnormal behavior.
                </p>
              </div>

              <div className="process-card">
                <span className="process-number">04</span>
                <ShieldCheck size={25} />
                <h3>Act</h3>
                <p>
                  Receive predictions, risk factors, alerts, and maintenance
                  recommendations.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* FEATURES */}
        <section id="features" className="content-section">
          <div className="section-container">
            <div className="section-heading">
              <div className="section-eyebrow">PLATFORM CAPABILITIES</div>
              <h2>
                Intelligence built around
                <span> machine health.</span>
              </h2>
              <p>
                Everything your maintenance team needs to understand equipment
                condition and make faster decisions.
              </p>
            </div>

            <div className="capability-grid">
              {capabilities.map((capability) => {
                const Icon = capability.icon;

                return (
                  <article className="capability-card" key={capability.title}>
                    <div className="capability-icon">
                      <Icon size={22} />
                    </div>
                    <h3>{capability.title}</h3>
                    <p>{capability.text}</p>
                    <button className="card-link">
                      Learn more <ArrowRight size={15} />
                    </button>
                  </article>
                );
              })}
            </div>
          </div>
        </section>

        {/* DEMO */}
        <section id="demo" className="demo-section">
          <div className="section-container">
            <div className="demo-copy">
              <div className="section-eyebrow">SEE IT IN ACTION</div>
              <h2>
                One operational view for your
                <span> production floor.</span>
              </h2>
              <p>
                Monitor machine condition, investigate risk, and understand
                where your maintenance team should focus next.
              </p>

              <button className="primary-button">
                Request Access
                <ArrowRight size={17} />
              </button>
            </div>

            <div className="demo-panel">
              <div className="demo-panel-header">
                <div>
                  <span>PredictGuard</span>
                  <strong>Production Floor</strong>
                </div>
                <span className="demo-online">
                  <span />
                  Systems operational
                </span>
              </div>

              <div className="demo-chart">
                <div className="chart-label">Machine Risk Trend</div>
                <div className="chart-bars">
                  <span style={{ height: "25%" }} />
                  <span style={{ height: "34%" }} />
                  <span style={{ height: "29%" }} />
                  <span style={{ height: "42%" }} />
                  <span style={{ height: "37%" }} />
                  <span style={{ height: "54%" }} />
                  <span style={{ height: "48%" }} />
                  <span style={{ height: "71%" }} />
                  <span style={{ height: "64%" }} />
                  <span style={{ height: "88%" }} />
                  <span style={{ height: "76%" }} />
                  <span style={{ height: "95%" }} />
                </div>
              </div>

              <div className="demo-alert">
                <div className="alert-icon">
                  <Factory size={19} />
                </div>
                <div>
                  <strong>CNC-004 requires attention</strong>
                  <span>Failure risk detected · 99.7%</span>
                </div>
                <ChevronRight size={18} />
              </div>
            </div>
          </div>
        </section>

        {/* INDUSTRIES */}
        <section className="industry-section">
          <div className="section-container">
            <div className="section-heading centered">
              <div className="section-eyebrow">BUILT FOR INDUSTRY</div>
              <h2>
                Designed for environments where
                <span> uptime matters.</span>
              </h2>
            </div>

            <div className="industry-grid">
              {industries.map((industry) => (
                <div className="industry-card" key={industry}>
                  <Factory size={20} />
                  <span>{industry}</span>
                  <ArrowRight size={16} />
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* PRICING */}
        <section id="pricing" className="pricing-section">
          <div className="section-container pricing-container">
            <div>
              <div className="section-eyebrow">PREDICTGUARD</div>
              <h2>
                Start building a more
                <span> predictable production floor.</span>
              </h2>
              <p>
                Flexible subscription plans designed for industrial teams
                scaling from a single production line to multiple facilities.
              </p>
            </div>

            <div className="pricing-card">
              <div className="pricing-card-top">
                <span>Professional</span>
                <strong>12 / 24 months</strong>
              </div>

              <ul>
                <li>
                  <CheckCircle2 size={17} /> Real-time monitoring
                </li>
                <li>
                  <CheckCircle2 size={17} /> Predictive maintenance
                </li>
                <li>
                  <CheckCircle2 size={17} /> AI failure prediction
                </li>
                <li>
                  <CheckCircle2 size={17} /> Telemetry analytics
                </li>
                <li>
                  <CheckCircle2 size={17} /> Alerts and reports
                </li>
              </ul>

              <button className="primary-button pricing-button">
                Get Started
                <ArrowRight size={17} />
              </button>
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="cta-section">
          <div className="cta-container">
            <div>
              <div className="section-eyebrow light">PREDICT WHAT'S NEXT</div>
              <h2>Make machine health a decision, not a guess.</h2>
            </div>

            <button className="light-button">
              Request Access
              <ArrowRight size={17} />
            </button>
          </div>
        </section>
      </main>

      {/* FOOTER */}
      <footer className="landing-footer">
        <div className="footer-container">
          <div className="footer-brand">
            <div className="brand">
              <span className="brand-mark">
                <span />
                <span />
                <span />
              </span>
              <span className="brand-name">PredictGuard</span>
            </div>
            <p>Industrial Predictive Intelligence.</p>
          </div>

          <div className="footer-links">
            <div>
              <strong>Product</strong>
              <button onClick={() => scrollTo("features")}>Features</button>
              <button onClick={() => scrollTo("demo")}>Demo</button>
              <button onClick={() => scrollTo("pricing")}>Pricing</button>
            </div>

            <div>
              <strong>Company</strong>
              <button onClick={() => scrollTo("about")}>About</button>
              <button>Customers</button>
              <button>Contact</button>
            </div>

            <div>
              <strong>Legal</strong>
              <button>Privacy Policy</button>
              <button>Terms & Conditions</button>
              <button>Subscription Policy</button>
            </div>
          </div>
        </div>

        <div className="footer-bottom">
          <span>© 2026 PredictGuard. All rights reserved.</span>
          <span>Industrial Predictive Intelligence</span>
        </div>
      </footer>
    </div>
  );
}

export default LandingPage;
