import React from "react"

export const SpeedChart = ({ stats }: { stats: { totalVehicles: number; averageSpeed: number; maxSpeed: number; overspeedCount: number } }) => {
  const speeds = [0, 20, 40, 60, 80, 100]
  const counts = speeds.map((speed) => {
    if (speed < stats.averageSpeed * 0.8) return 5
    if (speed < stats.averageSpeed) return 8
    if (speed <= stats.maxSpeed) return 3
    return 0
  })

  return (
    <div className="h-64">
      <div className="flex justify-between text-xs text-gray-400 mb-2">
        <span>0 km/h</span>
        <span>{stats.maxSpeed} km/h</span>
      </div>
      <div className="flex-1 bg-gray-700 rounded-h">
        <div
          className="bg-blue-60 h-4 rounded-t shadow"
          style={{ width: `${(stats.averageSpeed / stats.maxSpeed) * 100}%` }}
        />
      </div>
      <div className="flex justify-between text-xs text-gray-400 mt-2">
        <span>Avg: {stats.averageSpeed} km/h</span>
        <span>Max: {stats.maxSpeed} km/h</span>
      </div>
    </div>
  )
}