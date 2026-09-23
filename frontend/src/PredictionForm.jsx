function PredictionForm({ formData, onChange, onSubmit, loading }) {
  return (
    <form onSubmit={onSubmit} className="card">
      <h2>Machine Information</h2>

      <div className="field">
        <label>Machine ID</label>
        <input type="text" name="machine_id" value={formData.machine_id} onChange={onChange} placeholder="e.g. M001" required />
      </div>

      <div className="field">
        <label>Machine Type</label>
        <select name="type" value={formData.type} onChange={onChange}>
          <option value="L">L (Low)</option>
          <option value="M">M (Medium)</option>
          <option value="H">H (High)</option>
        </select>
      </div>

      <h2>Sensor Readings</h2>

      <div className="grid">
        <div className="field">
          <label>Air Temperature (K)</label>
          <input type="number" step="0.1" name="air_temperature" value={formData.air_temperature} onChange={onChange} required />
        </div>
        <div className="field">
          <label>Process Temperature (K)</label>
          <input type="number" step="0.1" name="process_temperature" value={formData.process_temperature} onChange={onChange} required />
        </div>
        <div className="field">
          <label>Rotational Speed (rpm)</label>
          <input type="number" name="rotational_speed" value={formData.rotational_speed} onChange={onChange} required />
        </div>
        <div className="field">
          <label>Torque (Nm)</label>
          <input type="number" step="0.1" name="torque" value={formData.torque} onChange={onChange} required />
        </div>
        <div className="field">
          <label>Tool Wear (min)</label>
          <input type="number" name="tool_wear" value={formData.tool_wear} onChange={onChange} required />
        </div>
      </div>

      <button type="submit" disabled={loading} className="predict-btn">
        {loading ? "Predicting..." : "Predict Failure"}
      </button>
    </form>
  );
}

export default PredictionForm;