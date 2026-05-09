# Render Setup Steps (Manual)

These steps must be done via the Render web dashboard. There is no CLI equivalent.

## Step 1: Create Web Service

1. Go to https://dashboard.render.com
2. Click **New +** → **Web Service**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `ai-diagram-api`
   - **Root Directory**: `apps/api`
   - **Runtime**: `Docker`
   - **Branch**: `main`
   - **Dockerfile Path**: `Dockerfile` (default)

## Step 2: Add Environment Variables

In the service dashboard → **Environment** tab, add:

| Key | Value |
|-----|-------|
| `APP_ENV` | `production` |
| `CORS_ORIGINS` | `https://your-frontend.vercel.app` |
| `OPENAI_API_KEY` | `sk-...your-key...` |
| `ENHANCE_TIMEOUT_SECONDS` | `30` |
| `REFINE_TIMEOUT_SECONDS` | `45` |
| `ANALYZE_TIMEOUT_SECONDS` | `60` |
| `ENHANCE_RATE_LIMIT` | `10` |
| `REFINE_RATE_LIMIT` | `8` |
| `ANALYZE_RATE_LIMIT` | `5` |

> Replace `CORS_ORIGINS` with your actual Vercel frontend URL after deployment.

## Step 3: Get Deploy Hook URL

1. In the service dashboard → **Settings** tab
2. Scroll to **Deploy Hook**
3. Click **Create Deploy Hook**
4. Name it: `github-actions-deploy`
5. Copy the URL (looks like: `https://api.render.com/deploy/srv-xxx...`)
6. Add it as GitHub Secret: `RENDER_DEPLOY_HOOK_URL`

## Step 4: Deploy

Click **Manual Deploy** → **Deploy latest commit** to verify it builds.

After successful deploy:
- Copy the service URL (e.g., `https://ai-diagram-api.onrender.com`)
- Use this as `NEXT_PUBLIC_API_BASE_URL` in Vercel dashboard
