#!/bin/bash

# NZ Electricity Chatbot - Run Script
echo "🔌 Starting NZ Electricity Chatbot..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Navigate to src directory and run Streamlit
echo "🚀 Starting Streamlit app..."
cd src
streamlit run app.py --server.address=0.0.0.0 --server.port=8501

echo "✅ App should be running at http://localhost:8501"