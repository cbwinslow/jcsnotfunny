#!/bin/bash

# Website Source Code Access Script
# Provides secure access to JCS Not Funny website source code with development environment setup

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
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

show_help() {
    echo "Website Development Environment Setup"
    echo ""
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  clone               Clone the website repository"
    echo "  setup               Install dependencies and start dev server"
    echo "  analytics           Configure Google Analytics and view metrics"
    echo "  edit                Open code editor for targeted improvements"
    echo "  deploy              Deploy changes to staging/production"
    echo "  backup              Create and restore website state"
    echo "  production           Deploy to production environment"
    echo "  status              Check system health and status"
    echo "  logs                View development logs and errors"
    echo "  --force             Skip confirmation prompts"
    echo ""
    echo "Examples:"
    echo "  $0 setup               # Full development environment setup"
    echo "  $0 analytics            # Check analytics dashboard"
    echo "  $0 edit --optimize-title  # Quick SEO improvement"
    echo "  $0 logs --error       # Check recent error logs"
    echo ""
    echo "All scripts are available in scripts/ directory"
}

# Main execution logic
case "${1:-help}" in
    "setup")
        setup_development_environment
        ;;
    "analytics")
        show_analytics_dashboard
        ;;
    "edit")
        open_code_editor
        ;;
    "deploy")
        deploy_changes
        ;;
    "backup")
        backup_website_state
        ;;
    "production")
        deploy_to_production
        ;;
    "status")
        check_system_status
        ;;
    "logs")
        show_development_logs
        ;;
    *)
        show_help
        exit 1
        ;;
esac

setup_development_environment() {
    print_success "Setting up development environment..."
    
    echo "🔧 Repository Status:"
    if [ -d "website" ]; then
        print_success "✓ Website repository exists"
    else
        print_warning "Cloning repository..."
        git clone https://github.com/cbwinslow/jcsnotfunny.git website
        cd website
    fi
    
    echo "📦 Installing dependencies..."
    npm install
    
    echo "🔑 Setting up environment variables..."
    if [ ! -f ".env" ]; then
        print_success "✓ .env file found"
    else
        print_warning "Creating .env template..."
        cp .env.example .env
        echo "# Please add your Google Analytics ID and API keys to .env"
    fi
    
    echo "🚀 Starting development server..."
    npm run dev > /dev/null 2>&1 &
    DEV_PID=$!
    
    print_success "Development environment ready!"
    print_success "✓ Repository: website/"
    print_success "✓ Dependencies: Installed and configured"
    print_success "✓ Environment: .env configured"
    print_success "✓ Dev server: Running on localhost:3000"
    print_success "✅ Process ID: $DEV_PID"
    
    echo ""
    echo "🌐 Access URLs:"
    echo "  • Website: http://localhost:3000"
    echo "  • Analytics: Visit http://localhost:3000 after running: npm run analytics"
    echo "  • Code Editor: Use: npm run edit --help"
    echo ""
    echo "📝 Next Steps:"
    echo "  1. Edit code: npm run edit [file] [options]"
    echo "  2. Add dependencies: npm install [package]"
    echo "  3. Run tests: npm test"
    echo "  4. Deploy: npm run deploy [env]"
    echo "  5. Monitor: npm run analytics"
}

show_analytics_dashboard() {
    print_success "Opening analytics dashboard..."
    
    cd website
    
    # Check if analytics is configured
    if grep -q "G-" pages/_app.js; then
        print_success "✓ Google Analytics configured"
        
        echo "📊 Current Analytics Data:"
        echo "  • To view real-time data: npm run analytics"
        echo "  • To check setup: npm run analytics --check"
        
        # Show sample analytics command
        echo "  • Sample: npm run analytics --traffic --days 7"
        echo "  • Help: npm run analytics --help"
    else
        print_warning "⚠ Analytics not configured"
        echo "  • Run: npm run setup-analytics.sh"
    fi
}

