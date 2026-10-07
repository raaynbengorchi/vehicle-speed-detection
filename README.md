# RoadWatch AI

Vehicle speed detection web application using YOLO, ByteTrack, and OpenCV.

## Overview

RoadWatch AI is a web application that detects vehicles in traffic videos, tracks them using ByteTrack, and estimates their speed using two virtual lines and a configurable real-world distance.

## Features

1. **Video Upload**: Accepts traffic video files (MP4, AVI, MOV, WebM)
2. **Vehicle Detection**: Uses Ultralytics YOLO to detect cars, motorcycles, buses, and trucks
3. **Vehicle Tracking**: Uses ByteTrack for stable ID assignment across frames
4. **Speed Estimation**: Calculates speed when vehicles cross two configurable virtual lines
5. **Overspeed Detection**: Marks vehicles as "Normal" or "Overspeed" based on configurable speed limit
6. **Summary Dashboard**: Shows total vehicles, average speed, max speed, and overspeed count
7. **Speed Chart**: Visual representation of speed distribution
8. **Processed Video Download**: Download the processed video with annotations
9. **Settings Panel**: Configure line positions, distance, speed limit, and confidence threshold

## Technology Stack

### Backend
- Python 3.11
- FastAPI
- OpenCV
- Ultralytics YOLO
- Supervision (ByteTrack)
- NumPy
- Pydantic

### Frontend
- React 18
- TypeScript
- Vite
- Tailwind CSS
- Axios
- Recharts

## Project Structure

```
.
├── README.md
├── docker-compose.yml
├── .env.example
├── .gitignore
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI application
│   │   ├── config.py        # Application settings
│   │   ├── schemas.py       # Pydantic schemas
│   │   ├── api/           # API routes
│   │   │   └── routes.py  # Endpoint handlers
│   │   ├── services/      # Computer vision services
│   │   │   ├── detector.py    # YOLO vehicle detector
│   │   │   ├── tracker.py     # ByteTrack tracker
│   │   │   ├── speed_estimator.py  # Speed calculation
│   │   │   └── video_processor.py  # Video processing pipeline
│   │   └── utils/         # Utility modules
│   │       ├── geometry.py    # Geometry utilities
│   │       └── file_manager.py  # File management
│   ├── uploads/           # Uploaded video files
│   ├── outputs/           # Processed video files
│   └── requirements.txt   # Python dependencies
└── frontend/
    ├── package.json
    ├── vite.config.ts
    ├── tailwind.config.ts
    ├── tsconfig.json
    ├── index.html
    ├── src/
    │   ├── App.tsx          # Main application component
    │   ├── main.tsx         # Entry point
    │   ├── pages/
    │   │   └── Dashboard.tsx  # Main dashboard page
    │   ├── components/      # UI components
    │   │   ├── VideoUploader.tsx
    │   │   ├── VideoPlayer.tsx
    │   │   ├── SettingsPanel.tsx
    │   │   ├── StatsCards.tsx
    │   │   ├── VehicleTable.tsx
    │   │   └── SpeedChart.tsx
    │   ├── services/
    │   │   └── api.ts       # API service integration
    │   └── types/
    │       └── index.ts     # TypeScript types
```

## Installation

### Prerequisites

- Python 3.11+
- Node.js 18+
- Git

### Backend Setup

1. Create and activate a virtual environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. Run the backend server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. Install Node.js dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Start the frontend development server:
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:3000`

### Docker Setup

```bash
docker-compose up --build
```

## API Endpoints

### Health Check

```bash
GET http://localhost:8000/api/health
```

### Video Upload

```bash
POST http://localhost:8000/api/videos/upload
# Form-data with file field
```

### Start Video Processing

```bash
POST http://localhost:8000/api/videos/{video_id}/process
# Body: { line_1_y, line_2_y, distance_meters, speed_limit, confidence_threshold }
```

### Get Processing Status

```bash
GET http://localhost:8000/api/videos/{video_id}/status
```

### Get Results

```bash
GET http://localhost:8000/api/videos/{video_id}/results
```

### Get Processed Video

```bash
GET http://localhost:8000/api/videos/{video_id}/output
```

## How Speed Estimation Works

1. Two horizontal virtual lines are drawn on the video frame
2. The user configures the real-world distance between the lines in meters
3. When a vehicle's center point crosses line 1, a timestamp is recorded
4. When the same vehicle crosses line 2, another timestamp is recorded
5. Elapsed time = time_crossing_line2 - time_crossing_line1
6. Speed (km/h) = distance_meters / elapsed_time_seconds * 3.6
7. Vehicle is marked as "Overspeed" if speed > configured speed limit

## Limitations

- Speed estimation is an **estimate only**, not legally accurate
- Requires a relatively static camera angle
- Best results with perpendicular camera view to road
- Single-camera setup cannot provide truly accurate speed measurements
- Vehicle speed varies within the frame due to perspective
- Minimum 2-3 seconds of video needed for accurate timing
- FPS assumption may affect timing accuracy

## Calibration Guide

1. **Line Positioning**: Place line 1 before the area of interest and line 2 after
2. **Distance Configuration**: Measure the real-world distance between lines in meters
   - Example: If lines are 100 meters apart on the road, set distance_meters=100
3. **Speed Limit**: Configure the legal speed limit for the road
4. **FPS**: The system uses video FPS or defaults to 30 FPS if unavailable
5. **Testing**: Upload a test video and verify speed calculations

## Example Usage

### Upload a video using curl:

```bash
curl -X POST "http://localhost:8000/api/videos/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@traffic_video.mp4"
```

### Start processing:

```bash
curl -X POST "http://localhost:8000/api/videos/{video_id}/process" \
  -H "Content-Type: application/json" \
  -d '{
    "line_1_y": 200,
    "line_2_y": 400,
    "distance_meters": 100,
    "speed_limit": 60,
    "confidence_threshold": 0.5
  }'
```

### Check status:

```bash
GET http://localhost:8000/api/videos/{video_id}/status
```

### Download processed video:

```bash
GET http://localhost:8000/api/videos/{video_id}/output
```