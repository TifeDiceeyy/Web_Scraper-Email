/**
 * Settings page for API keys and credentials
 */
import { useState, useEffect } from 'react';
import { authAPI } from '../../api/auth';
import toast from 'react-hot-toast';

export default function Settings() {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [settings, setSettings] = useState({
    gemini_api_key: '',
    gmail_address: '',
    gmail_app_password: '',
    telegram_bot_token: '',
    telegram_chat_id: '',
    notification_method: 'email',
  });

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      const data = await authAPI.getSettings();
      setSettings({
        gemini_api_key: '',
        gmail_address: data.gmail_address || '',
        gmail_app_password: '',
        telegram_bot_token: '',
        telegram_chat_id: data.telegram_chat_id || '',
        notification_method: data.notification_method || 'email',
      });
    } catch (error) {
      toast.error('Failed to load settings');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);

    try {
      // Only send non-empty values
      const updates = {};
      if (settings.gemini_api_key) updates.gemini_api_key = settings.gemini_api_key;
      if (settings.gmail_address) updates.gmail_address = settings.gmail_address;
      if (settings.gmail_app_password) updates.gmail_app_password = settings.gmail_app_password;
      if (settings.telegram_bot_token) updates.telegram_bot_token = settings.telegram_bot_token;
      if (settings.telegram_chat_id) updates.telegram_chat_id = settings.telegram_chat_id;
      updates.notification_method = settings.notification_method;

      await authAPI.updateSettings(updates);
      toast.success('Settings saved successfully!');

      // Clear password fields after save
      setSettings(prev => ({
        ...prev,
        gemini_api_key: '',
        gmail_app_password: '',
        telegram_bot_token: '',
      }));
    } catch (error) {
      toast.error('Failed to save settings');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="text-gray-500">Loading settings...</div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
        <p className="mt-2 text-gray-600">Configure your API keys and credentials</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-8">
        {/* Google Gemini AI */}
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Google Gemini AI</h2>
          <div className="space-y-4">
            <div>
              <label htmlFor="gemini_api_key" className="block text-sm font-medium text-gray-700 mb-1">
                Gemini API Key
              </label>
              <input
                id="gemini_api_key"
                type="password"
                value={settings.gemini_api_key}
                onChange={(e) => setSettings({...settings, gemini_api_key: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="Enter new API key to update"
              />
              <p className="mt-1 text-sm text-gray-500">
                Get your API key from{' '}
                <a href="https://makersuite.google.com/app/apikey" target="_blank" rel="noopener noreferrer" className="text-indigo-600 hover:text-indigo-500">
                  Google AI Studio
                </a>
              </p>
            </div>
          </div>
        </div>

        {/* Gmail Configuration */}
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Gmail Configuration</h2>
          <div className="space-y-4">
            <div>
              <label htmlFor="gmail_address" className="block text-sm font-medium text-gray-700 mb-1">
                Gmail Address
              </label>
              <input
                id="gmail_address"
                type="email"
                value={settings.gmail_address}
                onChange={(e) => setSettings({...settings, gmail_address: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="your-email@gmail.com"
              />
            </div>
            <div>
              <label htmlFor="gmail_app_password" className="block text-sm font-medium text-gray-700 mb-1">
                Gmail App Password
              </label>
              <input
                id="gmail_app_password"
                type="password"
                value={settings.gmail_app_password}
                onChange={(e) => setSettings({...settings, gmail_app_password: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="Enter new app password to update"
              />
              <p className="mt-1 text-sm text-gray-500">
                Generate an app password from{' '}
                <a href="https://myaccount.google.com/apppasswords" target="_blank" rel="noopener noreferrer" className="text-indigo-600 hover:text-indigo-500">
                  Google Account Settings
                </a>
              </p>
            </div>
          </div>
        </div>

        {/* Telegram Configuration (Optional) */}
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Telegram Notifications (Optional)</h2>
          <div className="space-y-4">
            <div>
              <label htmlFor="telegram_bot_token" className="block text-sm font-medium text-gray-700 mb-1">
                Bot Token
              </label>
              <input
                id="telegram_bot_token"
                type="password"
                value={settings.telegram_bot_token}
                onChange={(e) => setSettings({...settings, telegram_bot_token: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="Enter new bot token to update"
              />
            </div>
            <div>
              <label htmlFor="telegram_chat_id" className="block text-sm font-medium text-gray-700 mb-1">
                Chat ID
              </label>
              <input
                id="telegram_chat_id"
                type="text"
                value={settings.telegram_chat_id}
                onChange={(e) => setSettings({...settings, telegram_chat_id: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="Your Telegram chat ID"
              />
            </div>
            <div>
              <label htmlFor="notification_method" className="block text-sm font-medium text-gray-700 mb-1">
                Notification Method
              </label>
              <select
                id="notification_method"
                value={settings.notification_method}
                onChange={(e) => setSettings({...settings, notification_method: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              >
                <option value="email">Email</option>
                <option value="telegram">Telegram</option>
              </select>
            </div>
          </div>
        </div>

        {/* Save Button */}
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={saving}
            className="px-6 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
          >
            {saving ? 'Saving...' : 'Save Settings'}
          </button>
        </div>
      </form>
    </div>
  );
}
