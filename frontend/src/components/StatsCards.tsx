import React from "react"

export const StatsCards = ({ stats }: { stats: { totalVehicles: number; averageSpeed: number; maxSpeed: number; overspeedCount: number } }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <div className="bg-gray-800 p-4 rounded-md">
        <svg viewBox="0 0 24 24" fill="currentColor" className="h-5 w-5 mb-2 text-blue-400" />
        <div>
          <div className="text-gray-400 text-sm">Total Vehicles</div>
          <div className="text-2xl font-bold text-white">{stats.totalVehicles}</div>
        </div>
      </div>
      <div className="bg-gray-800 p-4 rounded-md">
        <svg viewBox="0 0 24 24" fill="currentColor" className="h-5 w-5 mb-2 text-blue-400" />
        <div>
          <div className="text-gray-400 text-sm">Average Speed</div>
          <div className="text-2xl font-bold text-white">{stats.averageSpeed} km/h</div>
        </div>
      </div>
      <div className="bg-gray-800 p-4 rounded-md">
        <svg viewBox="0 0 24 24" fill="currentColor" className="h-5 w-5 mb-2 text-blue-400" />
        <div>
          <div className="text-gray-400 text-sm">Max Speed</div>
          <div className="text-2xl font-bold text-white">{stats.maxSpeed} km/h</div>
        </div>
      </div>
      <div className="bg-gray-800 p-4 rounded-md">
        <svg viewBox="0 0 24 24" fill="currentColor" className="h-5 w-5 mb-2 text-blue-400" />
        <div>
          <div className="text-gray-400 text-sm">Overspeed</div>
          <div className="text-2xl font-bold text-red-500">{stats.overspeedCount}</div>
        </div>
      </div>
    </div>
  )
}