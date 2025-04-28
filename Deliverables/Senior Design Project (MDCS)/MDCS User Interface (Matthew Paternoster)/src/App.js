// src/App.js
import React, { useState, useEffect } from "react";

const App = () => {
  const [activeTab, setActiveTab] = useState("Drone Feed");
  const [drones, setDrones] = useState([]);
  const [selectedDrone, setSelectedDrone] = useState(1);
  const [videoFeed, setVideoFeed] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const [connectionError, setConnectionError] = useState(null);

  // Fetch drones data
  useEffect(() => {
    const fetchDrones = async () => {
      try {
        const response = await fetch("http://localhost:5000/drones");
        if (response.ok) {
          const data = await response.json();
          setDrones(data);
          setIsConnected(true);
          setConnectionError(null);
        } else {
          throw new Error("Failed to fetch drone data");
        }
      } catch (error) {
        console.error("Error fetching drone data:", error);
        setIsConnected(false);
        setConnectionError("Failed to connect to the AirSim server. Make sure it's running.");
      }
    };

    fetchDrones();
    const interval = setInterval(fetchDrones, 1000); // Update drone data every second

    return () => clearInterval(interval);
  }, []);

  // Set up video feed
  useEffect(() => {
    if (isConnected) {
      setVideoFeed(`http://localhost:5000/video_feed?drone=${selectedDrone}`);
    }
  }, [isConnected, selectedDrone]);

  const handleDroneChange = async (e) => {
    const selectedDroneId = Number(e.target.value);
    setSelectedDrone(selectedDroneId);

    // Send the selected camera to the backend
    try {
      const response = await fetch(`http://localhost:5000/set_camera/${selectedDroneId}`, {
        method: 'POST',
      });
      if (!response.ok) {
        throw new Error("Failed to update camera");
      }
      console.log(`Camera updated to drone ${selectedDroneId}`);
    } catch (error) {
      console.error("Error updating camera:", error);
    }
  };

  const getBatteryColor = (battery) => {
    if (battery > 60) return "green";
    if (battery > 30) return "yellow";
    return "red";
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'Flying':
        return '✈️';
      case 'Landed':
        return '🛬';
      case 'Taking Off':
        return '🛫';
      case 'Landing':
        return '⬇️';
      case 'Idle':
        return '⏸️';
      case 'Charging':
        return '🔋';
      case 'Disconnected':
        return '❌';
      default:
        return '❓';
    }
  };

  return (
    <div className="container">
      <h1>Multi-Drone Coordination System</h1>
      <div className="tabs">
        {["Drone Feed", "Logs", "Drone Status"].map((tab) => (
          <button
            key={tab}
            className={`tab-button ${activeTab === tab ? "active" : ""}`}
            onClick={() => setActiveTab(tab)}
          >
            {tab}
          </button>
        ))}
      </div>
      <div className="tab-content">
        {activeTab === "Drone Feed" && (
          <div className="drone-feed-container">
            {connectionError ? (
              <div className="connection-error">
                <p>{connectionError}</p>
                <button onClick={() => window.location.reload()}>Retry Connection</button>
              </div>
            ) : (
              <>
                <div className="drone-selector">
                  <label>Select Drone: </label>
                  <select
                    value={selectedDrone}
                    onChange={handleDroneChange}
                  >
                    {drones.map(drone => (
                      <option key={drone.id} value={drone.id}>
                        {drone.name} ({drone.status})
                      </option>
                    ))}
                  </select>
                </div>

                <div className="video-feed">
                  {videoFeed ? (
                    <img
                      src={videoFeed}
                      alt="Drone Camera Feed"
                      style={{ maxWidth: '100%', height: 'auto', borderRadius: '10px' }}
                    />
                  ) : (
                    <div className="loading-feed">Loading drone feed...</div>
                  )}
                </div>

                {selectedDrone && drones.length > 0 && (
                  <div className="drone-info">
                    <h3>Drone Information</h3>
                    {drones.find(d => d.id === selectedDrone) && (
                      <div className="info-grid">
                        <div className="info-item">
                          <strong>Status:</strong> {getStatusIcon(drones.find(d => d.id === selectedDrone).status)} {drones.find(d => d.id === selectedDrone).status}
                        </div>
                        <div className="info-item">
                          <strong>Battery:</strong>
                          <span style={{ color: getBatteryColor(drones.find(d => d.id === selectedDrone).battery) }}>
                            {drones.find(d => d.id === selectedDrone).battery.toFixed(1)}%
                          </span>
                        </div>
                        <div className="info-item">
                          <strong>Altitude:</strong> {drones.find(d => d.id === selectedDrone).altitude.toFixed(2)}m
                        </div>
                        <div className="info-item">
                          <strong>Speed:</strong> {drones.find(d => d.id === selectedDrone).speed ? drones.find(d => d.id === selectedDrone).speed.toFixed(2) : '0.00'} m/s
                        </div>
                        <div className="info-item">
                          <strong>Armed:</strong> {drones.find(d => d.id === selectedDrone).is_armed ? '✅' : '❌'}
                        </div>
                        <div className="info-item">
                          <strong>Collision:</strong> {drones.find(d => d.id === selectedDrone).has_collided ? '⚠️ Yes' : '✅ No'}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </>
            )}
          </div>
        )}
        {activeTab === "Logs" && (
          <div className="logs">
            <h2>Logs</h2>
            <ul>
              <li>Drone 1 activated at 10:00 AM</li>
              <li>Drone 2 is idle since 10:15 AM</li>
              <li>Drone 3 started charging at 10:30 AM</li>
            </ul>
          </div>
        )}
        {activeTab === "Drone Status" && (
          <div className="drone-status">
            <h2>Drone Status</h2>
            <table>
              <thead>
                <tr>
                  <th>Drone</th>
                  <th>Status</th>
                  <th>Battery</th>
                  <th>Altitude</th>
                  <th>Speed</th>
                  <th>Armed</th>
                  <th>Collision</th>
                </tr>
              </thead>
              <tbody>
                {drones.map((drone) => (
                  <tr key={drone.id}>
                    <td>{drone.name}</td>
                    <td>
                      {getStatusIcon(drone.status)} {drone.status}
                    </td>
                    <td>
                      <span
                        className="battery-status"
                        style={{
                          backgroundColor: getBatteryColor(drone.battery),
                        }}
                      ></span>
                      {drone.battery.toFixed(1)}%
                    </td>
                    <td>{drone.altitude.toFixed(2)}m</td>
                    <td>{drone.speed ? drone.speed.toFixed(2) : '0.00'} m/s</td>
                    <td>{drone.is_armed ? '✅' : '❌'}</td>
                    <td>{drone.has_collided ? '⚠️ Yes' : '✅ No'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;