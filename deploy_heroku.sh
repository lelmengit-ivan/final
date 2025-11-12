#!/bin/bash

echo "🚀 Deploying Pharmacy System to Heroku..."
echo "=========================================="
echo ""

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found!"
    echo "Please install from: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

echo "✅ Heroku CLI found"
echo ""

# Copy Heroku requirements
echo "📦 Preparing requirements..."
cp requirements-heroku.txt requirements.txt
echo "✅ Requirements updated"
echo ""

# Initialize git if needed
if [ ! -d .git ]; then
    echo "📁 Initializing git repository..."
    git init
    echo "✅ Git initialized"
    echo ""
fi

# Commit changes
echo "💾 Committing changes..."
git add .
git commit -m "Deploy to Heroku - $(date +%Y-%m-%d)"
echo "✅ Changes committed"
echo ""

# Check if Heroku app exists
echo "🔍 Checking Heroku app..."
if ! heroku apps:info > /dev/null 2>&1; then
    echo "📱 Creating new Heroku app..."
    heroku create
    echo "✅ Heroku app created"
else
    echo "✅ Heroku app exists"
fi
echo ""

# Add PostgreSQL if not exists
echo "🗄️  Checking PostgreSQL..."
if ! heroku addons | grep -q "heroku-postgresql"; then
    echo "Adding PostgreSQL database..."
    heroku addons:create heroku-postgresql:essential-0
    echo "✅ PostgreSQL added"
else
    echo "✅ PostgreSQL exists"
fi
echo ""

# Set SECRET_KEY if not set
echo "🔐 Checking SECRET_KEY..."
if [ -z "$(heroku config:get SECRET_KEY)" ]; then
    echo "Generating SECRET_KEY..."
    SECRET=$(python -c "import secrets; print(secrets.token_hex(32))")
    heroku config:set SECRET_KEY=$SECRET
    echo "✅ SECRET_KEY set"
else
    echo "✅ SECRET_KEY exists"
fi
echo ""

# Deploy
echo "🚀 Deploying to Heroku..."
git push heroku main
echo "✅ Deployment complete"
echo ""

# Run migration
echo "🔄 Running database migration..."
heroku run python migrate_to_multitenancy.py
echo "✅ Migration complete"
echo ""

# Show app info
echo "=========================================="
echo "🎉 DEPLOYMENT SUCCESSFUL!"
echo "=========================================="
echo ""
echo "📊 App Information:"
heroku info
echo ""
echo "🌐 Opening your app..."
heroku open
echo ""
echo "📝 View logs with: heroku logs --tail"
echo "🔧 Manage app at: https://dashboard.heroku.com"
echo ""
echo "✅ All done!"
