/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'zed-green': '#198A00', // Zambian Flag Green
        'zed-red': '#DE2010',   // Zambian Flag Red
        'zed-black': '#000000', // Zambian Flag Black
        'zed-orange': '#EF7D00', // Zambian Flag Orange
      }
    },
  },
  plugins: [],
}