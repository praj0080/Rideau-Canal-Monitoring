# Real-Time Monitoring System for Rideau Canal Skateway# Rideau-Canal-Monitoring
## 📘 Scenario Description
The Rideau Canal Skateway in Ottawa serves as a well-known winter destination that needs constant supervision to guarantee skater safety. Implementing a real-time data streaming system which gathers environmental data from simulated IoT sensors installed at three key canal locations—Dow's Lake, Fifth Avenue, and NAC—is the aim of this project. When hazardous weather or ice conditions are detected, this system records the information in Azure Blob Storage for later study.

## 🧩 System Architecture

### Components:
- **IoT Devices** (Simulated):Every ten seconds, collect data on snow, temperature, and ice thickness.
- **Azure IoT Hub**: receives information from sensors.
- **Azure Stream Analytics**: Real-time processing and gathering of incoming telemetry.
- **Azure Blob Storage**: keeps the information that has been processed for further examination.
---
## ⚙️ Implementation Details
### 🛰️ IoT Sensor Simulation
Utilizing the Azure IoT Hub SDK, three Python-simulated devices send sensor data every ten seconds. Every data record contains:
```json
{
  "location": "Dow's Lake",
  "iceThickness": 27,
  "surfaceTemperature": -1,
  "snowAccumulation": 8,
  "externalTemperature": -4,
  "timestamp": "2024-11-23T12:00:00Z"
}
**### Script File:**
sensor-simulation/simulate_sensors.py
The script pushes information to the IoT Hub utilizing device-specific connecting credentials via the Azure IoT Device SDK.

## 🔐 Azure IoT Hub Configuration

