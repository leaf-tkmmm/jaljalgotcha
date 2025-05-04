import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { defineConfig as defineVitestConfig } from "vitest/config";

// https://vitejs.dev/config/
export default defineConfig(
  defineVitestConfig({
    plugins: [react()],
    server: {
      proxy: {
        "/api": {
          target: "https://jaljalgotcha.onrender.com",
          changeOrigin: true,
        },
      },
      host: true,
    },
    test: {
      globals: true,
      environment: "jsdom",
      setupFiles: ["./src/test/setup.ts"],
    },
  })
);
