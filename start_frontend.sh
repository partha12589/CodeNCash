#!/bin/bash

echo "?? Starting CodeNCash Frontend..."
echo ""

# Check if in correct directory
if [ ! -f "frontend/codencash_app.py" ]; then
    echo "? Error: Please run this script from the project root directory"
    exit 1
fi

# Install dependencies if needed
if [ "$1" == "--install" ]; then
    echo "?? Installing dependencies..."
    pip install -r requirements-frontend.txt
    echo ""
fi

# Run Streamlit app
echo "? Launching CodeNCash..."
echo "?? URL: http://localhost:8501"
echo ""

cd frontend
streamlit run codencash_app.py --server.port=8501
