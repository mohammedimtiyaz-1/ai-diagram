import httpx
import re
from typing import List, Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)

class GitHubService:
    def __init__(self):
        self.base_url = "https://api.github.com"
        # We use a public API client. For better rate limits, one would add a GITHUB_TOKEN.
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "AI-Design-System-Diagram-Assistant"
        }

    def parse_url(self, url: str) -> Optional[Dict[str, str]]:
        """Extract owner and repo from a GitHub URL."""
        pattern = r"github\.com/([^/]+)/([^/]+)(?:/tree/([^/]+))?"
        match = re.search(pattern, url)
        if match:
            repo = match.group(2)
            # Remove .git if present
            if repo.endswith(".git"):
                repo = repo[:-4]
            return {
                "owner": match.group(1),
                "repo": repo,
                "branch": match.group(3) or "main" # Default to main if not in URL
            }
        return None

    async def fetch_tree(self, owner: str, repo: str, branch: str = "main") -> Dict[str, Any]:
        """Fetch the recursive file tree from a GitHub repository."""
        # First, we need to get the SHA of the branch if not provided
        # For simplicity, we try /git/trees/{branch}?recursive=1
        url = f"{self.base_url}/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers)
                if response.status_code == 404 and branch == "main":
                    # Try master if main fails
                    url = f"{self.base_url}/repos/{owner}/{repo}/git/trees/master?recursive=1"
                    response = await client.get(url, headers=self.headers)
                
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"GitHub API error: {e.response.status_code} - {e.response.text}")
                raise Exception(f"GitHub API returned {e.response.status_code}")
            except Exception as e:
                logger.error(f"Error fetching tree: {str(e)}")
                raise

    def filter_tree(self, tree: List[Dict[str, Any]], max_depth: int = 5) -> List[str]:
        """Filter out noise and return a clean list of paths."""
        ignored_patterns = [
            r"node_modules/", r"\.git/", r"dist/", r"build/", 
            r"\.next/", r"__pycache__/", r"\.pyc$", 
            r"\.png$", r"\.jpg$", r"\.jpeg$", r"\.gif$", r"\.svg$", r"\.ico$",
            r"package-lock\.json$", r"yarn\.lock$", r"pnpm-lock\.yaml$",
            r"\.DS_Store", r"vendor/"
        ]
        
        clean_paths = []
        for item in tree:
            path = item.get("path", "")
            if item.get("type") == "blob":
                # Check depth
                if path.count("/") >= max_depth:
                    continue
                
                # Check ignored patterns
                if any(re.search(p, path) for p in ignored_patterns):
                    continue
                    
                clean_paths.append(path)
                
        return clean_paths[:1000] # Limit to 1000 paths to avoid token overflow

    async def fetch_file_content(
        self,
        owner: str,
        repo: str,
        path: str,
        branch: str = "main",
        client: Optional[httpx.AsyncClient] = None,
        max_chars: int = 5000,
    ) -> Optional[str]:
        """Fetch content of a specific file. Uses a shared client when provided."""
        url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"

        async def _do(c: httpx.AsyncClient) -> Optional[str]:
            try:
                response = await c.get(url, timeout=8.0)
                if response.status_code == 404 and branch == "main":
                    fallback = f"https://raw.githubusercontent.com/{owner}/{repo}/master/{path}"
                    response = await c.get(fallback, timeout=8.0)
                if response.status_code == 200:
                    content = response.text
                    if len(content) > max_chars:
                        content = content[:max_chars] + "\n... (truncated)"
                    return content
                return None
            except Exception as e:
                logger.warning(f"Error fetching file {path}: {e}")
                return None

        if client is not None:
            return await _do(client)
        async with httpx.AsyncClient() as c:
            return await _do(c)

    # ── Important file selection ─────────────────────────────────────────────
    # Names checked anywhere in the tree (filename match).
    _IMPORTANT_FILENAMES = {
        # Manifests
        "package.json", "pnpm-workspace.yaml", "turbo.json", "nx.json", "lerna.json",
        "pyproject.toml", "requirements.txt", "setup.py", "setup.cfg", "Pipfile",
        "go.mod", "Cargo.toml", "composer.json", "Gemfile", "pom.xml", "build.gradle",
        # Configs
        "tsconfig.json", "next.config.js", "next.config.mjs", "next.config.ts",
        "vite.config.ts", "vite.config.js", "webpack.config.js",
        "tailwind.config.js", "tailwind.config.ts", "postcss.config.js",
        "nuxt.config.ts", "svelte.config.js", "remix.config.js",
        # Backend frameworks
        "app.py", "main.py", "manage.py", "wsgi.py", "asgi.py", "server.ts", "server.js",
        # Infra
        "Dockerfile", "docker-compose.yml", "docker-compose.yaml",
        "render.yaml", "vercel.json", "netlify.toml", "fly.toml", "railway.json",
        "Procfile", "serverless.yml",
        # Docs
        "README.md", "ARCHITECTURE.md",
    }

    # Path prefixes whose direct children are interesting (entry points, routes).
    _IMPORTANT_PATH_HINTS = (
        "src/index.", "src/main.", "src/app.", "src/server.",
        "app/layout.", "app/page.", "app/main.",
        "apps/", "packages/", "services/", "internal/", "cmd/",
        ".github/workflows/", "prisma/schema.prisma", "schema.prisma",
    )

    def identify_important_files(self, paths: List[str], limit: int = 18) -> List[str]:
        """Pick architecture-relevant files for AI analysis.

        Prioritises root-level manifests and entry points first, then path-hint matches.
        """
        scored: List[tuple[int, str]] = []
        for path in paths:
            filename = path.split("/")[-1]
            # Higher score = more important (sorted descending)
            score = 0
            depth = path.count("/")
            if filename in self._IMPORTANT_FILENAMES:
                score += 100 - depth  # prefer shallower
            for hint in self._IMPORTANT_PATH_HINTS:
                if path.startswith(hint) or hint in path:
                    score += 30 - depth
                    break
            if score > 0:
                scored.append((score, path))

        scored.sort(key=lambda t: t[0], reverse=True)
        seen = set()
        result: List[str] = []
        for _, path in scored:
            if path in seen:
                continue
            seen.add(path)
            result.append(path)
            if len(result) >= limit:
                break
        return result
