import "./tailwind.css"
import { useEffect } from "react"
import { checkHealth } from "./src/services/api"
import { Dashboard } from "./src/pages/Dashboard"

const appRoot = document.getElementById("root")!

createRoot(appRoot).render(<App />)

// Initialize API on load
useEffect(() => {
  checkHealth().catch(console.error)
}, [])