import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  ArrowLeft,
  Edit3,
  LogOut,
  Plus,
  RefreshCw,
  Trash2,
  X,
} from "lucide-react";

import { apiRequest } from "../../services/api";
import { useAuth } from "../../context/AuthContext";

import "./Assets.css";

const emptyForm = {
  machine_name: "",
  serial_number: "",
  machine_type: "",
  location: "",
};

function Status({ status }) {
  const normalized = String(status || "NORMAL").toUpperCase();

  return (
    <span className={`status status-${normalized.toLowerCase()}`}>
      <span className="status-dot" />
      {normalized}
    </span>
  );
}

export default function Assets() {
  const { logout } = useAuth();

  const [user, setUser] = useState(null);
  const [machines, setMachines] = useState([]);

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const [error, setError] = useState("");
  const [formError, setFormError] = useState("");

  const [showForm, setShowForm] = useState(false);
  const [editingMachine, setEditingMachine] = useState(null);

  const [form, setForm] = useState(emptyForm);

  const loadAssets = async () => {
    setLoading(true);
    setError("");

    try {
      const [userData, machineData] = await Promise.all([
        apiRequest("/api/v1/users/me"),
        apiRequest("/api/v1/machines/"),
      ]);

      setUser(userData);
      setMachines(Array.isArray(machineData) ? machineData : []);
    } catch (err) {
      setError(err.message || "Unable to load assets.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAssets();
  }, []);

  const openAddForm = () => {
    setEditingMachine(null);
    setForm(emptyForm);
    setFormError("");
    setShowForm(true);
  };

  const openEditForm = (machine) => {
    setEditingMachine(machine);

    setForm({
      machine_name: machine.machine_name || "",
      serial_number: machine.serial_number || "",
      machine_type: machine.machine_type || "",
      location: machine.location || "",
      status: machine.status || "NORMAL",
    });

    setFormError("");
    setShowForm(true);
  };

  const closeForm = () => {
    if (saving) return;

    setShowForm(false);
    setEditingMachine(null);
    setForm(emptyForm);
    setFormError("");
  };

  const handleChange = (event) => {
    const { name, value } = event.target;

    setForm((current) => ({
      ...current,
      [name]: value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    setFormError("");

    if (!form.machine_name.trim()) {
      setFormError("Machine name is required.");
      return;
    }

    if (!editingMachine && !form.serial_number.trim()) {
      setFormError("Serial number is required.");
      return;
    }

    setSaving(true);

    try {
      if (editingMachine) {
        await apiRequest(
          `/api/v1/machines/${editingMachine.id}`,
          {
            method: "PUT",
            body: JSON.stringify({
              machine_name: form.machine_name.trim(),
              machine_type: form.machine_type.trim() || null,
              location: form.location.trim() || null,
              status: form.status || "NORMAL",
            }),
          }
        );
      } else {
        await apiRequest("/api/v1/machines/", {
          method: "POST",
          body: JSON.stringify({
            machine_name: form.machine_name.trim(),
            serial_number: form.serial_number.trim(),
            machine_type: form.machine_type.trim() || null,
            location: form.location.trim() || null,
          }),
        });
      }

      closeForm();
      await loadAssets();
    } catch (err) {
      setFormError(
        err.message ||
          `Unable to ${editingMachine ? "update" : "create"} machine.`
      );
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (machine) => {
    const confirmed = window.confirm(
      `Delete "${machine.machine_name}"?\n\nThis action cannot be undone.`
    );

    if (!confirmed) return;

    setError("");

    try {
      await apiRequest(`/api/v1/machines/${machine.id}`, {
        method: "DELETE",
      });

      await loadAssets();
    } catch (err) {
      setError(err.message || "Unable to delete machine.");
    }
  };

  const formatDate = (value) => {
    if (!value) return "—";

    const date = new Date(value);

    if (Number.isNaN(date.getTime())) {
      return "—";
    }

    return date.toLocaleDateString("en-IN", {
      day: "2-digit",
      month: "short",
      year: "numeric",
    });
  };

  return (
    <div className="assets-page">
      <aside className="assets-sidebar">
        <div className="assets-brand">
          PredictGuard
        </div>

        <div className="assets-workspace">
          <div className="assets-sidebar-label">
            WORKSPACE
          </div>

          <div className="assets-user-card">
            <strong>
              {user?.name || user?.full_name || "PredictGuard Admin"}
            </strong>

            <small>
              {user?.email || "Loading..."}
            </small>
          </div>
        </div>

        <nav className="assets-navigation">
          <div className="assets-nav-group">
            <div className="assets-nav-heading">
              OPERATIONS
            </div>

            <Link
              to="/app"
              className="assets-nav-item"
            >
              Overview
            </Link>

            <div className="assets-nav-item active">
              Assets
            </div>

            <div className="assets-nav-item">
              <span>Alarms</span>
              <span className="assets-alarm-badge">
                0
              </span>
            </div>
          </div>

          <div className="assets-nav-group">
            <div className="assets-nav-heading">
              ANALYSIS
            </div>

            <div className="assets-nav-item">
              Telemetry
            </div>

            <div className="assets-nav-item">
              Predictions
            </div>

            <div className="assets-nav-item">
              Reports
            </div>
          </div>

          <div className="assets-nav-group">
            <div className="assets-nav-heading">
              SYSTEM
            </div>

            <div className="assets-nav-item">
              Settings
            </div>
          </div>
        </nav>

        <div className="assets-sidebar-footer">
          <button
            className="assets-logout"
            onClick={logout}
          >
            <LogOut size={16} />
            Sign out
          </button>
        </div>
      </aside>

      <main className="assets-main">
        <header className="assets-header">
          <div>
            <div className="assets-breadcrumb">
              <Link to="/app">
                <ArrowLeft size={15} />
                Production Floor
              </Link>
            </div>

            <h1>Assets</h1>

            <p>
              Manage the machines connected to your workspace.
            </p>
          </div>

          <div className="assets-header-actions">
            <button
              className="assets-refresh"
              onClick={loadAssets}
              disabled={loading}
            >
              <RefreshCw
                size={16}
                className={loading ? "assets-spin" : ""}
              />
              {loading ? "Refreshing..." : "Refresh"}
            </button>

            <button
              className="assets-add"
              onClick={openAddForm}
            >
              <Plus size={17} />
              Add machine
            </button>
          </div>
        </header>

        {error && (
          <div className="assets-error">
            <div>
              <strong>Unable to load assets</strong>
              <span>{error}</span>
            </div>

            <button onClick={loadAssets}>
              Retry
            </button>
          </div>
        )}

        <section className="assets-summary">
          <div>
            <span>CONNECTED ASSETS</span>
            <strong>{loading ? "—" : machines.length}</strong>
          </div>

          <div>
            <span>NORMAL</span>
            <strong className="summary-normal">
              {loading
                ? "—"
                : machines.filter(
                    (machine) =>
                      String(machine.status).toUpperCase() ===
                      "NORMAL"
                  ).length}
            </strong>
          </div>

          <div>
            <span>WARNING</span>
            <strong className="summary-warning">
              {loading
                ? "—"
                : machines.filter((machine) => {
                    const status = String(
                      machine.status
                    ).toUpperCase();

                    return status === "WARNING" || status === "WARN";
                  }).length}
            </strong>
          </div>

          <div>
            <span>CRITICAL</span>
            <strong className="summary-critical">
              {loading
                ? "—"
                : machines.filter(
                    (machine) =>
                      String(machine.status).toUpperCase() ===
                      "CRITICAL"
                  ).length}
            </strong>
          </div>
        </section>

        <section className="assets-panel">
          <div className="assets-panel-header">
            <div>
              <h2>Machine inventory</h2>
              <p>
                All production assets registered to your company.
              </p>
            </div>

            <span className="asset-count">
              {machines.length}{" "}
              {machines.length === 1 ? "asset" : "assets"}
            </span>
          </div>

          {loading ? (
            <div className="assets-loading">
              <RefreshCw size={20} className="assets-spin" />
              Loading assets...
            </div>
          ) : machines.length === 0 ? (
            <div className="assets-empty">
              <div className="assets-empty-icon">
                <Plus size={22} />
              </div>

              <h3>No machines connected</h3>

              <p>
                Register your first production machine to begin
                monitoring its condition.
              </p>

              <button
                className="assets-add"
                onClick={openAddForm}
              >
                <Plus size={17} />
                Add your first machine
              </button>
            </div>
          ) : (
            <div className="assets-table-wrapper">
              <table className="assets-table">
                <thead>
                  <tr>
                    <th>MACHINE</th>
                    <th>STATUS</th>
                    <th>SERIAL NUMBER</th>
                    <th>TYPE</th>
                    <th>LOCATION</th>
                    <th>INSTALLED</th>
                    <th>ACTIONS</th>
                  </tr>
                </thead>

                <tbody>
                  {machines.map((machine) => (
                    <tr key={machine.id}>
                      <td>
                        <div className="asset-machine-name">
                          {machine.machine_name}
                        </div>

                        <div className="asset-machine-id">
                          Asset #{machine.id}
                        </div>
                      </td>

                      <td>
                        <Status status={machine.status} />
                      </td>

                      <td>
                        {machine.serial_number || "—"}
                      </td>

                      <td>
                        {machine.machine_type || "—"}
                      </td>

                      <td>
                        {machine.location || "—"}
                      </td>

                      <td>
                        {formatDate(machine.installed_at)}
                      </td>

                      <td>
                        <div className="asset-actions">
                          <button
                            className="icon-button edit-button"
                            title="Edit machine"
                            onClick={() =>
                              openEditForm(machine)
                            }
                          >
                            <Edit3 size={15} />
                          </button>

                          <button
                            className="icon-button delete-button"
                            title="Delete machine"
                            onClick={() =>
                              handleDelete(machine)
                            }
                          >
                            <Trash2 size={15} />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </main>

      {showForm && (
        <div
          className="asset-modal-overlay"
          onMouseDown={(event) => {
            if (event.target === event.currentTarget) {
              closeForm();
            }
          }}
        >
          <div className="asset-modal">
            <div className="asset-modal-header">
              <div>
                <h2>
                  {editingMachine
                    ? "Edit machine"
                    : "Add machine"}
                </h2>

                <p>
                  {editingMachine
                    ? "Update the machine information."
                    : "Register a production asset in your workspace."}
                </p>
              </div>

              <button
                className="modal-close"
                onClick={closeForm}
                disabled={saving}
              >
                <X size={20} />
              </button>
            </div>

            <form
              className="asset-form"
              onSubmit={handleSubmit}
            >
              <div className="form-grid">
                <div className="form-field full-width">
                  <label htmlFor="machine_name">
                    Machine name
                  </label>

                  <input
                    id="machine_name"
                    name="machine_name"
                    value={form.machine_name}
                    onChange={handleChange}
                    placeholder="e.g. CNC Milling Machine 01"
                    required
                  />
                </div>

                <div className="form-field">
                  <label htmlFor="serial_number">
                    Serial number
                  </label>

                  <input
                    id="serial_number"
                    name="serial_number"
                    value={form.serial_number}
                    onChange={handleChange}
                    placeholder="e.g. CNC-2026-001"
                    disabled={Boolean(editingMachine)}
                    required={!editingMachine}
                  />

                  {editingMachine && (
                    <small>
                      Serial number cannot be changed.
                    </small>
                  )}
                </div>

                <div className="form-field">
                  <label htmlFor="machine_type">
                    Machine type
                  </label>

                  <input
                    id="machine_type"
                    name="machine_type"
                    value={form.machine_type}
                    onChange={handleChange}
                    placeholder="e.g. CNC, Pump, Motor"
                  />
                </div>

                <div className="form-field">
                  <label htmlFor="location">
                    Location
                  </label>

                  <input
                    id="location"
                    name="location"
                    value={form.location}
                    onChange={handleChange}
                    placeholder="e.g. Plant 1, Line A"
                  />
                </div>

                {editingMachine && (
                  <div className="form-field">
                    <label htmlFor="status">
                      Status
                    </label>

                    <select
                      id="status"
                      name="status"
                      value={form.status || "NORMAL"}
                      onChange={handleChange}
                    >
                      <option value="NORMAL">
                        Normal
                      </option>
                      <option value="WARNING">
                        Warning
                      </option>
                      <option value="CRITICAL">
                        Critical
                      </option>
                    </select>
                  </div>
                )}
              </div>

              {formError && (
                <div className="form-error">
                  {formError}
                </div>
              )}

              <div className="asset-form-actions">
                <button
                  type="button"
                  className="cancel-button"
                  onClick={closeForm}
                  disabled={saving}
                >
                  Cancel
                </button>

                <button
                  type="submit"
                  className="save-button"
                  disabled={saving}
                >
                  {saving
                    ? "Saving..."
                    : editingMachine
                    ? "Save changes"
                    : "Add machine"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
