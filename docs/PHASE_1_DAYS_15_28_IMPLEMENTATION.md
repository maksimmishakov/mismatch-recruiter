# PHASE 1: DAYS 15-28 COMPREHENSIVE IMPLEMENTATION

## Overview
Days 15-28 focus on backend API infrastructure and frontend dashboard development.

## DAY 15-16: CORS Configuration & API Routes

### Backend Setup (Flask)

**Install dependencies:**
```bash
pip install flask-cors python-dotenv
```

**Update app/api.py:**
```python
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

## DAY 17-18: React Frontend Setup

**Install frontend dependencies:**
```bash
cd mismatch-recruiter
npx create-react-app frontend
cd frontend
npm install axios typescript
```

**Create tsconfig.json in frontend:**
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "jsx": "react-jsx",
    "module": "ESNext",
    "moduleResolution": "node",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

## DAY 19-21: API Integration Hooks

**Create frontend/src/hooks/useApi.ts:**
```typescript
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

export const useApi = () => {
  const fetchCandidates = async () => {
    const response = await axios.get(`${API_BASE_URL}/candidates`);
    return response.data.candidates;
  };

  const fetchMatches = async (userId: string) => {
    const response = await axios.get(`${API_BASE_URL}/matches`, {
      params: { user_id: userId }
    });
    return response.data.matches;
  };

  return { fetchCandidates, fetchMatches };
};
```

## DAY 22-24: Dashboard Component

**Create frontend/src/components/Dashboard.tsx:**
```typescript
import React, { useState, useEffect } from 'react';
import { useApi } from '../hooks/useApi';

interface Match {
  id: string;
  name: string;
  score: number;
  position: string;
}

export const Dashboard: React.FC = () => {
  const { fetchMatches } = useApi();
  const [matches, setMatches] = useState<Match[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadMatches = async () => {
      try {
        const data = await fetchMatches('user123');
        setMatches(data);
      } catch (error) {
        console.error('Error loading matches:', error);
      } finally {
        setLoading(false);
      }
    };
    loadMatches();
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="dashboard">
      <h1>Matches</h1>
      <div className="matches-grid">
        {matches.map(match => (
          <div key={match.id} className="match-card">
            <h3>{match.name}</h3>
            <p>Position: {match.position}</p>
            <p>Match Score: {match.score}%</p>
          </div>
        ))}
      </div>
    </div>
  );
};
```

## DAY 25-26: Filtering & Matching Logic

**Create frontend/src/services/matchingService.ts:**
```typescript
export interface Candidate {
  id: string;
  skills: string[];
  experience: number;
  location: string;
}

export class MatchingService {
  calculateMatchScore(candidate: Candidate, requirements: string[]): number {
    const matchedSkills = candidate.skills.filter(s => 
      requirements.includes(s)
    ).length;
    return Math.round((matchedSkills / requirements.length) * 100);
  }

  filterCandidates(
    candidates: Candidate[],
    filters: { minScore?: number; location?: string }
  ): Candidate[] {
    return candidates.filter(c => {
      if (filters.location && c.location !== filters.location) return false;
      return true;
    });
  }
}
```

## DAY 27-28: Deployment & Testing

**Create deployment configuration (.env):**
```
FLASK_ENV=production
REACT_APP_API_URL=https://your-domain.com/api
DATABASE_URL=your_db_connection_string
```

**Testing checklist:**
- [ ] CORS headers working correctly
- [ ] API endpoints responding
- [ ] React components rendering
- [ ] Data flow from backend to frontend
- [ ] Error handling implemented
- [ ] Performance acceptable

## Next Steps
- Deploy to production servers
- Set up monitoring and logging
- Configure database backups
- Implement authentication
- Add advanced filtering features
