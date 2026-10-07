import { useState } from "react"
import { Card, Input, Button, Label } from "./index"

export const VideoUploader = ({
  onFileSelect,
  isProcessing,
}: {
  onFileSelect: (file: File) => void
  isProcessing: boolean
}) => {
  const [file, setFile] = useState<File | null>(null)

  return (
    <Card>
      <h3 className="text-lg font-semibold mb-3">Video Upload</h3>
      <form>
        <div>
          <Input
            type="file"
            accept="video/*"
            onChange={(e) => {
              if (e.target.files?.[0]) {
                setFile(e.target.files[0])
                onFileSelect(e.target.files[0])
              }
            }}
          />
          <Label>Select traffic video file</Label>
        </div>
        <Button type="button" disabled={isProcessing} onClick={() => {
          if (file) onFileSelect(file)
        }}>
          {isProcessing ? "Processing..." : "Upload"}
        </Button>
      </form>
    </Card>
  )
}