function PredictionResult({ result }) {
  if (!result) return null;

  const colors = { LOW: "#2e7d32", MEDIUM: "#e6a700", HIGH: "#c62828" };
  const emojis = { LOW: "🟢", MEDIUM: "🟡", HIGH: "🔴" };
  const color = colors[result.risk_level];
  const probabilityPercent = (result.probability * 100).toFixed(2);

  return (
    <div className="card result-card" style={{ borderColor: color }}>
      <h2>Prediction Result</h2>
      <p className="machine-id">Machine: {result.machine_id}</p>

      <h3 style={{ color }}>
        {emojis[result.risk_level]} {result.risk_level} RISK
      </h3>

      <p>Predicted Failure: <strong>{result.prediction === 1 ? "YES" : "NO"}</strong></p>
      <p>Prediction Probability: <strong>{probabilityPercent}%</strong></p>

      <div className="probability-bar-track">
        <div
          className="probability-bar-fill"
          style={{ width: `${probabilityPercent}%`, backgroundColor: color }}
        />
      </div>

      <p className="recommended-action">
        <strong>Recommended Action:</strong> {result.recommended_action}
      </p>
    </div>
  );
}

export default PredictionResult;