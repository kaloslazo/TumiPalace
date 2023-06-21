/** @type {import('tailwindcss').Config} */
module.exports = {
  purge: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  content: [],
  theme: {
    colors: {
      "brown": "#795548",
      "brown-50": "#efebe9",
      "brown-100": "#d7ccc8",
      "brown-200": "#bcaaa4",
      "brown-300": "#a1887f",
      "brown-400": "#8d6e63",
      "brown-500": "#795548",
      "brown-600": "#6d4c41",
      "brown-700": "#5d4037",
      "brown-800": "#4e342e",
      "brown-850": "#322823",
      "brown-900": "#28201C",
      "brown-950": "#3E312B",
      "yellow-600": "#fbbf24",
      "yellow-700": "#e4ad0a",
      'white': '#ffffff',
      'gray': '#ccc',
      'red-alert': '#ef4444',
      'red-alert-bg': '#fecaca',
      'red-alert-darker': '#991b1b',
    },
    extend: {
      fontFamily: {
        'sans': [
          'Fira Sans Condensed',
          'ui-sans-serif', 
          'system-ui', 
          '-apple-system', 
          'BlinkMacSystemFont', 
          "Segoe UI", 
          'Roboto', 
          "Helvetica Neue", 
          'Arial', 
          "Noto Sans", 
          'sans-serif', 
          "Apple Color Emoji", 
          "Segoe UI Emoji", 
          "Segoe UI Symbol", 
          "Noto Color Emoji"
        ],
      },
    },
  },
  plugins: [],
}

