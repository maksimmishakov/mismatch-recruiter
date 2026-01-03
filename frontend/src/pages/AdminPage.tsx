import React, { useState, useEffect } from 'react';
import { Settings, Users, Trash2, Key, Database } from 'lucide-react';

const AdminPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'users' | 'config' | 'data'>('users');
  const [users, setUsers] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

  useEffect(() => {
    if (activeTab === 'users') {
      fetchUsers();
    }
  }, [activeTab]);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/api/admin/users`, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` },
      });
      if (res.ok) {
        const data = await res.json();
        setUsers(data.users || []);
      }
    } catch (err) {
      console.error('Failed to fetch users:', err);
    } finally {
      setLoading(false);
    }
  };

  const tabs = [
    { id: 'users', label: 'Users', icon: Users },
    { id: 'config', label: 'Configuration', icon: Settings },
    { id: 'data', label: 'Data Management', icon: Database },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        <div className="bg-white rounded-lg shadow-lg">
          {/* Header */}
          <div className="border-b border-gray-200 p-6">
            <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
              <Settings className="h-8 w-8 text-red-600" />
              Administrator Panel
            </h1>
            <p className="mt-2 text-gray-600">Manage system settings and users</p>
          </div>

          {/* Tabs */}
          <div className="border-b border-gray-200 flex">
            {tabs.map((tab) => {
              const TabIcon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`flex items-center gap-2 px-6 py-4 font-medium transition ${
                    activeTab === tab.id
                      ? 'border-b-2 border-red-600 text-red-600'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  <TabIcon className="h-5 w-5" />
                  {tab.label}
                </button>
              );
            })}
          </div>

          {/* Content */}
          <div className="p-6">
            {activeTab === 'users' && (
              <div>
                <h2 className="text-xl font-bold text-gray-900 mb-4">User Management</h2>
                {loading ? (
                  <div className="text-center py-8">Loading users...</div>
                ) : (
                  <div className="overflow-x-auto">
                    <table className="w-full">
                      <thead>
                        <tr className="border-b border-gray-200">
                          <th className="px-4 py-2 text-left text-sm font-medium text-gray-900">Name</th>
                          <th className="px-4 py-2 text-left text-sm font-medium text-gray-900">Email</th>
                          <th className="px-4 py-2 text-left text-sm font-medium text-gray-900">Role</th>
                          <th className="px-4 py-2 text-left text-sm font-medium text-gray-900">Status</th>
                          <th className="px-4 py-2 text-left text-sm font-medium text-gray-900">Actions</th>
                        </tr>
                      </thead>
                      <tbody>
                        {users.map((user) => (
                          <tr key={user.id} className="border-b border-gray-200 hover:bg-gray-50">
                            <td className="px-4 py-2 text-sm text-gray-900">{user.name}</td>
                            <td className="px-4 py-2 text-sm text-gray-600">{user.email}</td>
                            <td className="px-4 py-2 text-sm">
                              <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs font-medium">
                                {user.role || 'User'}
                              </span>
                            </td>
                            <td className="px-4 py-2 text-sm">
                              <span className={`px-2 py-1 rounded text-xs font-medium ${
                                user.active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                              }`}>
                                {user.active ? 'Active' : 'Inactive'}
                              </span>
                            </td>
                            <td className="px-4 py-2 text-sm flex gap-2">
                              <button className="text-blue-600 hover:text-blue-800">Edit</button>
                              <button className="text-red-600 hover:text-red-800">Delete</button>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                    {users.length === 0 && (
                      <div className="text-center py-8 text-gray-500">No users found</div>
                    )}
                  </div>
                )}
              </div>
            )}

            {activeTab === 'config' && (
              <div>
                <h2 className="text-xl font-bold text-gray-900 mb-4">System Configuration</h2>
                <div className="space-y-4">
                  <div className="p-4 border border-gray-200 rounded-lg">
                    <label className="block text-sm font-medium text-gray-900 mb-2">
                      API Key
                    </label>
                    <input
                      type="password"
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500"
                      placeholder="••••••••••••••••"
                    />
                  </div>
                  <div className="p-4 border border-gray-200 rounded-lg">
                    <label className="block text-sm font-medium text-gray-900 mb-2">
                      Max Upload Size (MB)
                    </label>
                    <input
                      type="number"
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500"
                      defaultValue="5"
                    />
                  </div>
                  <button className="w-full bg-red-600 hover:bg-red-700 text-white font-medium py-2 px-4 rounded-lg transition">
                    Save Configuration
                  </button>
                </div>
              </div>
            )}

            {activeTab === 'data' && (
              <div>
                <h2 className="text-xl font-bold text-gray-900 mb-4">Data Management</h2>
                <div className="space-y-4">
                  <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                    <p className="text-sm text-yellow-800 mb-3">
                      <strong>Warning:</strong> These actions cannot be undone. Proceed with caution.
                    </p>
                    <div className="space-y-2">
                      <button className="w-full bg-yellow-600 hover:bg-yellow-700 text-white font-medium py-2 px-4 rounded-lg transition flex items-center gap-2">
                        <Trash2 className="h-4 w-4" />
                        Clear Cache
                      </button>
                      <button className="w-full bg-red-600 hover:bg-red-700 text-white font-medium py-2 px-4 rounded-lg transition flex items-center gap-2">
                        <Trash2 className="h-4 w-4" />
                        Delete Old Records
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminPage;
