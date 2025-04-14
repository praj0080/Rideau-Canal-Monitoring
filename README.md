# Real-Time Monitoring System for Rideau Canal Skateway# Rideau-Canal-Monitoring
## 📘 Scenario Description
The Rideau Canal Skateway in Ottawa serves as a well-known winter destination that needs constant supervision to guarantee skater safety. Implementing a real-time data streaming system which gathers environmental data from simulated IoT sensors installed at three key canal locations—Dow's Lake, Fifth Avenue, and NAC—is the aim of this project. When hazardous weather or ice conditions are detected, this system records the information in Azure Blob Storage for later study.

## 🧩 System Architecture

### 🔄 Data Flow Summary:
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
```
### Script File:
sensor-simulation/simulate_sensors.py
The script pushes information to the IoT Hub utilizing device-specific connecting credentials via the Azure IoT Device SDK.

## 🔐 Azure IoT Hub Configuration
This section provides instructions on how to configure the Azure IoT Hub, explaining how to create a device, set up a connection string, and route messages for the Rideau Canal Monitoring System.
---

1. Establish an IoT hub
   Go to [Azure Portal] (https://portal.azure.com) and select **Create a resource**. To proceed, The Internet of Things as a whole IoT Hub
   Please complete the following:
     - **IoT Hub Name:** `rideau-iot-hub` 
     - **area:** Select an area around Ottawa (such as Canada Central) 
     - **Pricing Tier:** F1 (Free Tier) 
     - **Resource Group:** (e.g., RideauProjectGroup)
2. **Wait for Deployment**
After deployment is finished, access the resource.


## 🧭 Create Devices (Simulated Sensors)
Navigate to:
- **IoT Hub → Devices (under Device management)**
Select **+ New Device** for every place:
- Device ID: `sensor-dowslake`
- Device ID: `sensor-fifthave`
- Device ID: `sensor-nac`

Following the creation of every device:

To authenticate, click on the device name, copy the **Primary Connection String**, 
and then paste it within the appropriate Python simulation script.

---
## 🔐 Endpoints & Consumer Groups
- Azure IoT Hub automatically configures an endpoint for Device-to-Cloud (D2C) communications with the name **events**.
- **Group of consumers used:** `$Default`

💡 For this project, no extra consumer groups or unique endpoints were required.
---
## ✉️ Routing Messages
**Default message routing** was employed for this project:
The **built-in endpoint** represents the destination for all incoming messages.
There were no new routes or unique endpoints made.
📌 With just one analytics pipeline, this streamlines setup and is effective for small to medium-sized enterprises.
## 📸 Screenshot Reference
View the screenshots of all three connected devices at `screenshots/iot-hub-devices.png` for visual proof.
A screenshot of the overview and default endpoints can be found at `screenshots/iot-hub-overview.png` *(if available)*.
---
# 🔄 Azure Stream Analytics Job Configuration
The Azure Stream Analytics task set up to manage the Rideau Canal Skateway Real-Time Monitoring System is detailed in depth in this document.
## 📌 Purpose
Real-time sensor data from Azure IoT Hub is processed by the Stream Analytics job. In order to track snow levels and ice safety conditions, it aggregates the data across a 5-minute tumbling window. The generated output can be saved in Azure Blob Storage for additional analysis.
## 🔌 Input Source Configuration

### Input Alias: `iothubinput`

**Source Type**: Azure IoT Hub  
**Selected Hub**: `rideau-iot-hub`  
**Consumer Group**: `$Default`  
**Data Format**: JSON  
**Encoding**: UTF-8  
**Timestamp Usage**: Timestamp from the event (`timestamp` field in the payload)

**Configuration Steps:**
1. In your Stream Analytics task, select the **Inputs** tab.
2. Select **+ Input stream → IoT Hub**
3. Select the `$Default` consumer group and the relevant IoT hub.
4. Configure `iothubinput` as the alias.
5. Save the setup.
---
## 📥 Logic of Queries

Sensor information can be sorted by location and processed by the job every five minutes. The objective is to calculate:
Ice safety conditions can be determined by the average thickness of the ice.
The impact of snow on usefulness is shown by the **maximum snow accumulation**.

### Sample SQL Query:
```sql
SELECT
    location,
    System.Timestamp AS window_end,
    AVG(CAST(iceThickness AS float)) AS avg_iceThickness,
    MAX(CAST(snowAccumulation AS float)) AS max_snowAccumulation
INTO
    [outputstorage]
FROM
    [iothubinput] TIMESTAMP BY timestamp
GROUP BY
    location,
    TumblingWindow(minute, 5)
```
Using a tumbling window, the Stream Analytics inquiry aggregates values every five minutes to process real-time IoT data. To evaluate the safety conditions on the Rideau Canal, it analyzes the maximum amount of snow accumulation and the average thickness of the ice at each location. Even when messages arrive late, the query guarantees correct time-based analysis by utilizing the event's timestamp.

# 💾 Azure Blob Storage Configuration
It defines the folder structure, file format, and naming standards for the processed data from Azure Stream Analytics that are saved in Azure Blob Storage.

