import { useState, useEffect } from "react";

function PredictionHistory({ refreshKey }) {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetch("http://127.0.0.1:8001/history?limit=20")
      .then((res) => res.json())
      .then((data) => {
        setRecords(data.records);
        setError(null);
      })
      .catch(() => {
        setError("Failed to load history");
      })
      .finally(() => setLoading(false));
  }, [refreshKey]);

  const riskColor = {
    LOW: "#2e7d32",
    MEDIUM: "#e6a700",
    HIGH: "#c62828",
  };

  if (loading) return <p>Loading history...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;
  if (records.length === 0) return <p>No predictions logged yet.</p>;

  return (
    <div className="card history-card">
      <h2>Recent Predictions</h2>
      <table className="history-table">
        <thead>
          <tr>
            <th>Machine</th>
            <th>Risk</th>
            <th>Probability</th>
            <th>Time</th>
          </tr>
        </thead>
        <tbody>
          {records.map((r) => (
            <tr key={r.id}>
              <td>{r.machine_id}</td>
              <td style={{ color: riskColor[r.risk_level] }}>{r.risk_level}</td>
              <td>{(r.probability * 100).toFixed(1)}%</td>
              <td>{r.predicted_at}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default PredictionHistory;