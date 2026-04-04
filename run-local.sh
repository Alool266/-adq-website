#!/bin/bash

# Start ADQ Admin Panel locally

echo "🚀 Starting ADQ Backend on port 8001..."
rm -f adq.db
cd backend
pip install -r requirements.txt -q
DATABASE_URL=sqlite:///../adq.db python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 &

sleep 3

echo ""
echo "✅ Backend running at http://localhost:8001"
echo "✅ Create admin at http://localhost:8001/setup"
echo ""
echo "Now in another terminal, run:"
echo "  cd frontend && npm install && REACT_APP_API_URL=http://localhost:8001/api/v1 npm start"
echo ""
echo "Login: admin / admin123"