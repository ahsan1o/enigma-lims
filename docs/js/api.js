const API = {
  async request(method, path, body = null) {
    const headers = { 'Content-Type': 'application/json' };
    const token = (typeof Auth !== 'undefined') ? Auth.getToken() : localStorage.getItem('enigma_token');
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const opts = { method, headers };
    if (body) opts.body = JSON.stringify(body);

    try {
      const res = await fetch(`${CONFIG.API_URL}${path}`, opts);
      if (res.status === 401) { localStorage.removeItem('enigma_token'); localStorage.removeItem('enigma_user'); window.location.href='index.html'; return null; }
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: 'Request failed' }));
        throw new Error(err.detail || 'Request failed');
      }
      if (res.status === 204) return null;
      return await res.json();
    } catch(e) {
      console.error('API error:', e);
      throw e;
    }
  },

  get: (path) => API.request('GET', path),
  post: (path, body) => API.request('POST', path, body),
  put: (path, body) => API.request('PUT', path, body),
  delete: (path) => API.request('DELETE', path),

  // Auth
  login: (username, password) => API.post('/api/auth/login', { username, password }),

  // Dashboard
  getStats: () => API.get('/api/dashboard/stats'),
  getRecentSamples: () => API.get('/api/dashboard/recent-samples'),
  getRecentResults: () => API.get('/api/dashboard/recent-results'),

  // Patients
  getPatients: (search = '') => API.get(`/api/patients?limit=200${search ? '&search=' + encodeURIComponent(search) : ''}`),
  createPatient: (data) => API.post('/api/patients', data),
  updatePatient: (id, data) => API.put(`/api/patients/${id}`, data),
  deletePatient: (id) => API.delete(`/api/patients/${id}`),

  // Doctors
  getDoctors: () => API.get('/api/doctors?limit=200'),
  createDoctor: (data) => API.post('/api/doctors', data),

  // Samples
  getSamples: (status = '', search = '') => API.get(`/api/samples?limit=200${status ? '&status=' + status : ''}${search ? '&search=' + encodeURIComponent(search) : ''}`),
  createSample: (data) => API.post('/api/samples', data),
  updateSampleStatus: (id, status) => API.put(`/api/samples/${id}/status`, { status }),

  // Tests
  getTests: (search = '') => API.get(`/api/tests?limit=200${search ? '&search=' + encodeURIComponent(search) : ''}`),
  createTest: (data) => API.post('/api/tests', data),
  updateTest: (id, data) => API.put(`/api/tests/${id}`, data),

  // Orders
  getOrders: (status = '') => API.get(`/api/orders?limit=200${status ? '&status=' + status : ''}`),
  createOrder: (data) => API.post('/api/orders', data),

  // Results
  getResults: (sampleId = '') => API.get(`/api/results?limit=200${sampleId ? '&sample_id=' + sampleId : ''}`),
  createResult: (data) => API.post('/api/results', data),
  approveResult: (id) => API.post(`/api/results/${id}/approve`, {}),

  // Instruments
  getInstruments: () => API.get('/api/instruments'),
  createInstrument: (data) => API.post('/api/instruments', data),
  updateInstrument: (id, data) => API.put(`/api/instruments/${id}`, data),

  // Users
  getUsers: () => API.get('/api/users'),
  createUser: (data) => API.post('/api/users', data),
  updateUser: (id, data) => API.put(`/api/users/${id}`, data),

  // Reports
  getReports: () => API.get('/api/reports'),
  getSampleReport: (id) => API.get(`/api/reports/${id}`),

  // Panels
  getPanels: (activeOnly = false) => API.get(`/api/panels?active_only=${activeOnly}`),
  createPanel: (data) => API.post('/api/panels', data),
  updatePanel: (id, data) => API.put(`/api/panels/${id}`, data),
  deletePanel: (id) => API.delete(`/api/panels/${id}`),

  // Billing
  getInvoices: (status = '') => API.get(`/api/billing?limit=200${status ? '&status=' + status : ''}`),
  createInvoice: (data) => API.post('/api/billing', data),
  payInvoice: (id, data) => API.post(`/api/billing/${id}/pay`, data),
  deleteInvoice: (id) => API.delete(`/api/billing/${id}`),

  // Reagents
  getReagents: (activeOnly = false) => API.get(`/api/reagents?active_only=${activeOnly}`),
  createReagent: (data) => API.post('/api/reagents', data),
  updateReagent: (id, data) => API.put(`/api/reagents/${id}`, data),
  deleteReagent: (id) => API.delete(`/api/reagents/${id}`),

  // Audit
  getAuditLogs: (tableName = '') => API.get(`/api/audit?limit=200${tableName ? '&table_name=' + tableName : ''}`),

  // Patient history
  getPatientHistory: (id) => API.get(`/api/patients/${id}/history`),

  // Sample reject
  rejectSample: (id, reason) => API.put(`/api/samples/${id}/reject`, { rejection_reason: reason }),
};
