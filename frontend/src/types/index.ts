export interface Vehicle {
  id: number
  class: string
  speed: number | null
  status: "Normal" | "Overspeed" | "Unknown"
  detectedAt: number
}

export interface ProcessingStatus {
  status: "idle" | "processing" | "completed" | "error"
  progress: number
  message: string
}

export interface ProcessingResults {
  totalVehicles: number
  averageSpeed: number
  maxSpeed: number
  overspeedCount: number
  vehicles: Vehicle[]
}

export interface LineConfig {
  line1Y: number
  line2Y: number
  distanceMeters: number
  speedLimit: number
  confidenceThreshold: number
}

export interface UploadResponse {
  videoId: string
  filename: string
}

export interface VideoStatus {
  status: string
  progress: number
  message: string
}

export interface VideoResults {
  totalVehicles: number
  averageSpeed: number
  maxSpeed: number
  overspeedCount: number
  vehicleResults: VehicleResult[]
}

export interface VehicleResult {
  vehicleId: number
  vehicleClass: string
  speedKmh: number
  status: string
  detectedAt: number
}