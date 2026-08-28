import { useEffect, useMemo, useState } from "react";
import { LogOut, RefreshCw } from "lucide-react";
import { Link } from "react-router-dom";

import { apiRequest } from "../services/api";
import { useAuth } from "../context/AuthContext";

import "./Dashboard.css";

function Status({ status }) {
  const normalized = String(status || "UNKNOWN").toUpperCase();

  return (
    <span className={`status status-${normalized.toLowerCase()}`}>
      <span className="status-dot" />
      {normalized}
    </span>
  );
}

function formatValue(value, suffix = "") {
  if (value === null || value === undefined || value === "") {
    return "—";
  }

  const numeric = Number(value);

  if (Number.isFinite(numeric)) {
    return `${numeric.toFixed(2)}${suffix}`;
  }

  return `${value}${suffix}`;
}

function formatTime(value) {
  if (!value) return "—";

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return "—";
  }

  return date.toLocaleTimeString("en-IN", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
}

function buildTelemetryMap(records) {
  const result = {
    temperature: null,
    pressure: null,
    humidity: null,
    vibration: null,
    rpm: null,
    timestamp: null,
  };

  if (!Array.isArray(records)) {
    return result;
  }

  for (const record of records) {
    if (Object.prototype.hasOwnProperty.call(result, record.field)) {
      result[record.field] = record.value;

      if (record.time) {
        result.timestamp = record.time;
      }
    }
  }

  return result;
}

