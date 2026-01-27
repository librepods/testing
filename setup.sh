#!/bin/bash

# CloudSync API Setup Script
# Configures development environment and validates credentials

set -e

echo "🚀 CloudSync API Setup"
echo "====================="
echo ""

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not installed. Please install Node.js first."
    exit 1
fi

echo "✓ Node.js $(node --version)"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
npm install --silent 2>/dev/null || npm install
echo "✓ Dependencies installed"
echo ""

# Setup environment
if [ ! -f .env ]; then
    echo "📝 Creating environment configuration..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
else
    echo "✓ .env file exists"
    echo ""
fi

# Credential validation
echo "🔐 Checking credentials..."
echo ""

if [ -f .env ]; then
    source .env 2>/dev/null || true
    
    if [ -z "$CLOUD_CREDENTIALS" ] || [ -z "$API_KEY" ]; then
        echo "⚠️  Setup incomplete: Missing required credentials"
        echo ""
        echo "This application requires valid cloud provider credentials to function."
        echo "Please configure the following in your .env file:"
        echo ""
        echo "  1. CLOUD_CREDENTIALS - Your cloud provider credentials"
        echo "  2. API_KEY - Your API key for enhanced features"
        echo ""
        echo "To obtain credentials:"
        echo "  • Google Cloud: https://console.cloud.google.com/apis/credentials"
        echo "  • AWS: https://console.aws.amazon.com/iam/"
        echo "  • Azure: https://portal.azure.com/"
        echo ""
        echo "After obtaining your credentials, add them to the .env file and run setup again."
        echo ""
        exit 1
    fi
    
    echo "✓ Credentials configured"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Run 'npm test' to verify your installation"
echo ""

