#!/bin/bash
# Helper to set GitHub secrets using gh CLI
# Install: https://cli.github.com/

set -e

REPO=$(git remote get-url origin | sed 's/.*github.com[:/]//' | sed 's/\.git$//')

echo "=== GitHub Secrets Setup ==="
echo "Target repo: $REPO"
echo ""

echo "You need these values ready:"
echo "  1. VERCEL_TOKEN       (from https://vercel.com/account/tokens)"
echo "  2. VERCEL_ORG_ID      (from scripts/setup-vercel.sh output)"
echo "  3. VERCEL_PROJECT_ID  (from scripts/setup-vercel.sh output)"
echo "  4. RENDER_DEPLOY_HOOK (from Render dashboard → Settings → Deploy Hook)"
echo ""

read -p "VERCEL_TOKEN: " VERCEL_TOKEN
read -p "VERCEL_ORG_ID: " VERCEL_ORG_ID
read -p "VERCEL_PROJECT_ID: " VERCEL_PROJECT_ID
read -p "RENDER_DEPLOY_HOOK_URL: " RENDER_HOOK

echo ""
echo "Setting secrets on $REPO..."

echo "$VERCEL_TOKEN" | gh secret set VERCEL_TOKEN --repo="$REPO" --body="$VERCEL_TOKEN"
echo "$VERCEL_ORG_ID" | gh secret set VERCEL_ORG_ID --repo="$REPO" --body="$VERCEL_ORG_ID"
echo "$VERCEL_PROJECT_ID" | gh secret set VERCEL_PROJECT_ID --repo="$REPO" --body="$VERCEL_PROJECT_ID"
echo "$RENDER_HOOK" | gh secret set RENDER_DEPLOY_HOOK_URL --repo="$REPO" --body="$RENDER_HOOK"

echo ""
echo "=== Secrets set successfully ==="
echo "Verify at: https://github.com/$REPO/settings/secrets/actions"
