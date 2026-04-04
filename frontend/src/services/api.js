import axios from 'axios';

export const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001/api/v1';
export const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8001';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('admin_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Handle 401 errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('admin_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const adminAPI = {
  login: (username, password) => api.post('/admin/login', new URLSearchParams({ username, password })),
  createAdmin: (data) => api.post('/admin/create', data),
  getCurrentAdmin: () => api.get('/admin/me'),
};

export const contentAPI = {
  // Settings
  getSettings: () => api.get('/content/settings'),
  updateSetting: (key, data) => api.put(`/content/settings/${key}`, data),

  // Sections
  getSections: () => api.get('/content/sections'),
  getSection: (key) => api.get(`/content/sections/${key}`),
  createSection: (data) => api.post('/content/sections', data),
  updateSection: (key, data) => api.put(`/content/sections/${key}`, data),
  deleteSection: (id) => api.delete(`/content/sections/${id}`),

  // Projects
  getProjects: () => api.get('/content/projects'),
  createProject: (data) => api.post('/content/projects', data),
  updateProject: (id, data) => api.put(`/content/projects/${id}`, data),
  deleteProject: (id) => api.delete(`/content/projects/${id}`),

  // Services
  getServices: () => api.get('/content/services'),
  createService: (data) => api.post('/content/services', data),
  updateService: (id, data) => api.put(`/content/services/${id}`, data),
  deleteService: (id) => api.delete(`/content/services/${id}`),

  // Contact Info
  getContactInfo: () => api.get('/content/contact'),
  updateContactInfo: (data) => api.put('/content/contact', data),

  // Image Upload
  uploadImage: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/content/upload-image', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
};

export default api;
