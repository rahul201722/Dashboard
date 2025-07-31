#!/bin/bash

# TV Shows Analysis Dashboard Launch Script

echo "🚀 Launching TV Shows Analysis Dashboard..."
echo "=================================="

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run this script from the Dashboard directory."
    exit 1
fi

# Check if requirements are installed
echo "📦 Checking dependencies..."
python -c "import streamlit, pandas, matplotlib, seaborn, plotly" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📋 Installing missing dependencies..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies. Please check the error messages above."
        exit 1
    fi
fi

echo "✅ Dependencies checked!"

# Test the data pipeline
echo "🔍 Testing data pipeline..."
python -c "
import sys
sys.path.append('.')
from utils.data_loader import get_data
from utils.data_processor import process_one_season_shows
try:
    basics, episodes = get_data()
    df = process_one_season_shows(basics, episodes)
    print(f'✅ Successfully loaded {len(df)} shows')
except Exception as e:
    print(f'❌ Error in data pipeline: {e}')
    sys.exit(1)
"

if [ $? -ne 0 ]; then
    echo "❌ Data pipeline test failed."
    exit 1
fi

echo "🎉 All systems ready!"
echo "📊 Starting Streamlit dashboard..."
echo "💡 The dashboard will open in your web browser automatically."
echo "🔗 URL: http://localhost:8501"
echo ""
echo "To stop the dashboard, press Ctrl+C"
echo ""

# Launch Streamlit
streamlit run app.py
