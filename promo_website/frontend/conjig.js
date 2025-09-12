// This script automatically detects if the website is running locally or on a live server
// and sets the correct backend API URL.

let API_BASE_URL;

// Check the hostname (the website's address)
if (
  window.location.hostname === "127.0.0.1" ||
  window.location.hostname === "localhost"
) {
  // We are on a local machine. Use the local backend URL.
  API_BASE_URL = "http://127.0.0.1:5000";
  console.log("Running in LOCAL environment");
} else {
  // We are on a live server (like Vercel). Use the production backend URL.
  // ** IMPORTANT: Replace this with your actual Railway backend URL! **
  API_BASE_URL = "jarvis-production-b333.up.railway.app";
  console.log("Running in PRODUCTION environment");
}
