import { useState } from "react"
import { Card, Input, Label, Button } from "./index"

export const SettingsPanel = ({
  config,
  onConfigChange,
  isProcessing,
}: {
  config: {
    line1Y: number
    line2Y: number
    distanceMeters: number
    speedLimit: number
    confidenceThreshold: number
  }
  onConfigChange: (e: React.ChangeEvent) => void
  isProcessing: boolean
}) => {
  return (
    <Card>
      <h3 className="text-lg font-semibold mb-3">Configuration</h3>
      <form>
        <div className="mb-3">
          <Label>Distance between lines (meters)</Label>
          <Input
            type="number"
            name="distanceMeters"
            value={config.distanceMeters}
            onChange={onConfigChange}
            min="0.1"
            step="0.1"
            disabled={isProcessing}
          />
        </div>
        <div className="mb-3">
          <Label>Speed limit (km/h)</Label>
          <Input
            type="number"
            name="speedLimit"
            value={config.speedLimit}
            onChange={onConfigChange}
            min="0"
            step="1"
            disabled={isProcessing}
          />
        </div>
        <div className="mb-3">
          <Label>Confidence threshold</Label>
          <Input
            type="number"
            name="confidenceThreshold"
            value={config.confidenceThreshold}
            onChange={onConfigChange}
            min="0"
            max="1"
            step="0.1"
            disabled={isProcessing}
          />
          <small className="text-xs text-gray-400">0.0 - 1.0</small>
        </div>
        <div className="mb-3">
          <Label>Line 1 position (Y pixels)</Label>
          <Input
            type="number"
            name="line1Y"
            value={config.line1Y}
            onChange={onConfigChange}
            min="0"
            disabled={isProcessing}
          />
          <small className="text-xs text-gray-400">Top virtual line</small>
        </div>
        <div className="mb-3">
          <Label>Line 2 position (Y pixels)</Label>
          <Input
            type="number"
            name="line2Y"
            value={config.line2Y}
            onChange={onConfigChange}
            min="1"
            disabled={isProcessing}
          />
          <small className="text-xs text-gray-400">Bottom virtual line (must be > line 1)</small>
        </div>
        <Button type="button" disabled={isProcessing} className="mt-3 w-full">
          {isProcessing ? "Saving..." : "Apply Settings"}
        </Button>
      </form>
    </Card>
  )
}