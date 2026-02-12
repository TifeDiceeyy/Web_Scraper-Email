/**
 * Dashboard page - Main overview
 */
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { campaignAPI } from '../../api/campaigns';
import { useAuth } from '../../context/AuthContext';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [statsData, campaignsData] = await Promise.all([
        campaignAPI.getStats(),
        campaignAPI.list(),
      ]);
      setStats(statsData);
      setCampaigns(campaignsData);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="flex justify-center items-center h-screen">Loading...</div>;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">
          Welcome back, {user?.full_name || user?.email}!
        </h1>
        <p className="mt-2 text-gray-600">Here's what's happening with your campaigns</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-1">
                <dt className="text-sm font-medium text-gray-500 truncate">
                  Total Campaigns
                </dt>
                <dd className="mt-1 text-3xl font-semibold text-gray-900">
                  {stats?.total_campaigns || 0}
                </dd>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-1">
                <dt className="text-sm font-medium text-gray-500 truncate">
                  Active Campaigns
                </dt>
                <dd className="mt-1 text-3xl font-semibold text-gray-900">
                  {stats?.active_campaigns || 0}
                </dd>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-1">
                <dt className="text-sm font-medium text-gray-500 truncate">
                  Businesses Scraped
                </dt>
                <dd className="mt-1 text-3xl font-semibold text-gray-900">
                  {stats?.total_businesses || 0}
                </dd>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-1">
                <dt className="text-sm font-medium text-gray-500 truncate">
                  Response Rate
                </dt>
                <dd className="mt-1 text-3xl font-semibold text-gray-900">
                  {stats?.response_rate?.toFixed(1) || 0}%
                </dd>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Campaigns */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 border-b border-gray-200 sm:px-6">
          <div className="flex items-center justify-between">
            <h3 className="text-lg leading-6 font-medium text-gray-900">
              Recent Campaigns
            </h3>
            <Link
              to="/campaigns/create"
              className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700"
            >
              Create Campaign
            </Link>
          </div>
        </div>
        <ul className="divide-y divide-gray-200">
          {campaigns.length === 0 ? (
            <li className="px-4 py-12 text-center text-gray-500">
              No campaigns yet. Create your first campaign to get started!
            </li>
          ) : (
            campaigns.slice(0, 5).map((campaign) => (
              <li key={campaign.id} className="px-4 py-4 hover:bg-gray-50">
                <Link to={`/campaigns/${campaign.id}`}>
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <p className="text-sm font-medium text-indigo-600">{campaign.name}</p>
                      <p className="text-sm text-gray-500">{campaign.business_type}</p>
                    </div>
                    <div className="flex items-center space-x-4">
                      <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                        {campaign.status}
                      </span>
                      <span className="text-sm text-gray-500">
                        {campaign.total_businesses} businesses
                      </span>
                    </div>
                  </div>
                </Link>
              </li>
            ))
          )}
        </ul>
      </div>
    </div>
  );
}
