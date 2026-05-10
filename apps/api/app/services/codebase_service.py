import asyncio
import json
import logging
from uuid import uuid4

import httpx

from app.core.config import settings
from app.core.openai_client import OpenAIClient
from app.core.errors import AiTimeoutError
from app.prompts.codebase_prompt import (
    CODEBASE_ANALYSIS_SYSTEM_PROMPT,
    CODEBASE_ANALYSIS_USER_TEMPLATE,
)
from app.schemas.codebase import CodebaseAnalysisResponse
from app.services.github_service import GitHubService

logger = logging.getLogger(__name__)

# Hard caps to keep analysis fast and within token budget.
_MAX_TREE_PATHS = 600
_TOTAL_CONTENT_BUDGET_CHARS = 45_000


class CodebaseService:
    def __init__(self):
        self.github = GitHubService()

    async def analyze_repository(
        self, repo_url: str, diagram_type: str = "auto"
    ) -> CodebaseAnalysisResponse:
        """Evidence-based GitHub repo analysis using a powerful model.

        Speed optimisations:
        - Parallel file content fetches with a shared httpx client.
        - Tighter file-content budget so we stay well below model context.
        - File tree truncated to most relevant prefix.
        """
        logger.info(f"Analyzing repository: {repo_url}")

        repo_info = self.github.parse_url(repo_url)
        if not repo_info:
            raise ValueError("Invalid GitHub URL")
        owner, repo, branch = repo_info["owner"], repo_info["repo"], repo_info["branch"]

        # 1. Tree
        tree_data = await self.github.fetch_tree(owner, repo, branch)
        raw_tree = tree_data.get("tree", [])
        clean_paths = self.github.filter_tree(raw_tree)
        truncated_paths = clean_paths[:_MAX_TREE_PATHS]

        # 2. Important files (scored)
        important_paths = self.github.identify_important_files(truncated_paths)

        # 3. Parallel content fetch
        file_contents: dict[str, str] = {}
        async with httpx.AsyncClient() as http_client:
            results = await asyncio.gather(
                *(
                    self.github.fetch_file_content(owner, repo, p, branch, client=http_client)
                    for p in important_paths
                ),
                return_exceptions=True,
            )
        for path, content in zip(important_paths, results):
            if isinstance(content, Exception):
                logger.warning(f"Skipping {path}: {content}")
                continue
            if content:
                file_contents[path] = content

        # 4. Build AI context within total char budget
        file_tree_str = "\n".join(truncated_paths)
        contents_buf: list[str] = []
        used = 0
        for path, content in file_contents.items():
            block = f"\n--- {path} ---\n{content}\n"
            if used + len(block) > _TOTAL_CONTENT_BUDGET_CHARS:
                contents_buf.append(f"\n--- {path} ---\n... (skipped to fit budget)\n")
                continue
            contents_buf.append(block)
            used += len(block)
        file_contents_str = "".join(contents_buf)

        user_prompt = CODEBASE_ANALYSIS_USER_TEMPLATE.format(
            repo_name=f"{owner}/{repo}",
            file_tree=file_tree_str,
            file_contents=file_contents_str,
        )

        # 5. Powerful model for analysis
        logger.info(
            "Calling AI for codebase analysis (model=%s, files=%d, content_chars=%d)",
            settings.analyze_model, len(file_contents), used,
        )
        client = OpenAIClient.get_async()

        try:
            response = await asyncio.wait_for(
                client.chat.completions.create(
                    model=settings.analyze_model,
                    messages=[
                        {"role": "system", "content": CODEBASE_ANALYSIS_SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt},
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.2,
                    max_tokens=2000,
                ),
                timeout=settings.analyze_timeout_seconds,
            )
            ai_content = response.choices[0].message.content
            if not ai_content:
                raise ValueError("AI returned empty analysis")
            ai_response = json.loads(ai_content)
        except asyncio.TimeoutError:
            logger.error(f"Codebase analysis timed out after {settings.analyze_timeout_seconds}s")
            raise AiTimeoutError(
                f"Codebase analysis timed out after {settings.analyze_timeout_seconds}s. "
                "Repository may be too large; try a smaller branch or sub-path."
            )
        except Exception as e:
            logger.error(f"Codebase analysis AI call failed: {e}")
            ai_response = {}

        analysis_id = str(uuid4())
        return CodebaseAnalysisResponse(
            analysis_id=analysis_id,
            repo_name=f"{owner}/{repo}",
            detected_stack=ai_response.get("detected_stack", []),
            important_files=important_paths,
            project_summary=ai_response.get("project_summary", "No summary available."),
            architecture_summary=ai_response.get(
                "architecture_summary", "No architecture summary available."
            ),
            recommended_diagram_type=ai_response.get(
                "recommended_diagram_type", "flowchart"
            ),
            enhanced_prompt=ai_response.get(
                "enhanced_prompt",
                f"Generate an architecture diagram for {owner}/{repo}",
            ),
            warnings=ai_response.get("warnings", []),
        )


codebase_service = CodebaseService()
