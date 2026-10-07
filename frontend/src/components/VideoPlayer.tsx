import { useState } from "react"
import { Card, Button } from "./index"

export const VideoPlayer = ({
  videoUrl,
  isProcessing,
}: {
  videoUrl: string | null
  isProcessing: boolean
}) => {
  return (
    <Card>
      <h3 className="text-lg font-semibold mb-3">Processed Video</h3>
      {videoUrl ? (
        <>
          <video src={videoUrl} controls className="w-full rounded-md" />
          <Button onClick={() => window.open(videoUrl, "_blank")} className="mt-2">
            Open in new tab
          </Button>
          <Button
            onClick={() => {
              const a = document.createElement("a")
              a.href = videoUrl
              a.download = "processed_video.mp4"
              a.click()
            }}
            className="mt-2 ml-2"
          >
            Download
          </Button>
        </>
      ) : (
        <p className="text-gray-400">No video available</p>
      )}
    </Card>
  )
}