#!/bin/bash
echo "=== MisMatch Recruiter Integration Verification ==="
echo ""
echo "1. Checking Backend API Health..."
BACKEND_HEALTH=$(curl -s http://localhost:5000/api/health)
echo "Backend Response: $BACKEND_HEALTH"

echo ""
echo "2. Checking Frontend Dev Server..."
FRONTEND_CHECK=$(curl -s -o /dev/null -w '%{http_code}' http://localhost:3001/)
echo "Frontend Status Code: $FRONTEND_CHECK"

echo ""
echo "3. Checking Backend Services..."
echo "  - PostgreSQL: "
ps aux | grep -E 'postgres|psql' | grep -v grep || echo "    Not running as separate process"

echo ""
echo "  - Redis: "
ps aux | grep -E 'redis' | grep -v grep || echo "    Not running as separate process"

echo ""
echo "4. Project Structure Status:"
echo "  - Backend models: $(ls backend/app/models/*.py | wc -l) files"
echo "  - Frontend components: $(find frontend/src/components -name '*.jsx' -o -name '*.js' | wc -l) files"
echo "  - Test files: $(find backend/tests -name '*.py' | wc -l) files"

echo ""
echo "5. Git Status:"
echo "  Last Commit: $(git log -1 --oneline)"
echo "  Branch: $(git branch --show-current)"

echo ""
echo "=== Verification Complete ==="