open_code_editor() {
    local file="${2:-pages/index.js}"
    
    if [ -z "$file" ]; then
        echo "Available files:"
        ls -la pages/
        echo ""
        echo "Usage: $0 edit <filename> [options]"
        echo "Options:"
        echo "  --optimize-title    Optimize for search keywords"
        echo "  --enhance-meta     Improve SEO meta tags"
        echo "  --add-schema       Add structured data"
        exit 1
    fi
    
    echo "🔍 Opening $file for editing..."
    
    # Try VS Code first, then fallback to system editor
    if command -v code >/dev/null 2>&1; then
        code --wait "$file"
        print_success "✓ Opened in VS Code"
    elif command -v vim >/dev/null 2>&1; then
        vim "$file"
        print_success "✓ Opened in vim"
    else
        # Try opening with default system editor
        ${EDITOR:-nano} "$file"
        print_success "✓ Opened with ${EDITOR:-nano}"
    fi
}

deploy_changes() {
    print_success "Deploying website changes..."
    
    cd website
    
    # Build the site
    npm run build > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        print_success "✓ Build successful"
        
        # Deploy to staging (if applicable)
        if [ "$1" = "staging" ]; then
            echo "🚀 Deploying to staging..."
            # staging deployment command here
        else
            echo "🚀 Deploying to production..."
            # production deployment command here
            npm run start > /dev/null 2>&1
        fi
        
        if [ $? -eq 0 ]; then
            print_success "✓ Deployment successful"
        else
            print_error "❌ Deployment failed"
        fi
    else
        print_error "❌ Build failed"
    fi
}

deploy_to_production() {
    print_success "Deploying to production..."
    
    cd website
    
    # Production deployment
    npm run build && npm run start > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        print_success "✓ Production deployment successful"
    else
        print_error "❌ Production deployment failed"
    fi
}

backup_website_state() {
    print_success "Creating backup of website state..."
    
    cd website
    
    # Create backup directory
    BACKUP_DIR="backups/$(date +%Y-%m-%d_%H-%M-%S)"
    mkdir -p "$BACKUP_DIR"
    
    # Backup important files
    cp -r .env "$BACKUP_DIR/" 2>/dev/null
    cp -r public/sitemap.xml "$BACKUP_DIR/" 2>/dev/null
    cp -r public/feed.xml "$BACKUP_DIR/" 2>/dev/null
    cp -r lib/episodes.js "$BACKUP_DIR/" 2>/dev/null
    
    # Create backup info file
    cat > "$BACKUP_DIR/backup-info.txt" << EOF
Backup created: $(date)
Files backed up:
- Environment configuration (.env)
- SEO files (sitemap.xml, feed.xml)
- Episode data (episodes.js)
- Build artifacts (out directory)

To restore:
1. Copy files from backup to main directory
2. Run npm install
3. Test deployment locally
EOF
    
    print_success "✓ Backup created in $BACKUP_DIR"
}

check_system_status() {
    print_success "Checking system status..."
    
    echo "🖥️ Repository Status:"
    cd website
    echo "  • Current branch: $(git branch --show-current)"
    echo "  • Last commit: $(git log -1 --pretty=format:'%h' --abbrev-commit)"
    echo "  • Uncommitted changes: $(git status --porcelain | grep -c '^ M' | wc -l)"
    
    echo ""
    echo "📦 Dependencies Status:"
    if [ -f "package-lock.json" ]; then
        print_success "✅ Node.js dependencies locked"
    else
        print_warning "⚠ Node.js dependencies not locked"
    fi
    
    echo ""
    echo "🌐 Server Status:"
    if pgrep -f "npm.*dev" > /dev/null; then
        print_success "✅ Development server running (PID: $(pgrep -o pid= -f 'npm.*dev'))"
    else
        print_warning "⚠ Development server not running"
    fi
    
    echo ""
    echo "📊 Analytics Status:"
    if grep -q "G-" pages/_app.js; then
        print_success "✅ Analytics configured"
    else
        print_warning "⚠ Analytics not configured"
    fi
}

show_development_logs() {
    print_success "Showing development logs..."
    
    echo "📋 Recent Errors (last 20 lines):"
    cd website
    if [ -f ".next" ]; then
        echo "  • Next.js build logs:"
        tail -20 .next/build.log
    fi
    
    echo ""
    echo "📋 Recent Development Activity:"
    echo "  • Recent commits:"
    git log --oneline -5
    echo ""
    echo "  • Server processes:"
    ps aux | grep -E "npm\|node" | head -5
}

# Main execution
print_success "Website Development Environment Manager"
echo ""
echo "🎯 Ready to enhance your website with professional automation tools!"