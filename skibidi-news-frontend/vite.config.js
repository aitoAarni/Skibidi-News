import { defineConfig } from "vite"
import react from "@vitejs/plugin-react"

// https://vite.dev/config/
export default defineConfig({
    plugins: [react()],
    // added for hot reloads when using docker compose
    server: {
        watch: {
            usePolling: true,
        },
        host: true,
        port: 5173,
    },
})
