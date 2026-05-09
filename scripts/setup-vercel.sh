#!/bin/bash
# Setup Vercel project and extract IDs for GitHub Actions secrets
# Run this after installing Vercel CLI: npm install -g vercel

set -e

PROJECT_NAME="ai-design-system-diagram"

echo "=== Vercel Project Setup ==="
echo ""
echo "Prerequisites:"
echo "  1. Vercel CLI installed: npm install -g vercel"
echo "  2. Logged in: vercel login"
echo "  3. You are in the repo root directory"
echo ""
read -p "Press Enter to continue or Ctrl+C to cancel..."

# Link/create project
echo ""
echo "Linking Vercel project (apps/web)..."
cd apps/web
vercel link --yes --project "$PROJECT_NAME" || vercel --yes --name "$PROJECT_NAME"

# Extract IDs from .vercel/project.json
echo ""
echo "Extracting Vercel IDs..."
ORG_ID=$(cat .vercel/project.json | grep -o '"orgId"[^,]*' | cut -d'"' -f4)
PROJECT_ID=$(cat .vercel/project.json | grep -o '"projectId"[^,]*' | cut -d'"' -f4)

echo ""
echo "=== Extracted Values ==="
echo "VERCEL_ORG_ID=$ORG_ID"
echo "VERCEL_PROJECT_ID=$PROJECT_ID"

echo ""
echo "=== Next Steps ==="
echo "1. Get your Vercel token:"
echo "   https://vercel.com/account/tokens"
echo ""
echo "2. Add these GitHub Secrets at:"
echo "   https://github.com/YOUR_USER/YOUR_REPO/settings/secrets/actions"
echo ""
echo "   Name: VERCEL_TOKEN"
echo "   Value: <your-token>"
echo ""
echo "   Name: VERCEL_ORG_ID"
echo "   Value: $ORG_ID"
echo ""
echo "   Name: VERCEL_PROJECT_ID"
echo "   Value: $PROJECT_ID"
echo ""
echo "3. Set environment variable in Vercel dashboard:"
echo "   NEXT_PUBLIC_API_BASE_URL=https://your-backend-url.onrender.com"
echo ""
