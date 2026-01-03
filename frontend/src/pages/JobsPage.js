import Card from '@components/common/Card';
import Button from '@components/common/Button';
export default function JobsPage() {
    return (<div className="p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Jobs</h1>
        <Button variant="primary">+ Create Job</Button>
      </div>
      
      <Card title="Job Listings" subtitle="Manage all open positions">
        <div className="space-y-4">
          <div className="bg-gray-50 p-4 rounded border border-gray-200">
            <p className="text-gray-600">Job management interface coming soon...</p>
            <p className="text-sm text-gray-500 mt-2">Features: Create, Edit, Publish, Analysis, Matching</p>
          </div>
        </div>
      </Card>
    </div>);
}
