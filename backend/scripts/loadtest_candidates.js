import http from 'k6/http';
import { check, group, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 10 },   // Ramp up to 10 users
    { duration: '1m', target: 50 },    // Ramp up to 50 users
    { duration: '2m', target: 100 },   // Ramp up to 100 users
    { duration: '1m', target: 50 },    // Ramp down to 50 users
    { duration: '30s', target: 0 },    // Ramp down to 0
  ],
  thresholds: {
    'http_req_duration': ['p(99)<500'],  // 99% of requests under 500ms
    'http_req_failed': ['rate<0.1'],     // 10% error rate
  },
};

export function setup() {
  // Login and get token
  const loginRes = http.post('http://localhost:5000/api/auth/login', {
    email: 'test@example.com',
    password: 'password123',
  });
  const token = loginRes.json('token');
  return { token };
}

export default function (data) {
  const token = data.token;
  const headers = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  };

  group('Candidates API Performance', () => {
    group('GET /api/candidates', () => {
      const res = http.get('http://localhost:5000/api/candidates?page=1&per_page=20', { headers });
      check(res, {
        'status is 200': (r) => r.status === 200,
        'response time < 200ms': (r) => r.timings.duration < 200,
        'has items': (r) => r.json('items') !== null,
      });
    });
    sleep(0.5);

    group('GET /api/candidates/search', () => {
      const res = http.get('http://localhost:5000/api/candidates/search?location=Moscow', { headers });
      check(res, {
        'status is 200': (r) => r.status === 200,
        'response time < 300ms': (r) => r.timings.duration < 300,
      });
    });
    sleep(1);
  });

  group('Matches API Performance', () => {
    const res = http.get('http://localhost:5000/api/matches', { headers });
    check(res, {
      'status is 200': (r) => r.status === 200,
      'response time < 250ms': (r) => r.timings.duration < 250,
    });
    sleep(1);
  });
}
