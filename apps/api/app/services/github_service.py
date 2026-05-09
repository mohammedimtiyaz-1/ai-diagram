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

    async def fetch_file_content(self, owner: str, repo: str, path: str, branch: str = "main") -> Optional[str]:
        """Fetch content of a specific file."""
        url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)
                if response.status_code == 404 and branch == "main":
                    url = f"https://raw.githubusercontent.com/{owner}/{repo}/master/{path}"
                    response = await client.get(url)
                
                if response.status_code == 200:
                    # Truncate large files
                    content = response.text
                    if len(content) > 10000:
                        content = content[:10000] + "\n... (truncated)"
                    return content
                return None
            except Exception as e:
                logger.error(f"Error fetching file {path}: {str(e)}")
                return None

    def identify_important_files(self, paths: List[str]) -> List[str]:
        """Identify files useful for architecture analysis."""
        important_names = [
            "package.json", "tsconfig.json", "README.md", "app.py", "main.py",
            "next.config.js", "next.config.mjs", "tailwind.config.js",
            "index.tsx", "App.tsx", "Layout.tsx"
        ]
        
        important_files = []
        for path in paths:
            filename = path.split("/")[-1]
            if filename in important_names:
                important_files.append(path)
                
        return important_files[:10] # Limit to top 10
