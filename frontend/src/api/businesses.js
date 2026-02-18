/**
 * Business API endpoints
 */
import apiClient from './client';

export const businessAPI = {
  /**
   * List businesses for a campaign
   */
  list: async (campaignId) => {
    const response = await apiClient.get(`/api/campaigns/${campaignId}/businesses`);
    return response.data;
  },

  /**
   * Scrape businesses from Google Maps
   */
  scrapeBusinesses: async (campaignId, params) => {
    const response = await apiClient.post(`/api/campaigns/${campaignId}/scrape`, params);
    return response.data;
  },

  /**
   * Generate emails for all draft businesses
   */
  generateEmails: async (campaignId) => {
    const response = await apiClient.post(`/api/campaigns/${campaignId}/generate-emails`);
    return response.data;
  },

  /**
   * Send all approved emails
   */
  sendApprovedEmails: async (campaignId) => {
    const response = await apiClient.post(`/api/campaigns/${campaignId}/send-approved`);
    return response.data;
  },

  /**
   * Track email responses
   */
  trackResponses: async (campaignId) => {
    const response = await apiClient.post(`/api/campaigns/${campaignId}/track-responses`);
    return response.data;
  },

  /**
   * Add business manually
   */
  create: async (campaignId, business) => {
    const response = await apiClient.post(`/api/campaigns/${campaignId}/businesses`, business);
    return response.data;
  },

  /**
   * Update business
   */
  update: async (businessId, updates) => {
    const response = await apiClient.put(`/api/businesses/${businessId}`, updates);
    return response.data;
  },

  /**
   * Delete business
   */
  delete: async (businessId) => {
    const response = await apiClient.delete(`/api/businesses/${businessId}`);
    return response.data;
  },

  /**
   * Approve email for a business
   */
  approve: async (businessId) => {
    const response = await apiClient.put(`/api/businesses/${businessId}/approve`);
    return response.data;
  },
};
