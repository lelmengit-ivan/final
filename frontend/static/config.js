// API Configuration
const CONFIG = {
    // Auto-detect: uses local when running locally, Render when deployed
    API_URL: 'https://pharmacy-backened.onrender.com/api'
    
    // To force Render backend even when running locally, use this:
    // API_URL: 'https://pharmacy-system-pgkk.onrender.com/api'
};

// Export for use in other scripts
window.CONFIG = CONFIG;
