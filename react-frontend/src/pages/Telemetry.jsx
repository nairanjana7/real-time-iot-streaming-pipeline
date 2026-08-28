import { useCallback, useEffect, useMemo, useState } from "react";
import { Activity, ArrowLeft, RefreshCw, LogOut } from "lucide-react";
import { Link } from "react-router-dom";

import { apiRequest } from "../services/api";
import { useAuth } from "../context/AuthContext";

import "./Telemetry.css";

function formatTime(value) {
  if (!value) return "—";

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) return "—";

  return date.toLocaleString();
}

function getTelemetryMap(records) {
  if (!Array.isArray(records)) return {};

  return records.reduce((result, record) => {
    if (record?.field) {
      result[record.field] = {
        value: record.value,
        time: record.time,
      };
    }

    return result;
  }, {});
}

function MetricCard({ label, value, unit }) {
  return (
    <div className="telemetry-metric">
      <div className="telemetry-metric-label">{label}</div>

      <div className="telemetry-metric-value">
        {value === undefined || value === null ? "—" : value}
        {value !== undefined && value !== null && unit && (
          <span>{unit}</span>
        )}
      </div>
    </div>
  );
}

export default function Telemetry() {
  const { logout } = useAuth();

  const [user, setUser] = useState(null);
  const [machines, setMachines] = useState([]);
  const [selectedMachineId, setSelectedMachineId] = useState("");

  const [telemetry, setTelemetry] = useState({});
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState("");

  const loadPage = useCallback(async () => {
    setError("");

    try {
      const [userData, machineData] = await Promise.all([
        apiRequest("/api/v1/users/me"),
        apiRequest("/api/v1/machines/"),
      ]);

      const machineList = Array.isArray(machineData)
        ? machineData
        : [];

      setUser(userData);
      setMachines(machineList);

      if (machineList.length === 0) {
        setTelemetry({});
        return;
      }

      setSelectedMachineId((current) => {
        if (
          current &&
          machineList.some(
            (machine) => String(machine.id) === String(current)
          )
        ) {
          return current;
        }

        return String(machineList[0].id);
      });
    } catch (err) {
      setError(err.message || "Unable to load telemetry.");
    }
  }, []);

  const loadTelemetry = useCallback(async (machineId, isRefresh = false) => {
    if (!machineId) return;

    if (isRefresh) {
      setRefreshing(true);
    } else {
      setLoading(true);
    }

    setError("");

    try {
      const records = await apiRequest(
        `/api/v1/telemetry/latest/${machineId}`
      );

      setTelemetry(getTelemetryMap(records));
    } catch (err) {
      setError(err.message || "Unable to load telemetry.");
      setTelemetry({});
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    loadPage();
  }, [loadPage]);

  useEffect(() => {
    if (!selectedMachineId) return;

    loadTelemetry(selectedMachineId);

    const interval = setInterval(() => {
      loadTelemetry(selectedMachineId, true);
    }, 5000);

    return () => clearInterval(interval);
  }, [selectedMachineId, loadTelemetry]);

  const selectedMachine = useMemo(
    () =>
      machines.find(
        (machine) =>
          String(machine.id) === String(selectedMachineId)
      ),
    [machines, selectedMachineId]
  );

  const lastUpdated = useMemo(() => {
    const times = Object.values(telemetry)
      .map((item) => item?.time)
      .filter(Boolean)
      .map((time) => new Date(time).getTime())
      .filter((time) => !Number.isNaN(time));

    if (!times.length) return null;

    return new Date(Math.max(...times));
  }, [telemetry]);

  const hasTelemetry = Object.keys(telemetry).length > 0;

  return (
    <div className="telemetry-page">
      <aside className="telemetry-sidebar">
        <div className="telemetry-brand">
          PredictGuard <span>AI</span>
        </div>

        <div className="telemetry-workspace">
          <div className="telemetry-sidebar-label">
            WORKSPACE
          </div>

          <div className="telemetry-user-card">
            <div className="telemetry-avatar">
              {user?.full_name?.charAt(0)?.toUpperCase() || "U"}
            </div>

            <div>
              <strong>
                {user?.full_name || "User"}
              </strong>

              <span>
                {user?.role || "User"}
              </span>
            </div>
          </div>
        </div>

        <nav className="telemetry-navigation">
          <div className="telemetry-nav-heading">
            MONITORING
          </div>

          <Link
            to="/app"
            className="telemetry-nav-item"
          >
            Dashboard
          </Link>

          <Link
            to="/app/assets"
            className="telemetry-nav-item"
          >
            Assets
          </Link>

          <div className="telemetry-nav-item active">
            Telemetry
          </div>

          <div className="telemetry-nav-item disabled">
            Predictions
          </div>

          <div className="telemetry-nav-item disabled">
            Reports
          </div>
        </nav>

        <button
          className="telemetry-logout"
          onClick={logout}
        >
          <LogOut size={17} />
          Sign out
        </button>
      </aside>

      <main className="telemetry-main">
        <header className="telemetry-header">
          <div>
            <div className="telemetry-breadcrumb">
              Monitoring / Telemetry
            </div>

            <h1>Telemetry</h1>

            <p>
              Live operating data from your production assets.
            </p>
          </div>

          <div className="telemetry-header-actions">
            <div className="telemetry-live">
              <span />
              LIVE
            </div>

            <button
              className="telemetry-refresh"
              onClick={() =>
                loadTelemetry(selectedMachineId, true)
              }
              disabled={!selectedMachineId || refreshing}
            >
              <RefreshCw
                size={17}
                className={
                  refreshing ? "telemetry-spin" : ""
                }
              />
              Refresh
            </button>
          </div>
        </header>

        <section className="telemetry-content">
          <div className="telemetry-toolbar">
            <div>
              <label htmlFor="machine-select">
                MACHINE
              </label>

              <select
                id="machine-select"
                value={selectedMachineId}
                onChange={(event) =>
                  setSelectedMachineId(event.target.value)
                }
                disabled={!machines.length}
              >
                {machines.map((machine) => (
                  <option
                    key={machine.id}
                    value={machine.id}
                  >
                    {machine.machine_name} —{" "}
                    {machine.serial_number}
                  </option>
                ))}
              </select>
            </div>

            <div className="telemetry-status">
              <Activity size={17} />

              <div>
                <strong>
                  {selectedMachine?.machine_name ||
                    "No machine selected"}
                </strong>

                <span>
                  {lastUpdated
                    ? `Updated ${formatTime(lastUpdated)}`
                    : "Waiting for telemetry"}
                </span>
              </div>
            </div>
          </div>

          {error && (
            <div className="telemetry-error">
              <strong>Unable to load telemetry</strong>
              <span>{error}</span>

              <button
                onClick={() =>
                  loadTelemetry(selectedMachineId, true)
                }
              >
                Try again
              </button>
            </div>
          )}

          {!error && loading && (
            <div className="telemetry-state">
              <RefreshCw
                size={22}
                className="telemetry-spin"
              />
              <span>Loading telemetry...</span>
            </div>
          )}

          {!error &&
            !loading &&
            machines.length === 0 && (
              <div className="telemetry-state">
                <strong>No machines found</strong>
                <span>
                  Add a production asset before viewing telemetry.
                </span>

                <Link to="/app/assets">
                  Manage assets
                </Link>
              </div>
            )}

          {!error &&
            !loading &&
            machines.length > 0 &&
            !hasTelemetry && (
              <div className="telemetry-state">
                <strong>No telemetry available</strong>
                <span>
                  This machine has not reported any telemetry yet.
                </span>
              </div>
            )}

          {!loading && hasTelemetry && (
            <>
              <div className="telemetry-panel">
                <div className="telemetry-panel-header">
                  <div>
                    <h2>Current operating conditions</h2>
                    <p>
                      Latest recorded values for{" "}
                      {selectedMachine?.machine_name || "machine"}.
                    </p>
                  </div>

                  <div className="telemetry-auto">
                    Auto-refreshing · 5 sec
                  </div>
                </div>

                <div className="telemetry-grid">
                  <MetricCard
                    label="TEMPERATURE"
                    value={telemetry.temperature?.value}
                    unit=" °C"
                  />

                  <MetricCard
                    label="PRESSURE"
                    value={telemetry.pressure?.value}
                    unit=""
                  />

                  <MetricCard
                    label="HUMIDITY"
                    value={telemetry.humidity?.value}
                    unit="%"
                  />

                  <MetricCard
                    label="VIBRATION"
                    value={telemetry.vibration?.value}
                    unit=""
                  />

                  <MetricCard
                    label="RPM"
                    value={telemetry.rpm?.value}
                    unit=" rpm"
                  />
                </div>
              </div>

              <div className="telemetry-detail">
                <div>
                  <span>Machine</span>
                  <strong>
                    {selectedMachine?.machine_name || "—"}
                  </strong>
                </div>

                <div>
                  <span>Serial number</span>
                  <strong>
                    {selectedMachine?.serial_number || "—"}
                  </strong>
                </div>

                <div>
                  <span>Location</span>
                  <strong>
                    {selectedMachine?.location || "—"}
                  </strong>
                </div>

                <div>
                  <span>Last reading</span>
                  <strong>
                    {lastUpdated
                      ? formatTime(lastUpdated)
                      : "—"}
                  </strong>
                </div>
              </div>
            </>
          )}

          <Link
            to="/app"
            className="telemetry-back"
          >
            <ArrowLeft size={17} />
            Back to Dashboard
          </Link>
        </section>
      </main>
    </div>
  );
}
