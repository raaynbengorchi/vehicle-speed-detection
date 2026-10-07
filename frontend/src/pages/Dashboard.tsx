import {
  useState,
  useEffect,
  useCallback,
  FormEvent,
} from "react"
import { Card, Button, Input, Label } from "./components"
import { VehicleTable } from "./components/VehicleTable"
import { StatsCards } from "./components/StatsCards"
import { SpeedChart } from "./components/SpeedChart"
import { api, type LineConfig, type VehicleResult } from "@/services/api"
import { useNavigate } from "react-router-dom"

export const Dashboard = () => {
  const navigate = useNavigate()
  const [config, setConfig] = useState<LineConfig>({
    line1Y: 200,
    line2Y: 400,
    distanceMeters: 100,
    speedLimit: 60,
    confidenceThreshold: 0.5,
  })
  const [videoId, setVideoId] = useState<string | null>(null)
  const [status, setStatus] = useState<{
    processing: boolean
    progress: number
    message: string
  }>({ processing: false, progress: 0, message: "" })
  const [results, setResults] = useState<VehicleResult[]>([])
  const [stats, setStats] = useState({
    totalVehicles: 0,
    averageSpeed: 0,
    maxSpeed: 0,
    overspeedCount: 0,
  })
  const [videoUrl, setVideoUrl] = useState<string | null>(null)

  // Load results when videoId changes
  useEffect(() => {
    if (videoId) {
      loadResults(videoId)
    }
  }, [videoId])

  const loadResults = async (id: string) => {
    try {
      const data = await api.getResults(id)
      setResults(data)
      
      const total = data.length
      const speeds = data.map((r) => r.speedKmh).filter((s) => s !== null && !isNaN(s))
      const avgSpeed = speeds.length > 0 ? speeds.reduce((a, b) => a + b, 0) / speeds.length : 0
      const maxSpeed = speeds.length > 0 ? Math.max(...speeds) : 0
      const overspeedCount = data.filter((r) => r.status === "Overspeed").length
      
      setStats({
        totalVehicles: total,
        averageSpeed: Math.round(avgSpeed * 100) / 100,
        maxSpeed: Math.round(maxSpeed * 100) / 100,
        overspeedCount,
      })
    } catch (err) {
      console.error("Error loading results:", err)
    }
  }

  const handleUpload = async (event: FormEvent, file: File) => {
    event.preventDefault()
    setStatus({ processing: true, progress: 0, message: "Uploading..." })

    try {
      const uploadResponse = await api.uploadVideo(file)
      setVideoId(uploadResponse.videoId)
      setStatus({ processing: false, progress: 0, message: "Upload complete" })
    } catch (err) {
      setStatus({ processing: false, progress: 0, message: (err as Error).message })
    }
  }

  const handleProcess = async () => {
    if (!videoId) return

    setStatus({ processing: true, progress: 0, message: "Processing video..." })

    try {
      await api.processVideo(videoId, config)
      setStatus({ processing: false, progress: 100, message: "Processing complete" })
      
      // Load results after processing
      await loadResults(videoId)
      
      // Generate video URL
      const videoUrl = await api.getOutputVideo(videoId)
      setVideoUrl(videoUrl)
    } catch (err) {
      setStatus({ processing: false, progress: 0, message: (err as Error).message })
    }
  }

  const handleConfigChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setConfig(prev => ({ ...prev, [name]: parseFloat(value) }))
  }, [])

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <header className="border-b border-gray-700 bg-gray-800">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <h1 className="text-3xl font-bold">RoadWatch AI</h1>
          <p className="text-gray-400 text-sm">Vehicle speed detection system</p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto p-6">
        {/* Upload Section */}
        <section className="mb-6">
          <Card>
            <h2 className="text-xl font-semibold mb-4">Video Upload</h2>
            <form onSubmit={(e) => handleUpload(e, event.target?.files?.[0] || event.currentTarget?.files?.[0])} className="space-y-4">
              <div>
                <Input
                  type="file"
                  accept="video/*"
                  required
                  onChange={(e) => setConfig(prev => ({ ...prev, file: e.target.files?.[0] }))}
                />
                <Label>Select traffic video</Label>
              </div>
              <Button type="submit" disabled={status.processing}>
                {status.processing ? "Uploading..." : "Upload Video"}
              </Button>
              {!status.processing && videoId && (
                <Button
                  onClick={handleProcess}
                  variant="secondary"
                  className="mt-2"
                >
                  Process Video
                </Button>
              )}
            </form>
          </Card>
        </section>

        {/* Settings Section */}
        {videoId && !status.processing && (
          <section className="mb-6">
            <Card>
              <h2 className="text-xl font-semibold mb-4">Settings</h2>
              <form onSubmit={(e) => e.preventDefault()} className="space-y-4">
                <div>
                  <Label>Distance between lines (meters)</Label>
                  <Input
                    type="number"
                    name="distanceMeters"
                    value={config.distanceMeters}
                    onChange={handleConfigChange}
                    min="0.1"
                    step="0.1"
                  />
                </div>
                <div>
                  <Label>Speed limit (km/h)</Label>
                  <Input
                    type="number"
                    name="speedLimit"
                    value={config.speedLimit}
                    onChange={handleConfigChange}
                    min="0"
                    step="1"
                  />
                </div>
                <div>
                  <Label>Confidence threshold</Label>
                  <Input
                    type="number"
                    name="confidenceThreshold"
                    value={config.confidenceThreshold}
                    onChange={handleConfigChange}
                    min="0"
                    max="1"
                    step="0.1"
                  />
                  <small className="text-gray-400 text-xs">0.0 - 1.0</small>
                </div>
                <div>
                  <Label>Line 1 position (Y pixels)</Label>
                  <Input
                    type="number"
                    name="line1Y"
                    value={config.line1Y}
                    onChange={handleConfigChange}
                    min="0"
                  />
                  <small className="text-gray-400 text-xs">Y position of first virtual line</small>
                </div>
                <div>
                  <Label>Line 2 position (Y pixels)</Label>
                  <Input
                    type="number"
                    name="line2Y"
                    value={config.line2Y}
                    onChange={handleConfigChange}
                    min="1"
                  />
                  <small className="text-gray-400 text-xs">Y position of second virtual line (must be > line 1)</small>
                </div>
              </form>
            </Card>
          </section>
        )}

        {/* Processing Status */}
        {status.processing && (
          <section>
            <Card>
              <div className="progress-bar">
                <div
                  style={{ width: `${status.progress}%` }}
                  className="progress-progress"
                />
              </div>
              <p className="mt-2 text-sm">{status.message}</p>
            </Card>
          </section>
        )}

        {/* Results Section */}
        {videoId && !status.processing && results.length > 0 && (
          <section className="mt-6">
            <Card>
              <h2 className="text-xl font-semibold mb-4">Statistics</h2>
              <StatsCards stats={stats} />
            </Card>
          </section>
        )}

        {/* Video Player */}
        {videoId && !status.processing && videoUrl && (
          <section className="mt-6">
            <Card>
              <h2 className="text-xl font-semibold mb-4">Processed Video</h2>
              <video
                src={videoUrl}
                controls
                className="w-full rounded-md"
              />
              <div className="mt-2 flex justify-end">
                <Button onClick={() => {
                  // Trigger download
                  const a = document.createElement('a')
                  a.href = videoUrl
                  a.download = `processed_${videoId}.mp4`
                  a.click()
                }}>
                  Download Processed Video
                </Button>
              </div>
            </Card>
          </section>
        )}

        {/* Vehicle Table */}
        {videoId && !status.processing && results.length > 0 && (
          <section className="mt-6">
            <Card>
              <h2 className="text-xl font-semibold mb-4">Vehicle Results</h2>
              <VehicleTable vehicles={results} />
            </Card>
          </section>
        )}

        {/* Speed Chart */}
        {videoId && !status.processing && stats.totalVehicles > 0 && (
          <section className="mt-6">
            <Card>
              <h2 className="text-xl font-semibold mb-4">Speed Distribution</h2>
              <SpeedChart stats={stats} />
            </Card>
          </section>
        )}
      </main>
    </div>
  )
}