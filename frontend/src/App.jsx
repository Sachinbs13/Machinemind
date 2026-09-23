import { useState } from "react";
import PredictionForm from "./PredictionForm";
import PredictionResult from "./PredictionResult";
import PredictionHistory from "./PredictionHistory";
import "./App.css";

function App() {
  const [formData, setFormData] = useState({
    machine_id: "",
    air_temperature: "",
    process_temperature: "",
    rotational_speed: "",
    torque: "",
    tool_wear: "",
    type: "M",
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  function handleChange(e) {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch("http://127.0.0.1:8001/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          machine_id: formData.machine_id,
          air_temperature: parseFloat(formData.air_temperature),
          process_temperature: parseFloat(formData.process_temperature),
          rotational_speed: parseFloat(formData.rotational_speed),
          torque: parseFloat(formData.torque),
          tool_wear: parseFloat(formData.tool_wear),
          type: formData.type,
        }),
      });

      if (!response.ok) throw new Error("Prediction request failed");

      const data = await response.json();
      setResult(data);
      setRefreshKey((prev) => prev + 1);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app-container">
      <h1>MachineMind</h1>
      <p className="subtitle">Predictive Maintenance & Machine Intelligence</p>

      <PredictionForm formData={formData} onChange={handleChange} onSubmit={handleSubmit} loading={loading} />
      {error && <p className="error-text">{error}</p>}
      <PredictionResult result={result} />
      <PredictionHistory refreshKey={refreshKey} />
    </div>
  );
}

export default App;