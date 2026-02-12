/**
 * Campaign detail page with workflow actions
 */
import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { campaignAPI } from '../../api/campaigns';
import { businessAPI } from '../../api/businesses';
import toast from 'react-hot-toast';

export default function CampaignDetail() {
  const { id } = useParams();
  const [campaign, setCampaign] = useState(null);
  const [businesses, setBusinesses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(null);

  useEffect(() => {
    fetchCampaignData();
  }, [id]);

  const fetchCampaignData = async () => {
    try {
      const [campaignData, businessesData] = await Promise.all([
        campaignAPI.get(id),
        businessAPI.list(id),
      ]);
      setCampaign(campaignData);
      setBusinesses(businessesData);
    } catch (error) {
      toast.error('Failed to load campaign');
    } finally {
      setLoading(false);
    }
  };

  const handleScrapeBusinesses = async () => {
    setActionLoading('scrape');
    try {
      await businessAPI.scrapeBusinesses(id, {
        search_query: `${campaign.business_type} near me`,
        max_results: 20,
      });
      toast.success('Businesses scraped successfully!');
      await fetchCampaignData();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to scrape businesses');
    } finally {
      setActionLoading(null);
    }
  };

  const handleGenerateEmails = async () => {
    setActionLoading('generate');
    try {
      await businessAPI.generateEmails(id);
      toast.success('Emails generated successfully!');
      await fetchCampaignData();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to generate emails');
    } finally {
      setActionLoading(null);
    }
  };

  const handleSendEmails = async () => {
    if (!window.confirm('Are you sure you want to send approved emails?')) {
      return;
    }

    setActionLoading('send');
    try {
      await businessAPI.sendApprovedEmails(id);
      toast.success('Emails sent successfully!');
      await fetchCampaignData();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to send emails');
    } finally {
      setActionLoading(null);
    }
  };

  const handleTrackResponses = async () => {
    setActionLoading('track');
    try {
      await businessAPI.trackResponses(id);
      toast.success('Responses tracked successfully!');
      await fetchCampaignData();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to track responses');
    } finally {
      setActionLoading(null);
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      draft: 'bg-gray-100 text-gray-800',
      approved: 'bg-blue-100 text-blue-800',
      sent: 'bg-green-100 text-green-800',
      replied: 'bg-purple-100 text-purple-800',
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="text-gray-500">Loading campaign...</div>
      </div>
    );
  }

  if (!campaign) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900">Campaign not found</h2>
          <Link to="/campaigns" className="mt-4 text-indigo-600 hover:text-indigo-500">
            Back to campaigns
          </Link>
        </div>
      </div>
    );
  }

  const draftCount = businesses.filter((b) => b.status === 'draft').length;
  const approvedCount = businesses.filter((b) => b.status === 'approved').length;
  const sentCount = businesses.filter((b) => b.status === 'sent').length;
  const repliedCount = businesses.filter((b) => b.status === 'replied').length;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <Link to="/campaigns" className="text-indigo-600 hover:text-indigo-500 mb-4 inline-block">
          ← Back to campaigns
        </Link>
        <h1 className="text-3xl font-bold text-gray-900">{campaign.name}</h1>
        <p className="mt-2 text-gray-600">
          {campaign.business_type} • {campaign.outreach_type.replace('_', ' ')}
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-white shadow rounded-lg p-6">
          <div className="text-sm font-medium text-gray-500">Total Businesses</div>
          <div className="mt-2 text-3xl font-bold text-gray-900">{businesses.length}</div>
        </div>
        <div className="bg-white shadow rounded-lg p-6">
          <div className="text-sm font-medium text-gray-500">Draft</div>
          <div className="mt-2 text-3xl font-bold text-gray-600">{draftCount}</div>
        </div>
        <div className="bg-white shadow rounded-lg p-6">
          <div className="text-sm font-medium text-gray-500">Approved</div>
          <div className="mt-2 text-3xl font-bold text-blue-600">{approvedCount}</div>
        </div>
        <div className="bg-white shadow rounded-lg p-6">
          <div className="text-sm font-medium text-gray-500">Sent</div>
          <div className="mt-2 text-3xl font-bold text-green-600">{sentCount}</div>
        </div>
      </div>

      {/* Workflow Actions */}
      <div className="bg-white shadow rounded-lg p-6 mb-8">
        <h2 className="text-lg font-medium text-gray-900 mb-4">Campaign Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <button
            onClick={handleScrapeBusinesses}
            disabled={actionLoading !== null}
            className="px-4 py-3 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium"
          >
            {actionLoading === 'scrape' ? 'Scraping...' : '1. Scrape Businesses'}
          </button>

          <button
            onClick={handleGenerateEmails}
            disabled={actionLoading !== null || draftCount === 0}
            className="px-4 py-3 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium"
          >
            {actionLoading === 'generate' ? 'Generating...' : '2. Generate Emails'}
          </button>

          <button
            onClick={handleSendEmails}
            disabled={actionLoading !== null || approvedCount === 0}
            className="px-4 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium"
          >
            {actionLoading === 'send' ? 'Sending...' : '3. Send Approved'}
          </button>

          <button
            onClick={handleTrackResponses}
            disabled={actionLoading !== null || sentCount === 0}
            className="px-4 py-3 bg-purple-600 text-white rounded-md hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium"
          >
            {actionLoading === 'track' ? 'Tracking...' : '4. Track Responses'}
          </button>
        </div>

        <div className="mt-4 text-sm text-gray-500">
          <p>Follow the workflow in order: Scrape → Generate → Send → Track</p>
        </div>
      </div>

      {/* Businesses Table */}
      <div className="bg-white shadow rounded-lg overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-medium text-gray-900">Businesses</h2>
        </div>

        {businesses.length === 0 ? (
          <div className="p-12 text-center">
            <p className="text-gray-500">No businesses yet. Start by scraping businesses from Google Maps.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Location
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Email
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Phone
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Subject
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {businesses.map((business) => (
                  <tr key={business.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">{business.name}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-500">{business.location}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-500">{business.email || '-'}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-500">{business.phone || '-'}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusColor(
                          business.status
                        )}`}
                      >
                        {business.status}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-sm text-gray-500 truncate max-w-xs">
                        {business.generated_subject || '-'}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Response Stats */}
      {repliedCount > 0 && (
        <div className="mt-8 bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Response Statistics</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <div className="text-sm font-medium text-gray-500">Response Rate</div>
              <div className="mt-2 text-2xl font-bold text-gray-900">
                {sentCount > 0 ? ((repliedCount / sentCount) * 100).toFixed(1) : 0}%
              </div>
            </div>
            <div>
              <div className="text-sm font-medium text-gray-500">Total Sent</div>
              <div className="mt-2 text-2xl font-bold text-gray-900">{sentCount}</div>
            </div>
            <div>
              <div className="text-sm font-medium text-gray-500">Total Replies</div>
              <div className="mt-2 text-2xl font-bold text-purple-600">{repliedCount}</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
