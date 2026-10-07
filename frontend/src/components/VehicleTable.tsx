import React from "react"

export const VehicleTable = ({ vehicles }: { vehicles: { vehicleId: number; vehicleClass: string; speedKmh: number; status: string; detectedAt: number }[] }) => {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-gray-700">
            <th className="text-left text-gray-400 font-semibold">Vehicle ID</th>
            <th className="text-left text-gray-400 font-semibold">Type</th>
            <th className="text-left text-gray-400 font-semibold">Speed</th>
            <th className="text-left text-gray-400 font-semibold">Status</th>
            <th className="text-left text-gray-400 font-semibold">Time Detected</th>
          </tr>
        </thead>
        <tbody>
          {vehicles.map((vehicle) => (
            <tr key={vehicle.vehicleId} className="border-b border-gray-700 hover:bg-gray-700">
              <td className="text-gray-300">{vehicle.vehicleId}</td>
              <td className="text-gray-300">{vehicle.vehicleClass}</td>
              <td className="text-gray-300">
                {vehicle.speedKmh !== null && !isNaN(vehicle.speedKmh)
                  ? `${vehicle.speedKmh} km/h`
                  : "N/A"}
              </td>
              <td>
                <span
                  className={`px-2 py-1 text-xs rounded ${
                    vehicle.status === "Overspeed"
                      ? "bg-red-100 text-red-800"
                      : "bg-green-100 text-green-800"
                  }`}
                >
                  {vehicle.status}
                </span>
              </td>
              <td className="text-gray-300">
                {new Date(vehicle.detectedAt * 1000).toLocaleTimeString()}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}