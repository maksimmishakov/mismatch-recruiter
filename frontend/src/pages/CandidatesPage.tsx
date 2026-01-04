import Card from '@components/common/Card';
import Button from '@components/common/Button';
export default function CandidatesPage() {
    return (<div className="p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Candidates</h1>
        <Button variant="primary">+ Add Candidate</Button>
      </div>
      
      <Card title="Candidates Database" subtitle="Manage all candidates in your system">
        <div className="space-y-4">
          <div className="bg-gray-50 p-4 rounded border border-gray-200">
            <p className="text-gray-600">Candidate management interface coming soon...</p>
            <p className="text-sm text-gray-500 mt-2">Features: Search, Filter, Bulk actions, Import/Export</p>
          </div>
        </div>
      </Card>
    </div>);
}
