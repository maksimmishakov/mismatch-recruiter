import Card from '@components/common/Card';
export default function MatchesPage() {
    return (<div className="p-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Matches</h1>
      
      <Card title="Candidate-Job Matches" subtitle="AI-powered matching results">
        <div className="space-y-4">
          <div className="bg-gray-50 p-4 rounded border border-gray-200">
            <p className="text-gray-600">Match visualization interface coming soon...</p>
            <p className="text-sm text-gray-500 mt-2">Features: Scoring, Ranking, Details, Actions, History</p>
          </div>
        </div>
      </Card>
    </div>);
}
