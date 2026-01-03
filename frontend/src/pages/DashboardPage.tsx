export default function DashboardPage() {
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow p-6 border-l-4 border-blue-500">
          <div className="text-sm text-gray-600 font-medium">Total Candidates</div>
          <div className="text-3xl font-bold text-gray-900 mt-2">1,234</div>
          <div className="text-xs text-green-600 mt-2">+12% from last month</div>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6 border-l-4 border-green-500">
          <div className="text-sm text-gray-600 font-medium">Active Jobs</div>
          <div className="text-3xl font-bold text-gray-900 mt-2">48</div>
          <div className="text-xs text-green-600 mt-2">+5 this week</div>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6 border-l-4 border-purple-500">
          <div className="text-sm text-gray-600 font-medium">Matches</div>
          <div className="text-3xl font-bold text-gray-900 mt-2">892</div>
          <div className="text-xs text-green-600 mt-2">95% accuracy</div>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6 border-l-4 border-orange-500">
          <div className="text-sm text-gray-600 font-medium">Success Rate</div>
          <div className="text-3xl font-bold text-gray-900 mt-2">89%</div>
          <div className="text-xs text-green-600 mt-2">Hiring success</div>
        </div>
      </div>
      
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Activity</h2>
        <div className="text-gray-600">Loading...</div>
      </div>
    </div>
  )
}