export default function Dashboard() {
  const { logout } = useAuth();

  const [user, setUser] = useState(null);
  const [machines, setMachines] = useState([]);
  const [telemetry, setTelemetry] = useState({});

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadDashboard = async () => {
    setLoading(true);
    setError("");

    try {
      const [userData, machineData] = await Promise.all([
        apiRequest("/api/v1/users/me"),
        apiRequest("/api/v1/machines/"),
      ]);

      const machineList = Array.isArray(machineData)
        ? machineData
        : [];

      const telemetryEntries = await Promise.all(
        machineList.map(async (machine) => {
          try {
            const records = await apiRequest(
              `/api/v1/telemetry/latest/${machine.id}`
            );

            return [
              machine.id,
              buildTelemetryMap(records),
            ];
          } catch {
            return [
              machine.id,
              buildTelemetryMap([]),
            ];
          }
        })
      );

      setUser(userData);
      setMachines(machineList);
      setTelemetry(
        Object.fromEntries(telemetryEntries)
      );
    } catch (err) {
      setError(
        err.message ||
          "Unable to load your PredictGuard workspace."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboard();

    const interval = setInterval(() => {
      loadDashboard();
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const counts = useMemo(() => {
    return machines.reduce(
      (result, machine) => {
        const status = String(
          machine.status || "NORMAL"
        ).toUpperCase();

        if (status === "CRITICAL") {
          result.critical += 1;
        } else if (
          status === "WARNING" ||
          status === "WARN"
        ) {
          result.warning += 1;
        } else {
          result.normal += 1;
        }

        return result;
      },
      {
        normal: 0,
        warning: 0,
        critical: 0,
      }
    );
  }, [machines]);

  return (
    <div className="dashboard">
      <aside className="sidebar">
        <div className="brand">
          PredictGuard
        </div>

        <div className="plant-section">
          <div className="sidebar-label">
            WORKSPACE
          </div>

          <div className="plant-selector">
            <div>
              <strong>
                {user?.name || "PredictGuard Admin"}
              </strong>

              <small>
                {user?.email || "Loading..."}
              </small>
            </div>
          </div>
        </div>

        <nav className="navigation">
          <div className="nav-group">
            <div className="nav-heading">
              OPERATIONS
            </div>

            <div className="nav-item active">
              Overview
            </div>

            <Link
              to="/app/assets"
              className="nav-item"
            >
              Assets
            </Link>

            <div className="nav-item alarm-item">
              <span>Alarms</span>

              <span className="alarm-badge">
                {counts.warning + counts.critical}
              </span>
            </div>
          </div>

          <div className="nav-group">
            <div className="nav-heading">
              ANALYSIS
            </div>

            <div className="nav-item">
              Telemetry
            </div>

            <div className="nav-item">
              Predictions
            </div>

            <div className="nav-item">
              Reports
            </div>
          </div>

          <div className="nav-group">
            <div className="nav-heading">
              SYSTEM
            </div>

            <div className="nav-item">
              Settings
            </div>
          </div>
        </nav>

        <div className="sidebar-footer">
          <button
            className="logout-button"
            onClick={logout}
          >
            <LogOut size={16} />
            Sign out
          </button>
        </div>
      </aside>

      <main className="main-content">
        <header className="page-header">
          <div>
            <h1>Production Floor</h1>

            <p>
              {user?.role
                ? `${user.role} workspace`
                : "Predictive maintenance overview"}
            </p>
          </div>

          <button
            className="refresh-button"
            onClick={loadDashboard}
            disabled={loading}
          >
            <RefreshCw
              size={16}
              className={loading ? "spin" : ""}
            />

            {loading
              ? "Refreshing..."
              : "Refresh"}
          </button>
        </header>

        {error && (
          <div className="dashboard-error">
            <div>
              <strong>
                Unable to load dashboard
              </strong>

              <span>{error}</span>
            </div>

            <button onClick={loadDashboard}>
              Retry
            </button>
          </div>
        )}

        <section className="kpi-grid">
          <div className="kpi-card">
            <div className="kpi-title">
              CONNECTED ASSETS
            </div>

            <div className="kpi-value">
              {loading ? "—" : machines.length}
            </div>
          </div>

          <div className="kpi-card normal-card">
            <div className="kpi-title">
              NORMAL
            </div>

            <div className="kpi-value normal-value">
              {loading ? "—" : counts.normal}
            </div>
          </div>

          <div className="kpi-card warning-card">
            <div className="kpi-title">
              WARNING
            </div>

            <div className="kpi-value warning-value">
              {loading ? "—" : counts.warning}
            </div>
          </div>

          <div className="kpi-card critical-card">
            <div className="kpi-title">
              CRITICAL
            </div>

            <div className="kpi-value critical-value">
              {loading ? "—" : counts.critical}
            </div>
          </div>
        </section>

        <section className="machine-panel">
          <div className="panel-header">
            <div>
              <h2>Machine Condition</h2>

              <p>
                Live telemetry from your connected
                production assets
              </p>
            </div>
          </div>

          {loading ? (
            <div className="dashboard-loading">
              <RefreshCw
                size={20}
                className="spin"
              />

              Loading machine telemetry...
            </div>
          ) : machines.length === 0 ? (
            <div className="dashboard-empty">
              <h3>No machines connected</h3>

              <p>
                Add a machine to begin monitoring your
                production assets.
              </p>
            </div>
          ) : (
            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>MACHINE</th>
                    <th>STATUS</th>
                    <th>TEMP.</th>
                    <th>HUMIDITY</th>
                    <th>PRESSURE</th>
                    <th>VIBRATION</th>
                    <th>RPM</th>
                    <th>LAST SEEN</th>
                  </tr>
                </thead>

                <tbody>
                  {machines.map((machine) => {
                    const current =
                      telemetry[machine.id] ||
                      buildTelemetryMap([]);

                    return (
                      <tr key={machine.id}>
                        <td>
                          <div className="machine-name">
                            {machine.machine_name}
                          </div>

                          <div className="machine-line">
                            Asset #{machine.id}
                          </div>
                        </td>

                        <td>
                          <Status
                            status={machine.status}
                          />
                        </td>

                        <td>
                          {formatValue(
                            current.temperature,
                            " °C"
                          )}
                        </td>

                        <td>
                          {formatValue(
                            current.humidity,
                            " %"
                          )}
                        </td>

                        <td>
                          {formatValue(
                            current.pressure,
                            " hPa"
                          )}
                        </td>

                        <td>
                          {formatValue(
                            current.vibration
                          )}
                        </td>

                        <td>
                          {current.rpm ?? "—"}
                        </td>

                        <td>
                          {formatTime(
                            current.timestamp
                          )}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
