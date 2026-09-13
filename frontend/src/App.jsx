import { useEffect, useState } from "react";
import "./index.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [servers, setServers] = useState([]);
  const [latestMetric, setLatestMetric] = useState(null);
  const [incidents, setIncidents] = useState([]);
  const [deployments, setDeployments] = useState([]);
  const [aiAnalysis, setAiAnalysis] = useState(null);
  const [error, setError] = useState("");

  // Load all dashboard data
  const loadData = async () => {
    try {
      const [
        serversResponse,
        metricsResponse,
        incidentsResponse,
        deploymentsResponse,
        aiResponse,
      ] = await Promise.all([
        fetch(`${API_URL}/servers`),
        fetch(`${API_URL}/metrics/latest`),
        fetch(`${API_URL}/incidents`),
        fetch(`${API_URL}/deployments`),
        fetch(`${API_URL}/ai-analysis`),
      ]);

      if (!serversResponse.ok) {
        throw new Error("Failed to load servers");
      }

      if (!metricsResponse.ok) {
        throw new Error("Failed to load metrics");
      }

      if (!incidentsResponse.ok) {
        throw new Error("Failed to load incidents");
      }

      if (!deploymentsResponse.ok) {
        throw new Error("Failed to load deployments");
      }

      if (!aiResponse.ok) {
        throw new Error("Failed to load AI analysis");
      }

      const serversData = await serversResponse.json();
      const metricsData = await metricsResponse.json();
      const incidentsData = await incidentsResponse.json();
      const deploymentsData = await deploymentsResponse.json();
      const aiAnalysisData = await aiResponse.json();

      setServers(Array.isArray(serversData) ? serversData : []);
      setIncidents(Array.isArray(incidentsData) ? incidentsData : []);
      setDeployments(
        Array.isArray(deploymentsData) ? deploymentsData : []
      );

      // Handle "No metrics available"
      if (
        metricsData &&
        metricsData.cpu_usage !== undefined &&
        metricsData.memory_usage !== undefined &&
        metricsData.disk_usage !== undefined
      ) {
        setLatestMetric(metricsData);
      } else {
        setLatestMetric(null);
      }

      setAiAnalysis(aiAnalysisData);
      setError("");
    } catch (err) {
      console.error("Dashboard error:", err);
      setError("Unable to connect to AIOpsHub backend.");
    }
  };

  useEffect(() => {
    loadData();

    const interval = setInterval(() => {
      loadData();
    }, 10000);

    return () => clearInterval(interval);
  }, []);

  // First server
  const server = servers.length > 0 ? servers[0] : null;

  // Open incidents
  const openIncidents = incidents.filter(
    (incident) => incident.status === "open"
  );

  // Metric status
  const getMetricStatus = (value, warning, critical) => {
    const numberValue = Number(value);

    if (Number.isNaN(numberValue)) {
      return "Unknown";
    }

    if (numberValue >= critical) {
      return "Critical";
    }

    if (numberValue >= warning) {
      return "Warning";
    }

    return "Normal";
  };

  // Collect metrics
  const collectMetrics = async () => {
    try {
      setError("");

      const response = await fetch(`${API_URL}/metrics/collect`, {
        method: "POST",
      });

      if (!response.ok) {
        throw new Error("Failed to collect metrics");
      }

      // Reload dashboard data after collecting metrics
      await loadData();
    } catch (err) {
      console.error("Metrics collection error:", err);
      setError("Unable to collect metrics.");
    }
  };

  // Resolve incident
  const resolveIncident = async (incidentId) => {
    try {
      const response = await fetch(
        `${API_URL}/incidents/${incidentId}/resolve`,
        {
          method: "PUT",
        }
      );

      if (!response.ok) {
        throw new Error("Failed to resolve incident");
      }

      await loadData();
    } catch (err) {
      console.error("Resolve incident error:", err);
      setError("Unable to resolve incident.");
    }
  };

  return (
    <div className="dashboard">

      {/* HEADER */}

      <header className="header">
        <h1>AIOpsHub</h1>

        <p>
          AI-Powered DevOps Monitoring and Deployment System
        </p>
      </header>

      <main className="container">

        {/* ERROR MESSAGE */}

        {error && (
          <div className="card">
            <p>{error}</p>
          </div>
        )}

        {/* DEPLOYMENT HISTORY */}

        <div className="server-section">

          <h2>Deployment History</h2>

          {deployments.length === 0 ? (
            <div className="card">
              <p>No deployments available.</p>
            </div>
          ) : (
            deployments.map((deployment) => (
              <div
                className="card deployment-card"
                key={deployment.id}
              >

                <h3>
                  {deployment.application_name || "Unknown Application"}
                </h3>

                <p>
                  Version:{" "}
                  <strong>
                    {deployment.version || "Unknown"}
                  </strong>
                </p>

                <p>
                  Server ID:{" "}
                  {deployment.server_id ?? "N/A"}
                </p>

                <p>
                  Status:{" "}
                  <strong className="deployment-status">
                    {(deployment.status || "unknown").toUpperCase()}
                  </strong>
                </p>

                <p>
                  Deployed At:{" "}
                  {deployment.deployed_at
                    ? new Date(
                        deployment.deployed_at
                      ).toLocaleString()
                    : "N/A"}
                </p>

              </div>
            ))
          )}

        </div>

        {/* SYSTEM METRICS */}

        <h2 className="section-title">
          System Metrics
        </h2>

        <button
          className="collect-button"
          onClick={collectMetrics}
        >
          Collect Metrics
        </button>

        <div className="metrics">

          {/* CPU */}

          <div className="card">

            <h3>CPU Usage</h3>

            <div className="metric-value">

              {latestMetric?.cpu_usage !== undefined
                ? `${latestMetric.cpu_usage}%`
                : "No data"}

            </div>

            {latestMetric?.cpu_usage !== undefined && (
              <p
                className={`metric-status ${getMetricStatus(
                  latestMetric.cpu_usage,
                  70,
                  90
                ).toLowerCase()}`}
              >
                {getMetricStatus(
                  latestMetric.cpu_usage,
                  70,
                  90
                )}
              </p>
            )}

          </div>

          {/* MEMORY */}

          <div className="card">

            <h3>Memory Usage</h3>

            <div className="metric-value">

              {latestMetric?.memory_usage !== undefined
                ? `${latestMetric.memory_usage}%`
                : "No data"}

            </div>

            {latestMetric?.memory_usage !== undefined && (
              <p
                className={`metric-status ${getMetricStatus(
                  latestMetric.memory_usage,
                  70,
                  90
                ).toLowerCase()}`}
              >
                {getMetricStatus(
                  latestMetric.memory_usage,
                  70,
                  90
                )}
              </p>
            )}

          </div>

          {/* DISK */}

          <div className="card">

            <h3>Disk Usage</h3>

            <div className="metric-value">

              {latestMetric?.disk_usage !== undefined
                ? `${latestMetric.disk_usage}%`
                : "No data"}

            </div>

            {latestMetric?.disk_usage !== undefined && (
              <p
                className={`metric-status ${getMetricStatus(
                  latestMetric.disk_usage,
                  80,
                  90
                ).toLowerCase()}`}
              >
                {getMetricStatus(
                  latestMetric.disk_usage,
                  80,
                  90
                )}
              </p>
            )}

          </div>

        </div>

        {/* AI ANALYSIS */}

        <div className="server-section">

          <h2>
            AI Analysis & Recommendations
          </h2>

          <div className="card">

            {!aiAnalysis ? (
              <p>
                Loading AI analysis...
              </p>
            ) : aiAnalysis.recommendations &&
              Array.isArray(aiAnalysis.recommendations) &&
              aiAnalysis.recommendations.length > 0 ? (

              <ul>

                {aiAnalysis.recommendations.map(
                  (recommendation, index) => (
                    <li key={index}>
                      {recommendation}
                    </li>
                  )
                )}

              </ul>

            ) : (
              <p>
                No recommendations available.
              </p>
            )}

          </div>

        </div>

        {/* SERVER STATUS */}

        <div className="server-section">

          <h2>
            Server Status
          </h2>

          <div className="card">

            {server ? (
              <>

                <h3>
                  {server.name || "Unknown Server"}
                </h3>

                <p className="status-online">
                  ●{" "}
                  {(server.status || "unknown").toUpperCase()}
                </p>

                <p>
                  Environment:{" "}
                  {server.environment || "N/A"}
                </p>

                <p>
                  IP Address:{" "}
                  {server.ip_address || "N/A"}
                </p>

              </>
            ) : (
              <p>
                No server information available.
              </p>
            )}

          </div>

        </div>

        {/* OPEN INCIDENTS */}

        <div className="server-section">

          <h2>
            Open Incidents
          </h2>

          {openIncidents.length === 0 ? (

            <div className="card">

              <p>
                No open incidents 🎉
              </p>

            </div>

          ) : (

            openIncidents.map((incident) => (

              <div
                className="card incident"
                key={incident.id}
              >

                <div className="incident-title">
                  {incident.title || "Untitled Incident"}
                </div>

                <p>
                  {incident.description ||
                    "No description available."}
                </p>

                <p className="high">
                  Severity:{" "}
                  {(incident.severity || "unknown").toUpperCase()}
                </p>

                <p>
                  Status:{" "}
                  {(incident.status || "unknown").toUpperCase()}
                </p>

                <button
                  className="resolve-button"
                  onClick={() =>
                    resolveIncident(incident.id)
                  }
                >
                  Resolve Incident
                </button>

              </div>

            ))

          )}

        </div>

      </main>

    </div>
  );
}

export default App;