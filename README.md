# 🚗 RoadWatch AI

### AI-Powered Vehicle Speed Detection & Traffic Analysis

RoadWatch AI is a full-stack computer vision web application that detects, tracks, counts, and estimates the speed of vehicles from traffic videos using **YOLO, ByteTrack, and OpenCV**.

The application provides an interactive dashboard where users can upload traffic footage, configure detection parameters, analyze vehicle speeds, identify overspeeding vehicles, and download the processed video with real-time annotations.

---

## ✨ Features

### 🎥 Video Processing

* Upload traffic videos in **MP4, AVI, MOV, and WebM**
* Process uploaded videos through a computer vision pipeline
* Download processed videos with detection and speed annotations

### 🚘 Vehicle Detection

* Real-time vehicle detection using **Ultralytics YOLO**
* Supports:

  * 🚗 Cars
  * 🏍️ Motorcycles
  * 🚌 Buses
  * 🚛 Trucks

### 🎯 Vehicle Tracking

* Uses **ByteTrack** for multi-object tracking
* Assigns a unique ID to each detected vehicle
* Maintains vehicle identities across video frames

### ⚡ Speed Estimation

* Uses two configurable virtual lines
* Measures the time taken by vehicles to travel between the lines
* Converts travel time and real-world distance into estimated speed

### 🚨 Overspeed Detection

* Configurable speed limit
* Automatically identifies vehicles exceeding the configured limit
* Displays normal and overspeed vehicles separately

### 📊 Analytics Dashboard

* Total vehicles detected
* Average vehicle speed
* Maximum recorded speed
* Number of overspeeding vehicles
* Speed distribution chart
* Per-vehicle results table

### ⚙️ Configurable Settings

Users can configure:

* Detection confidence threshold
* Virtual line positions
* Real-world distance between lines
* Speed limit
* Video processing parameters

---

# 🧠 How It Works

RoadWatch AI processes traffic footage through several computer vision stages:

```text
Traffic Video
     │
     ▼
┌─────────────────┐
│   YOLO Detector │
│ Vehicle Detection│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    ByteTrack    │
│ Vehicle Tracking│
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│ Virtual Line Crossing│
│      Detection       │
└────────┬────────────┘
         │
         ▼
┌─────────────────┐
│ Speed Estimation│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Overspeed Check │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│ Analytics Dashboard │
└─────────────────────┘
```

---

# 🧮 Speed Estimation

The application estimates vehicle speed using two virtual lines placed on the road.

When a tracked vehicle crosses the first line, its timestamp is recorded.

When the same vehicle crosses the second line, the second timestamp is recorded.

The system then calculates:

```text
Elapsed Time = Time at Line 2 - Time at Line 1
```

Speed is calculated using:

```text
Speed (km/h) = Distance (meters) / Time (seconds) × 3.6
```

### Example

If:

```text
Distance = 100 meters
Elapsed time = 5 seconds
```

Then:

```text
Speed = 100 / 5 × 3.6
       = 72 km/h
```

If the configured speed limit is `60 km/h`, the vehicle will be classified as:

```text
🚨 Overspeed
```

---

# 🛠️ Technology Stack

## Backend

* **Python 3.11+**
* **FastAPI**
* **OpenCV**
* **Ultralytics YOLO**
* **Supervision**
* **ByteTrack**
* **NumPy**
* **Pydantic**

## Frontend

* **React 18**
* **TypeScript**
* **Vite**
* **Tailwind CSS**
* **Axios**
* **Recharts**

---

# 📁 Project Structure

```text
RoadWatch-AI/
│
├── README.md
├── docker-compose.yml
├── .env.example
├── .gitignore
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── schemas.py
│   │   │
│   │   ├── api/
│   │   │   └── routes.py
│   │   │
│   │   ├── services/
│   │   │   ├── detector.py
│   │   │   ├── tracker.py
│   │   │   ├── speed_estimator.py
│   │   │   └── video_processor.py
│   │   │
│   │   └── utils/
│   │       ├── geometry.py
│   │       └── file_manager.py
│   │
│   ├── uploads/
│   ├── outputs/
│   └── requirements.txt
│
└── frontend/
    ├── package.json
    ├── vite.config.ts
    ├── tailwind.config.ts
    ├── tsconfig.json
    │
    ├── index.html
    │
    └── src/
        ├── App.tsx
        ├── main.tsx
        │
        ├── pages/
        │   └── Dashboard.tsx
        │
        ├── components/
        │   ├── VideoUploader.tsx
        │   ├── VideoPlayer.tsx
        │   ├── SettingsPanel.tsx
        │   ├── StatsCards.tsx
        │   ├── VehicleTable.tsx
        │   └── SpeedChart.tsx
        │
        ├── services/
        │   └── api.ts
        │
        └── types/
            └── index.ts
```

