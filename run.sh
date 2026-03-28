#!/bin/bash
# Quick start script for AI Speaking Coach

echo "🗣️  Starting AI Speaking Coach..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
if [ "$OSTYPE" == "msys" ] || [ "$OSTYPE" == "win32" ]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install requirements
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Run the app
echo "🚀 Launching app..."
echo "📱 Open your browser at: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run main.py
