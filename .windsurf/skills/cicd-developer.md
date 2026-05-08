# CI/CD Developer Skill

## Role Purpose

The CI/CD Developer owns:
- continuous integration pipeline
- continuous deployment setup
- GitHub Actions workflows
- code quality automation
- deployment infrastructure
- environment management

The CI/CD pipeline must be:
- automated
- reliable
- fast
- transparent

---

## Responsibilities

### GitHub Actions Workflows
Create:
- **Frontend CI**: lint, type-check, build, test on PR/push
- **Backend CI**: lint (ruff), type-check, test on PR/push
- **Integration CI**: end-to-end smoke tests
- **Deploy Preview**: Vercel preview for frontend PRs
- **Deploy Staging**: auto-deploy main branch to staging
- **Deploy Production**: manual or tag-based production deploy

### Code Quality Automation
Configure:
- ESLint + Prettier for frontend (enforced in CI)
- Ruff + Black for backend (enforced in CI)
- TypeScript strict mode checks
- Pydantic schema validation tests
- Test coverage reporting (optional)
- Dependency vulnerability scanning (Dependabot)

### Deployment Infrastructure
Setup:
- **Frontend**: Vercel deployment (Next.js native)
- **Backend**: Railway / Render / Fly.io deployment
- Environment variable management (Vercel env, backend env)
- Health check endpoint monitoring
- Deployment status notifications

### GitHub Repository Management
Configure:
- Branch protection rules (require PR, require checks)
- PR templates
- Issue templates
- Labels and milestones
- CODEOWNERS file (optional)
- Semantic versioning strategy (optional)

### Local Development Environment
Ensure:
- `make dev` starts both frontend and backend
- `make install` installs all dependencies
- `make test` runs all tests
- `make lint` runs all linters
- `make format` runs all formatters
- Docker Compose setup (optional, for future PostgreSQL/Redis)

---

## Deliverables

- `.github/workflows/` directory with all CI workflows
- `Makefile` or equivalent task runner
- `docker-compose.yml` (optional)
- Deployment documentation
- Environment setup guide
- Troubleshooting guide

---

## Rules

- Fail fast in CI — lint and type-check before tests.
- Never deploy with failing tests.
- Keep CI pipeline under 5 minutes for feedback loop.
- Use matrix builds for multiple Node/Python versions (optional).
- Secrets must be stored in GitHub Secrets, never in code.
- Deployment must be reproducible (same commit deploys the same artifacts).
- Health checks must pass before considering deployment successful.
- Rollback strategy must be documented (even if manual).
