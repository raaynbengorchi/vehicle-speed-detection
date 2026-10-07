import "./tailwind.css"
import { createRoot } from "react-dom/client"
import App from "./App"

const appRoot = document.getElementById("root")!
createRoot(appRoot).render(<App />)