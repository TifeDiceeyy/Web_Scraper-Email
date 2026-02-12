/**
 * Campaign creation wizard - multi-step form
 */
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { campaignAPI } from '../../api/campaigns';
import toast from 'react-hot-toast';

const STEPS = {
  BASIC: 1,
  STRATEGY: 2,
  DATA_SOURCE: 3,
  SHEET: 4,
};

export default function CreateCampaign() {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(STEPS.BASIC);
  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState({
    name: '',
    business_type: '',
    outreach_type: 'general_help',
    automation_focus: '',
    data_source: 'google_maps',
    google_sheet_id: '',
  });

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleNext = () => {
    // Validation for each step
    if (currentStep === STEPS.BASIC) {
      if (!formData.name || !formData.business_type) {
        toast.error('Please fill in all fields');
        return;
      }
    }

    if (currentStep === STEPS.STRATEGY) {
      if (formData.outreach_type === 'specific_automation' && !formData.automation_focus) {
        toast.error('Please select an automation focus');
        return;
      }
    }

    if (currentStep < STEPS.SHEET) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handleBack = () => {
    if (currentStep > STEPS.BASIC) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.google_sheet_id) {
      toast.error('Please enter a Google Sheet ID');
      return;
    }

    setLoading(true);

    try {
      const campaign = await campaignAPI.create({
        name: formData.name,
        business_type: formData.business_type,
        outreach_type: formData.outreach_type,
        automation_focus: formData.outreach_type === 'specific_automation' ? formData.automation_focus : null,
        data_source: formData.data_source,
        google_sheet_id: formData.google_sheet_id,
      });

      toast.success('Campaign created successfully!');
      navigate(`/campaigns/${campaign.id}`);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to create campaign');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Create New Campaign</h1>
        <p className="mt-2 text-gray-600">Set up your outreach campaign in 4 easy steps</p>
      </div>

      {/* Progress Steps */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          {[
            { num: 1, label: 'Basic Info' },
            { num: 2, label: 'Strategy' },
            { num: 3, label: 'Data Source' },
            { num: 4, label: 'Google Sheet' },
          ].map((step, idx) => (
            <div key={step.num} className="flex items-center flex-1">
              <div className="flex flex-col items-center flex-1">
                <div
                  className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold ${
                    currentStep >= step.num
                      ? 'bg-indigo-600 text-white'
                      : 'bg-gray-200 text-gray-600'
                  }`}
                >
                  {step.num}
                </div>
                <span className="mt-2 text-xs text-gray-600">{step.label}</span>
              </div>
              {idx < 3 && (
                <div
                  className={`h-1 flex-1 mx-2 ${
                    currentStep > step.num ? 'bg-indigo-600' : 'bg-gray-200'
                  }`}
                />
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Form */}
      <form onSubmit={handleSubmit} className="bg-white shadow rounded-lg p-6">
        {/* Step 1: Basic Info */}
        {currentStep === STEPS.BASIC && (
          <div className="space-y-4">
            <h2 className="text-lg font-medium text-gray-900 mb-4">Campaign Basic Information</h2>

            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
                Campaign Name
              </label>
              <input
                id="name"
                type="text"
                required
                value={formData.name}
                onChange={(e) => handleChange('name', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="e.g., Dentist Outreach Q1 2024"
              />
            </div>

            <div>
              <label htmlFor="business_type" className="block text-sm font-medium text-gray-700 mb-1">
                Business Type
              </label>
              <input
                id="business_type"
                type="text"
                required
                value={formData.business_type}
                onChange={(e) => handleChange('business_type', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="e.g., Dentist, Restaurant, Salon"
              />
              <p className="mt-1 text-sm text-gray-500">
                Type of business you'll be reaching out to
              </p>
            </div>
          </div>
        )}

        {/* Step 2: Outreach Strategy */}
        {currentStep === STEPS.STRATEGY && (
          <div className="space-y-4">
            <h2 className="text-lg font-medium text-gray-900 mb-4">Outreach Strategy</h2>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Choose your approach
              </label>

              <div className="space-y-3">
                <label className="flex items-start p-4 border-2 border-gray-200 rounded-lg cursor-pointer hover:border-indigo-500">
                  <input
                    type="radio"
                    name="outreach_type"
                    value="general_help"
                    checked={formData.outreach_type === 'general_help'}
                    onChange={(e) => handleChange('outreach_type', e.target.value)}
                    className="mt-1 h-4 w-4 text-indigo-600 focus:ring-indigo-500"
                  />
                  <div className="ml-3">
                    <span className="font-medium text-gray-900">General Help</span>
                    <p className="text-sm text-gray-500">
                      Broad outreach offering general business automation services
                    </p>
                  </div>
                </label>

                <label className="flex items-start p-4 border-2 border-gray-200 rounded-lg cursor-pointer hover:border-indigo-500">
                  <input
                    type="radio"
                    name="outreach_type"
                    value="specific_automation"
                    checked={formData.outreach_type === 'specific_automation'}
                    onChange={(e) => handleChange('outreach_type', e.target.value)}
                    className="mt-1 h-4 w-4 text-indigo-600 focus:ring-indigo-500"
                  />
                  <div className="ml-3">
                    <span className="font-medium text-gray-900">Specific Automation</span>
                    <p className="text-sm text-gray-500">
                      Targeted approach focused on one specific automation solution
                    </p>
                  </div>
                </label>
              </div>
            </div>

            {formData.outreach_type === 'specific_automation' && (
              <div>
                <label htmlFor="automation_focus" className="block text-sm font-medium text-gray-700 mb-1">
                  Automation Focus
                </label>
                <select
                  id="automation_focus"
                  value={formData.automation_focus}
                  onChange={(e) => handleChange('automation_focus', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                >
                  <option value="">Select automation type</option>
                  <option value="appointment_reminders">Appointment Reminders</option>
                  <option value="review_requests">Review Requests</option>
                  <option value="lead_followup">Lead Follow-up</option>
                  <option value="feedback_collection">Feedback Collection</option>
                  <option value="inventory_alerts">Inventory Alerts</option>
                </select>
              </div>
            )}
          </div>
        )}

        {/* Step 3: Data Source */}
        {currentStep === STEPS.DATA_SOURCE && (
          <div className="space-y-4">
            <h2 className="text-lg font-medium text-gray-900 mb-4">Data Source</h2>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                How will you add businesses?
              </label>

              <div className="space-y-3">
                <label className="flex items-start p-4 border-2 border-gray-200 rounded-lg cursor-pointer hover:border-indigo-500">
                  <input
                    type="radio"
                    name="data_source"
                    value="google_maps"
                    checked={formData.data_source === 'google_maps'}
                    onChange={(e) => handleChange('data_source', e.target.value)}
                    className="mt-1 h-4 w-4 text-indigo-600 focus:ring-indigo-500"
                  />
                  <div className="ml-3">
                    <span className="font-medium text-gray-900">Google Maps Scraper</span>
                    <p className="text-sm text-gray-500">
                      Automatically scrape business data from Google Maps
                    </p>
                  </div>
                </label>

                <label className="flex items-start p-4 border-2 border-gray-200 rounded-lg cursor-pointer hover:border-indigo-500">
                  <input
                    type="radio"
                    name="data_source"
                    value="json_file"
                    checked={formData.data_source === 'json_file'}
                    onChange={(e) => handleChange('data_source', e.target.value)}
                    className="mt-1 h-4 w-4 text-indigo-600 focus:ring-indigo-500"
                  />
                  <div className="ml-3">
                    <span className="font-medium text-gray-900">Upload JSON File</span>
                    <p className="text-sm text-gray-500">
                      Import businesses from a JSON file
                    </p>
                  </div>
                </label>

                <label className="flex items-start p-4 border-2 border-gray-200 rounded-lg cursor-pointer hover:border-indigo-500">
                  <input
                    type="radio"
                    name="data_source"
                    value="manual"
                    checked={formData.data_source === 'manual'}
                    onChange={(e) => handleChange('data_source', e.target.value)}
                    className="mt-1 h-4 w-4 text-indigo-600 focus:ring-indigo-500"
                  />
                  <div className="ml-3">
                    <span className="font-medium text-gray-900">Manual Entry</span>
                    <p className="text-sm text-gray-500">
                      Add businesses manually one by one
                    </p>
                  </div>
                </label>
              </div>
            </div>
          </div>
        )}

        {/* Step 4: Google Sheet */}
        {currentStep === STEPS.SHEET && (
          <div className="space-y-4">
            <h2 className="text-lg font-medium text-gray-900 mb-4">Google Sheet Configuration</h2>

            <div>
              <label htmlFor="google_sheet_id" className="block text-sm font-medium text-gray-700 mb-1">
                Google Sheet ID
              </label>
              <input
                id="google_sheet_id"
                type="text"
                required
                value={formData.google_sheet_id}
                onChange={(e) => handleChange('google_sheet_id', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="e.g., 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
              />
              <p className="mt-1 text-sm text-gray-500">
                Create a new Google Sheet and paste its ID here. Find the ID in the sheet URL.
              </p>
              <p className="mt-1 text-sm text-gray-500">
                Example: https://docs.google.com/spreadsheets/d/<span className="font-mono text-indigo-600">SHEET_ID</span>/edit
              </p>
            </div>

            <div className="bg-blue-50 border border-blue-200 rounded-md p-4">
              <h3 className="text-sm font-medium text-blue-900 mb-2">Setup Instructions:</h3>
              <ol className="text-sm text-blue-800 space-y-1 list-decimal list-inside">
                <li>Create a new Google Sheet</li>
                <li>Share it with your Google service account email</li>
                <li>Copy the Sheet ID from the URL</li>
                <li>Paste it above</li>
              </ol>
            </div>
          </div>
        )}

        {/* Navigation Buttons */}
        <div className="flex justify-between mt-8 pt-6 border-t border-gray-200">
          <button
            type="button"
            onClick={handleBack}
            disabled={currentStep === STEPS.BASIC}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Back
          </button>

          {currentStep < STEPS.SHEET ? (
            <button
              type="button"
              onClick={handleNext}
              className="px-6 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Next
            </button>
          ) : (
            <button
              type="submit"
              disabled={loading}
              className="px-6 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
            >
              {loading ? 'Creating...' : 'Create Campaign'}
            </button>
          )}
        </div>
      </form>
    </div>
  );
}
