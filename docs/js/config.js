// Auto-detect: use local server when running as desktop EXE, cloud API otherwise
const CONFIG = {
  API_URL: (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
    ? `http://${window.location.host}`
    : 'https://enigma-lims-api.onrender.com',
  APP_NAME: 'Enigma LIMS',
  VERSION: '1.0.0'
};
