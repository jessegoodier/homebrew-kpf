#!/bin/bash

# Homebrew Tap Initialization Script
# Run this script to set up the homebrew-kpf repository

set -e

echo "🍺 Initializing homebrew-kpf repository..."

# Check if we're in the right directory
if [ ! -f "Formula/kpf.rb" ]; then
    echo "❌ Error: Formula/kpf.rb not found. Are you in the homebrew-kpf directory?"
    exit 1
fi

echo "✅ Found Formula/kpf.rb"

# Initialize git repository if not already done
if [ ! -d ".git" ]; then
    echo "📝 Initializing git repository..."
    git init
    git branch -M main
else
    echo "✅ Git repository already initialized"
fi

# Set up git hooks if desired
if [ ! -f ".git/hooks/pre-commit" ]; then
    echo "🪝 Setting up git hooks..."
    cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Pre-commit hook to validate formula syntax

echo "Checking formula syntax..."
ruby -c Formula/kpf.rb

if [ $? -ne 0 ]; then
    echo "❌ Formula syntax check failed"
    exit 1
fi

echo "✅ Formula syntax check passed"
EOF
    chmod +x .git/hooks/pre-commit
else
    echo "✅ Git hooks already configured"
fi

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "⚠️  Homebrew not found. Install with:"
    echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
else
    echo "✅ Homebrew is installed"
fi

# Test formula syntax
echo "🧪 Testing formula syntax..."
ruby -c Formula/kpf.rb
echo "✅ Formula syntax is valid"

# Add all files
echo "📝 Adding files to git..."
git add .

# Initial commit if no commits exist
if ! git rev-parse HEAD &> /dev/null; then
    echo "💾 Creating initial commit..."
    git commit -m "Initial commit: Add kpf Homebrew formula

- Added kpf.rb formula for version $(grep -o 'kpf-[0-9]*\.[0-9]*\.[0-9]*' Formula/kpf.rb | sed 's/kpf-//')
- Added automated GitHub Actions workflows
- Added documentation and setup scripts

🍺 Generated Homebrew tap for kpf"
else
    echo "✅ Repository already has commits"
fi

# Check if remote is set up
if ! git remote | grep -q origin; then
    echo "🔗 Setting up remote..."
    echo "Please run: git remote add origin https://github.com/jessegoodier/homebrew-kpf.git"
    echo "Then: git push -u origin main"
else
    echo "✅ Remote origin already configured"
    
    # Ask if user wants to push
    read -p "📤 Push changes to remote? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git push
        echo "✅ Changes pushed to remote"
    fi
fi

echo ""
echo "🎉 Homebrew tap initialization complete!"
echo ""
echo "Next steps:"
echo "1. Ensure GitHub secrets are configured:"
echo "   - HOMEBREW_TAP_TOKEN in jessegoodier/kpf repository"
echo "2. Test the formula locally:"
echo "   brew tap jessegoodier/kpf"
echo "   brew install kpf"
echo "3. Check the workflows in GitHub Actions"
echo ""
echo "For more information, see SETUP.md"