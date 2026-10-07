import type {
  Vehicle,
  ProcessingStatus,
  ProcessingResults,
  LineConfig,
  UploadResponse,
  VideoStatus,
  VideoResults,
  VehicleResult,
} from "../types/index"

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api"

export const api = {
  // Upload video
  uploadVideo: async (file: File): Promise<UploadResponse> => {
    const formData = new FormData()
    formData.append("file", file)

    const response = await fetch(`${API_BASE_URL}/videos/upload`, {
      method: "POST",
      body: formData,
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || "Failed to upload video")
    }

    return response.json()
  },

  // Start video processing
  processVideo: async (
    videoId: string,
    config: LineConfig
  ): Promise<string> => {
    const response = await fetch(`${API_BASE_URL}/videos/${videoId}/process`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(config),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || "Failed to start processing")
    }

    const data = await response.json()
    return data.processing_id || videoId
  },

  // Get processing status
  getStatus: async (videoId: string): Promise<VideoStatus> => {
    const response = await fetch(`${API_BASE_URL}/videos/${videoId}/status`)

    if (!response.ok) {
      throw new Error("Failed to get status")
    }

    return response.json()
  },

  // Get processing results
  getResults: async (videoId: string): Promise<VehicleResult[]> => {
    const response = await fetch(`${API_BASE_URL}/videos/${video_id}/results`)

    if (!response.ok) {
      throw new Error("Failed to get results")
    }

    return response.json()
  },

  // Get output video
  getOutputVideo: async (videoId: string): Promise<string> => {
    const response = await fetch(`${API_BASE_URL}/videos/${videoId}/output`)

    if (!response.ok) {
      throw new Error("Failed to get processed video")
    }

    const blob = await response.blob()
    const url = URL.createObjectURL(blob)
    return url
  },

  // Health check
  checkHealth: async (): Promise<{ status: string }> => {
    const response = await fetch(`${API_BASE_URL}/health`)
    return response.json()
  },
}