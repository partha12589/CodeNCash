#!/bin/bash

echo "?? Starting CodeNCash Backend API..."
echo ""

# Check if in correct directory
if [ ! -f "backend/api/routes.py" ]; then
    echo "? Error: Please run this script from the project root directory"
    exit 1
fi

# Install dependencies if needed
if [ "$1" == "--install" ]; then
    echo "?? Installing dependencies..."
    pip install -r requirements-backend.txt
    echo ""
fi

# Run FastAPI server
echo "? Launching API Server..."
echo "?? URL: http://localhost:8000"
echo "?? Docs: http://localhost:8000/docs"
echo ""

cd backend
python3 -m uvicorn api.routes:app --reload --port 8000
