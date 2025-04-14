# Real-Time Monitoring System for Rideau Canal Skateway

## 1.  📘 Scenario Description
Ottawa's Rideau Canal Skateway has become a successful winter tourist spot that needs to be monitored around the clock in order to guarantee skater safety. The purpose of this project is to implement a real-time data flowing system which collects environmental information from simulated IoT sensors placed at three canal locations: NAC, Fifth Avenue, and Dow's Lake. When hazardous weather or ice conditions are detected, this system records the information in Azure Blob Storage for later study.

## 2.  🧩 System Architecture ##
![Image](https://github.com/user-attachments/assets/aee72191-177a-4df8-8536-d7f20d215d4b)
### 🔄 Data Flow Summary:
- **IoT Devices** (Simulated):Every ten seconds, collect data on snow, temperature, and ice thickness.
- **Azure IoT Hub**: receives information from sensors.
- **Azure Stream Analytics**: Real-time processing and gathering of incoming telemetry.
- **Azure Blob Storage**: keeps the information that has been processed for further examination.
---
## 3. ⚙️ Implementation Details ##
### 🛰️ IoT Sensor Simulation
Utilizing the Azure IoT Hub SDK, three Python-simulated devices send sensor data every ten seconds. Every data record contains:
```json
{
  "location": "Dow's Lake",
  "iceThickness": 27,
  "surfaceTemperature": -1,
  "snowAccumulation": 8,
  "externalTemperature": -4,
  "timestamp": "2025-04-23T12:00:00Z"
}
```
### Script File:
sensor-simulation/simulate_sensors.py

The script pushes information to the IoT Hub utilizing device-specific connecting credentials via the Azure IoT Device SDK.

## 🔐 Azure IoT Hub Configuration
This section provides instructions on how to configure the Azure IoT Hub, explaining how to create a device, set up a connection string, and route messages for the Rideau Canal Monitoring System.
---

1. Establish an IoT hub
   Go to [Azure Portal] (https://portal.azure.com) and click on a  **Create a resource**. To proceed, The Internet of Things as a whole IoT Hub
   Please complete the following:
     - **IoT Hub Name:** `skateway-hub` 
     - **area:** Select an area around Ottawa (such as Canada Central) 
     - **Pricing Tier:** F1 (Free Tier) 
     - **Resource Group:** FinalProject
2. **Wait for Deployment**
After deployment is finished, access the resource.


## 🧭 Create Devices (Simulated Sensors)
Navigate to:
- **IoT Hub → Devices (under Device management)**
Select **+ New Device** for every place:
- Device ID: `sensor-dowslak`
- Device ID: `sensor-fifthave`
- Device ID: `sensor-nac`

Following the creation of every device:

To authenticate, click on the device name, copy the **Primary Connection String**, 
and then paste it within the appropriate Python simulation script.

---
## 🔐 Endpoints & Consumer Groups
- Azure IoT Hub dynamically sets up an endpoint with the label **events** for Device-to-Cloud (D2C) connections.
- **Group of consumers used:** `$Default`

💡 For this project, no extra consumer groups or unique endpoints were required.
---
## ✉️ Routing Messages
**Default message routing** was employed for this project:
The **built-in endpoint** represents the destination for all incoming messages.
There were no new routes or unique endpoints made.
📌 With just one analytics pipeline, this streamlines setup and is effective for small to medium-sized enterprises.

---
# 🔄 Azure Stream Analytics Job Configuration
The Azure Stream Analytics task set up to manage the Rideau Canal Skateway Real-Time Monitoring System is detailed in depth in this document.
## 📌 Purpose
Real-time sensor data from Azure IoT Hub is processed by the Stream Analytics job. In order to track snow levels and ice safety conditions, it aggregates the data across a 5-minute tumbling window. The generated output can be saved in Azure Blob Storage for additional analysis.
## 🔌 Input Source Configuration

### Input Alias: `iothubinput`

**Source Type**: Azure IoT Hub  
**Selected Hub**: `skateway-hub`  
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

## 📂 Folder Structure
The output data is automatically separated by time in Azure Stream Analytics. The year, month, day, and hour have been utilized to arrange the data into hierarchical folders. Future integrations as well as effective querying and processing are supported by this structure.
```
skateway/YYYY/MM/DD/HH
```
## 📄 File Format
- **Format**: JSON (the output settings option for Stream Analytics by default)
**Example Record:**
```json
{
  "location": "Dow's Lake",
  "window_end": "2024-11-23T12:10:00Z",
  "avg_iceThickness": 28.1,
  "max_snowAccumulation": 14
}
```
---
## 4 🚀 Usage Instructions 
The IoT simulation may be run, Azure services can be established, stored data may be retrieved, and project obstacles have been addressed in detail in this article.

## ▶️ Running the IoT Sensor Simulation
1. **Clone the repository on GitHub**
 ```bash
   git clone https://github.com/praj0080/Rideau-Canal-Monitoring.git
   cd Rideau-Canal-Monitoring/sensor-simulation
   ```
2. **Install the necessary Python libraries.**
   Run the following command to make sure `pip` is functional: 
   ```bash pip install azure-iot-device ```
3. **Set Up Connection Strings for Devices**
   Launch the `simulate_sensors.py` file.
   Use your real Azure IoT Hub device link strings in place of the placeholders for:
     - sensor-dowslak`
     - `sensor-fifthave`
     - `sensor-nac`
4. **Start the Simulation Script** 
  ```bash python simulate_sensors.py ```
    Every ten seconds, this device will begin transferring Azure IoT Hub simulated telemetry data.

## 🔧 Configuring Azure Services

### 1. **Setup of Azure IoT Hub**
In the Azure Portal, create a fresh IoT hub.
Three devices should be identified in accordance with the three sensor locations.
In the simulation script, copy the connection strings.

### 2. The job of Azure Stream Analytics
Make a new job in Stream Analytics.
Set up the IoT Hub's **input** source (`iothubinput`).
Set Azure Blob Storage (`outputstorage`) as the **output** destination.
Make use of the SQL query that follows:
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


### 3. **Azure Blob Storage Setup** - Rename the blob container `stream-output` and set up a storage account.
- Add it to your Stream Analytics task for an output.

## 📁 Accessing Stored Data in Azure Blob Storage
1. Launch the Azure Portal.
2. Go to **Containers** → **Storage Account** → `stream-output`
3. Examine the folder structure:
```
   year=YYYY/
     └── month=MM/
         └── day=DD/
             └── hour=HH/
                 └── result.json
 ```
4. To see the combined findings, download or look into the output JSON files.

## 5 📊 Results

# key findings:
-The ingestion and real-time processing of sensor data via all three locations (Dow's Lake, Fifth Avenue, and NAC) were carried out with success.
-Using tumbling windows, data was analyzed every five minutes to determine the maximum amount of snow accumulation and average ice thickness for each location.
-The output was arranged as JSON files and kept in ordered folders in Azure Blob Storage.

### 🔍 Sample Output (from Blob Storage)
```json
{
  "location": "Dow's Lake",
  "window_end": "2024-11-23T12:10:00Z",
  "avg_iceThickness": 28.1,
  "max_snowAccumulation": 14
}
```

- This indicates that in Dow's Lake, the **maximum snow accumulation** had been 14 cm and the **average ice thickness** was 28.1 cm for a 5-minute period.
---
## 6 🧠 Reflection
The following were the challenges encountered: 
1. **Python Environment Issues** - On certain systems, the absence of PATH configurations stopped `pip` and `python` from being recognized.
   Solution: During setup, choose "Add to PATH" and install Python from python.org.
2. **Incorrect Stream Analytics Query**
   The output initially went to the input alias (`INTO iothubinput`) rather than Blob storage after an incorrect stream analytics query.
   The query had been modified to `INTO [outputstorage] FROM [iothubinput]` as the solution.
3. **Testing Message Flow**
   The telemetry transfer within the script, IoT Hub, and Blob Storage needed to be observed in Azure. 
   The solution required to verify incoming data using Azure's "Monitor" tab for IoT Hub along with Blob Storage containers.





