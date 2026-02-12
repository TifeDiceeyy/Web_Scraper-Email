/**
 * Authentication API calls
 */
import apiClient from './client';

export const authAPI = {
  register: async (userData) => {
    const response = await apiClient.post('/api/auth/register', userData);
    return response.data;
  },

  login: async (credentials) => {
    const response = await apiClient.post('/api/auth/login', credentials);
    const { access_token, refresh_token } = response.data;

    // Store tokens
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);

    return response.data;
  },

  logout: async () => {
    await apiClient.post('/api/auth/logout');
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },

  getCurrentUser: async () => {
    const response = await apiClient.get('/api/auth/me');
    return response.data;
  },

  getSettings: async () => {
    const response = await apiClient.get('/api/auth/settings');
    return response.data;
  },

  updateSettings: async (settingsData) => {
    const response = await apiClient.put('/api/auth/settings', settingsData);
    return response.data;
  },
};
