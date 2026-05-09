# Deployment Guide

This document covers how to build, test, and deploy the AI Design System Diagram Assistant.

---

## Deployment Targets

| Component | Platform | URL Pattern |
|-----------|----------|-------------|
| Frontend | Vercel | `https://<project>.vercel.app` |
| Backend | Render | `https://<service>.onrender.com` |

---

## Required Secrets & Variables

### GitHub Secrets

Configure these in **Settings → Secrets and variables → Actions**:

| Secret | Description |
|--------|-------------|
| `VERCEL_TOKEN` | Vercel personal access token |
| `VERCEL_ORG_ID` | Vercel organization ID |
| `VERCEL_PROJECT_ID` | Vercel project ID |
| `RENDER_DEPLOY_HOOK_URL` | Render deploy hook URL (found in Render dashboard) |

### Vercel Project Environment Variables

Configure in **Vercel Dashboard → Project → Settings → Environment Variables**:

| Variable | Value Example | Environment |
|----------|---------------|-----------|
| `NEXT_PUBLIC_API_BASE_URL` | `https://your-backend.onrender.com` | Production |

### Render Environment Variables

Configure in **Render Dashboard → Service → Environment**:

| Variable | Required | Example |
|----------|----------|---------|
| `APP_ENV` | Yes | `production` |
| `CORS_ORIGINS` | Yes | `https://your-frontend.vercel.app` |
| `OPENAI_API_KEY` | Yes | `sk-...` |
| `ENHANCE_TIMEOUT_SECONDS` | Yes | `30` |
| `REFINE_TIMEOUT_SECONDS` | Yes | `45` |
| `ANALYZE_TIMEOUT_SECONDS` | Yes | `60` |
| `ENHANCE_RATE_LIMIT` | Yes | `10` |
| `REFINE_RATE_LIMIT` | Yes | `8` |
| `ANALYZE_RATE_LIMIT` | Yes | `5` |

> **Important:** Do not use `*` for `CORS_ORIGINS` in production. List your exact Vercel domain.

---

## Deployment Order

1. **Deploy backend first**
   - Create a new Web Service on Render
   - Connect your GitHub repo
   - Set root directory to `apps/api`
   - Choose "Docker" as runtime
   - Add all environment variables above
   - Copy the deploy hook URL into GitHub secrets

2. **Copy backend production URL**
   - After first deploy, Render gives you a URL like `https://ai-diagram-api.onrender.com`
   - Save this for the frontend env var

3. **Set frontend env var in Vercel**
   - `NEXT_PUBLIC_API_BASE_URL=https://your-backend.onrender.com`

4. **Deploy frontend**
   - Push to `main` or trigger the `deploy-frontend.yml` workflow manually

5. **Test integration**
   - Open the deployed frontend
   - Verify `/health` on the backend returns `{"status":"ok"}`
   - Send a test prompt and confirm the diagram generates

---

## CI/CD Workflows

### `ci.yml`

Runs on every push to `main` and every pull request.

- **frontend-ci**: installs deps → lint → type-check → build
- **backend-ci**: installs deps → ruff lint → pytest

### `deploy-frontend.yml`

Runs on pushes to `main` that touch `apps/web/**`.

- Pulls Vercel env → builds → deploys production
- Can also be triggered manually via `workflow_dispatch`

### `deploy-backend.yml`

Runs on pushes to `main` that touch `apps/api/**`.

- Runs backend CI (lint + tests)
- Only deploys if CI passes
- Calls Render deploy hook to trigger a new build

---

## Manual Deployment

### Frontend (Vercel CLI)

```bash
cd apps/web
npm install --global vercel
vercel --prod
```

### Backend (Render Deploy Hook)

```bash
curl -X POST "$RENDER_DEPLOY_HOOK_URL"
```

---

## Health Check

Test the backend health endpoint after deployment:

```bash
curl https://<your-backend>.onrender.com/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "ai-design-system-diagram-assistant-api"
}
```

---

## Troubleshooting

### CORS Errors

- Verify `CORS_ORIGINS` on Render matches your exact Vercel domain
- Do not include trailing slashes
- Include `http://localhost:3000` only for local dev

### Frontend Build Fails

- Check `NEXT_PUBLIC_API_BASE_URL` is set in Vercel
- Ensure `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID` are correct

### Backend Won't Start

- Check Render logs for missing env vars
- Verify `OPENAI_API_KEY` is set and valid
- Confirm Dockerfile is using correct path (`apps/api`)

### Rate Limit Hit

- If you see 429 errors during testing, wait 60 seconds and retry
- Limits: Enhance 10/min, Refine 8/min, Analyze 5/min