---

# 🚀 Installation

## Prerequisites

Make sure you have installed:

* Python 3.11+
* Node.js 18+
* Git
* npm

---

## 1. Clone the Repository

```bash
git clone https://github.com/raaynbengorchi/vehicle-speed-detection.git

cd vehicle-speed-detection
```

---

## 2. Backend Setup

```bash
cd backend
```

Create a virtual environment:

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create your environment file:

```bash
copy .env.example .env
```

Run the FastAPI server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend:

```text
http://localhost:8000
```

---

# 💻 Frontend Setup

Open a new terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will be available at:

```text
http://localhost:3000
```

---

# 🐳 Docker

The project also supports Docker:

```bash
docker-compose up --build
```

---

# 🔌 API Endpoints

## Health Check

```http
GET /api/health
```

## Upload Video

```http
POST /api/videos/upload
```

Upload a traffic video using multipart form data.

## Start Processing

```http
POST /api/videos/{video_id}/process
```

Example:

```json
{
  "line_1_y": 200,
  "line_2_y": 400,
  "distance_meters": 100,
  "speed_limit": 60,
  "confidence_threshold": 0.5
}
```

## Processing Status

```http
GET /api/videos/{video_id}/status
```

## Get Results

```http
GET /api/videos/{video_id}/results
```

## Download Processed Video

```http
GET /api/videos/{video_id}/output
```

---

# ⚙️ Calibration Guide

Accurate configuration is important for meaningful speed estimates.

### 1. Position the Virtual Lines

Place the first line before the measurement area and the second line after it.

```text
Road Direction →

────────────── Line 1
       ↓
       ↓
       ↓
────────────── Line 2
```

### 2. Set the Real-World Distance

Measure the actual distance between both lines.

For example:

```text
Line 1 → Line 2 = 100 meters
```

Set:

```text
distance_meters = 100
```

### 3. Configure the Speed Limit

Example:

```text
speed_limit = 60
```

Vehicles above 60 km/h will be classified as overspeeding.

### 4. Configure Detection Confidence

Example:

```text
confidence_threshold = 0.5
```

Higher values reduce false detections but may miss some vehicles.

---

# 📊 Example Processing Configuration

```json
{
  "line_1_y": 200,
  "line_2_y": 400,
  "distance_meters": 100,
  "speed_limit": 60,
  "confidence_threshold": 0.5
}
```

---

# 📸 Demo

> Add screenshots or a short demo video here.

Example:

```text
Frontend Dashboard
├── Video Upload
├── Detection Preview
├── Speed Statistics
├── Vehicle Table
└── Speed Distribution Chart
```

---

# ⚠️ Limitations

RoadWatch AI provides **estimated vehicle speeds** and should not be considered a legally certified speed measurement system.

Current limitations include:

* Requires a relatively stable camera
* Perspective distortion can affect speed estimation
* Camera angle significantly affects accuracy
* Single-camera measurements are estimates
* Accurate calibration is required
* Video FPS can affect timing calculations
* Very short videos may produce insufficient measurements
* Occluded vehicles may affect tracking accuracy
* Detection accuracy depends on video quality and lighting

---

# 🔮 Future Improvements

Potential improvements include:

* [ ] Improved camera calibration
* [ ] Perspective transformation / homography
* [ ] Automatic lane detection
* [ ] Multi-camera support
* [ ] Real-time CCTV camera input
* [ ] License plate recognition
* [ ] Vehicle classification
* [ ] Historical traffic analytics
* [ ] Export reports as CSV/PDF
* [ ] Cloud deployment
* [ ] Improved tracking in crowded traffic
* [ ] Real-time alerts for overspeeding vehicles

---

# 🎯 Use Cases

RoadWatch AI can be adapted for:

* Traffic monitoring
* Road safety analysis
* Vehicle speed analysis
* Smart city applications
* Intelligent transportation systems
* Traffic research
* Computer vision experimentation

---

# 🔐 Privacy

This project processes uploaded traffic videos locally through the application pipeline.

Users should ensure that any video processed complies with applicable privacy and data protection requirements.

---

# 👨‍💻 Author

**Rayan Bengourchi**

Full-Stack & AI Developer

* GitHub: [@raaynbengorchi](https://github.com/raaynbengorchi)
* LinkedIn: [Rayan Bengourchi](https://www.linkedin.com/in/rayan-bengourchi-207456440/)

---

## ⭐ If you find this project useful

Consider giving the repository a ⭐ on GitHub.

Built with Python, React, YOLO, ByteTrack, and OpenCV.
