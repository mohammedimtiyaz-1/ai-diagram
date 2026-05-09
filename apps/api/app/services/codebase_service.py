import json
from typing import List, Dict, Any, Optional
from uuid import uuid4
from app.services.github_service import GitHubService
from app.core.openai_client import openai_client
from app.prompts.codebase_prompt import CODEBASE_ANALYSIS_SYSTEM_PROMPT, CODEBASE_ANALYSIS_USER_TEMPLATE
from app.schemas.codebase import CodebaseAnalysisResponse
import logging

logger = logging.getLogger(__name__)

class CodebaseService:
    def __init__(self):
        self.github = GitHubService()

    async def analyze_repository(self, repo_url: str, diagram_type: str = "auto") -> CodebaseAnalysisResponse:
        """Coordinate the analysis of a GitHub repository."""
        logger.info(f"Analyzing repository: {repo_url}")
        
        # 1. Parse URL
        repo_info = self.github.parse_url(repo_url)
        if not repo_info:
            raise ValueError("Invalid GitHub URL")
        
        owner = repo_info["owner"]
        repo = repo_info["repo"]
        branch = repo_info["branch"]

        # 2. Fetch Tree
        tree_data = await self.github.fetch_tree(owner, repo, branch)
        raw_tree = tree_data.get("tree", [])
        clean_paths = self.github.filter_tree(raw_tree)
        
        # 3. Identify and Fetch Important Files
        important_paths = self.github.identify_important_files(clean_paths)
        file_contents = {}
        for path in important_paths:
            content = await self.github.fetch_file_content(owner, repo, path, branch)
            if content:
                file_contents[path] = content

        # 4. Prepare AI Context
        file_tree_str = "\n".join(clean_paths)
        file_contents_str = ""
        for path, content in file_contents.items():
            file_contents_str += f"\n--- {path} ---\n{content}\n"

        user_prompt = CODEBASE_ANALYSIS_USER_TEMPLATE.format(
            repo_name=f"{owner}/{repo}",
            file_tree=file_tree_str,
            file_contents=file_contents_str
        )

        # 5. Call AI for Analysis
        logger.info("Calling AI for codebase analysis...")
        ai_response = await openai_client.generate_json(
            system_prompt=CODEBASE_ANALYSIS_SYSTEM_PROMPT,
            user_prompt=user_prompt
        )

        # 6. Parse and Return
        analysis_id = str(uuid4())
        
        # Merge AI response with metadata
        result = CodebaseAnalysisResponse(
            analysis_id=analysis_id,
            repo_name=f"{owner}/{repo}",
            detected_stack=ai_response.get("detected_stack", []),
            important_files=important_paths,
            project_summary=ai_response.get("project_summary", "No summary available."),
            architecture_summary=ai_response.get("architecture_summary", "No architecture summary available."),
            recommended_diagram_type=ai_response.get("recommended_diagram_type", "architecture"),
            enhanced_prompt=ai_response.get("enhanced_prompt", f"Generate an architecture diagram for {owner}/{repo}"),
            warnings=ai_response.get("warnings", [])
        )
        
        return result

codebase_service = CodebaseService()
