/**
 * Campaign API calls
 */
import apiClient from './client';

export const campaignAPI = {
  list: async () => {
    const response = await apiClient.get('/api/campaigns');
    return response.data;
  },

  get: async (campaignId) => {
    const response = await apiClient.get(`/api/campaigns/${campaignId}`);
    return response.data;
  },

  create: async (campaignData) => {
    const response = await apiClient.post('/api/campaigns', campaignData);
    return response.data;
  },

  update: async (campaignId, updates) => {
    const response = await apiClient.put(`/api/campaigns/${campaignId}`, updates);
    return response.data;
  },

  delete: async (campaignId) => {
    await apiClient.delete(`/api/campaigns/${campaignId}`);
  },

  scrape: async (campaignId, maxResults = 20) => {
    const response = await apiClient.post(`/api/campaigns/${campaignId}/scrape`, null, {
      params: { max_results: maxResults }
    });
    return response.data;
  },

  generateEmails: async (campaignId) => {
    const response = await apiClient.post(`/api/campaigns/${campaignId}/generate-emails`);
    return response.data;
  },

  sendApproved: async (campaignId) => {
    const response = await apiClient.post(`/api/campaigns/${campaignId}/send-approved`);
    return response.data;
  },

  trackResponses: async (campaignId) => {
    const response = await apiClient.post(`/api/campaigns/${campaignId}/track-responses`);
    return response.data;
  },

  getResponses: async (campaignId) => {
    const response = await apiClient.get(`/api/campaigns/${campaignId}/responses`);
    return response.data;
  },

  getStats: async () => {
    const response = await apiClient.get('/api/campaigns/stats');
    return response.data;
  },
};
