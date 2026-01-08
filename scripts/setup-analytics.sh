#!/bin/bash

# Google Analytics 4 Setup Script
# Sets up GA4 measurement ID and validates tracking

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

echo "🔧 Setting up Google Analytics 4..."
echo ""

# Check if API key manager exists
if [ ! -f "../scripts/api-key-manager.sh" ]; then
    print_error "API key manager not found. Please run from website directory."
    exit 1
fi

# Get GA4 measurement ID
echo "Please enter your Google Analytics 4 Measurement ID:"
echo "Get this from: https://analytics.google.com"
echo "Format: G-XXXXXXXXXX"
read -p "> " ga_id

if [ -z "$ga_id" ]; then
    print_error "GA4 ID is required"
    exit 1
fi

# Validate GA4 ID format
if [[ ! $ga_id =~ ^G-[A-Z0-9]{10}$ ]]; then
    print_error "Invalid GA4 ID format. Expected: G-XXXXXXXXXX"
    exit 1
fi

# Store GA4 ID securely
cd ..
./scripts/api-key-manager.sh store "GOOGLE_ANALYTICS_ID" "$ga_id" "Google Analytics 4 Measurement ID for jcsnotfunny.com"

print_success "GA4 ID stored securely"

# Update _app.js with real GA4 ID
echo "Updating _app.js with real GA4 ID..."
sed -i.bak "s/GA_MEASUREMENT_ID/$ga_id/g" website/pages/_app.js

if [ -f "website/pages/_app.js.bak" ]; then
    rm website/pages/_app.js.bak
fi

print_success "GA4 tracking configured in _app.js"

# Create validation script
cat > website/scripts/validate-ga4.sh << 'EOF'
#!/bin/bash
# Validates GA4 tracking is working

echo "🔍 Validating Google Analytics 4 tracking..."

# Check if GA4 ID is set
GA4_ID=$(grep -o "G-[A-Z0-9]\{10\}" website/pages/_app.js || echo "")

if [ -z "$GA4_ID" ]; then
    echo "❌ GA4 ID not found in _app.js"
    exit 1
fi

echo "✅ GA4 ID found: $GA4_ID"

# Test website build
cd website
npm run build > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Website builds successfully with GA4 tracking"
else
    echo "❌ Website build failed"
    exit 1
fi

echo "🌐 Next steps:"
echo "1. Start dev server: npm run dev"
echo "2. Visit: http://localhost:3000"
echo "3. Check browser console for gtag() calls"
echo "4. Verify in GA4: https://analytics.google.com"
EOF

chmod +x website/scripts/validate-ga4.sh

print_success "GA4 setup complete!"
echo ""
echo "📊 Expected Results:"
echo "- 100% visitor tracking accuracy"
echo "- Real-time traffic monitoring"
echo "- Conversion goal tracking"
echo "- Audience demographic data"
echo ""
echo "🧪 Run validation:"
echo "cd website && ./scripts/validate-ga4.sh"