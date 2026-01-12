#!/bin/bash
# Quick start script for Thanos Threat Modeling Platform

set -e

echo "🔱 Thanos Threat Modeling Platform - Quick Start"
echo "================================================"
echo ""

# Check if we're in the right directory
if [ ! -f "src/schema.py" ]; then
    echo "❌ Error: Please run this script from the root of the thanos repository"
    exit 1
fi

# Navigate to src directory
cd src

# Initialize database
echo "📦 Initializing database..."
if ! python3 -c "from schema import init_db; init_db()" 2>&1; then
    echo ""
    echo "❌ Failed to initialize database (see error above)"
    exit 1
fi

# Load default data
echo "📥 Loading default component types and controls..."
python3 load_data.py -f data/default.yaml > /dev/null 2>&1 || {
    echo "⚠️  Warning: Could not load default data"
}

# Load comprehensive controls and threats
echo "📥 Loading STRIDE threat categories and controls..."
python3 load_data.py -f data/init/controls.yaml > /dev/null 2>&1 || {
    echo "⚠️  Warning: Could not load control data"
}

# Load example threat model
echo "📥 Loading example e-commerce threat model..."
python3 load_data.py -f data/examples/ecommerce_platform.tm.yaml > /dev/null 2>&1 || {
    echo "⚠️  Warning: Could not load example threat model"
}

# Load customer call recordings example if exists
if [ -f "data/customer_call_recordings_workflow.tm.yaml" ]; then
    echo "📥 Loading customer call recordings example..."
    python3 load_data.py -f data/customer_call_recordings_workflow.tm.yaml > /dev/null 2>&1 || {
        echo "⚠️  Warning: Could not load customer recordings example"
    }
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Starting Thanos web interface..."
echo "   Access the application at: http://localhost:8501"
echo ""
echo "   Press Ctrl+C to stop the server"
echo ""

# Start Streamlit
streamlit run streamlit_app/app.py
