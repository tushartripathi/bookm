#!/bin/bash

# AI Alignment Forum News Scraper - Startup Script

echo "🚀 Starting AI Alignment Forum News Scraper..."
echo "📁 Activating virtual environment..."

# Activate virtual environment
source venv/bin/activate

echo "🔧 Installing/updating dependencies..."
pip install -r requirements.txt

echo "🌐 Starting Flask server on port 5001..."
echo "📱 Frontend: http://localhost:5001"
echo "🔌 API: http://localhost:5001/api/scrape"
echo "💚 Health: http://localhost:5001/api/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Flask application
python app.py
