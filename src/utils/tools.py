## 
## Filename: Github-Project-AI-Agent/src/utils/tools.py
## Created Date: Thursday, April 30th 2026, 8:21:12 pm
## Author: Toa
## Description: Utility functions for the Github Project AI Agent application.
## 

import os

from models.schemas import ProjectSpec
from utils.graphql_query import get_owner_id, create_project, add_issue_to_project
from github import Github
from typing import Dict, Any
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_ollama import ChatOllama
from tqdm import tqdm


def resolve_repo_full_name(owner: str, repo_input: str) -> str:
    """
    Resolve repository input into a full GitHub repository name (owner/repo).
    Accepts either "repo" or "owner/repo".
    """
    owner = (owner or "").strip()
    repo_input = (repo_input or "").strip()

    if not repo_input:
        raise ValueError("Repository name is empty.")

    if "/" in repo_input:
        return repo_input

    if not owner:
        raise ValueError("OWNER is empty while repository is provided without owner.")

    return f"{owner}/{repo_input}"

@tool
def create_full_github_project(spec: ProjectSpec, config: Dict[str, Any], repo: str) -> str:
    """
    Create a full GitHub project based on the provided specification and configuration.
    This includes creating the project, adding columns, and creating issues for each ticket.
    """
    try:
        print("Creating project structure...")
        owner_id = get_owner_id(config.get('OWNER'), config)
        project_result = create_project(spec.project_name, spec.description, owner_id, config)
        project_id = project_result["id"]
        project_url = project_result["url"]
        print(f"Project created: {project_url}")

        g = Github(config.get('GITHUB_TOKEN'))
        full_repo_name = resolve_repo_full_name(config.get('OWNER'), repo)
        repo_obj = g.get_repo(full_repo_name)
        added_count = 0

        print(f"\nCreating {len(spec.tickets)} issues...")
        for ticket in tqdm(spec.tickets, desc="Issues", unit="issue"):
            issue = repo_obj.create_issue(
                title=ticket.title,
                body=ticket.body,
                labels=ticket.labels
            )
            add_issue_to_project(issue.node_id, project_id, config)
            added_count += 1
        return f"Project created: {project_url} with {added_count} issues added."

    except Exception as e:
        return f"Error during project creation: {str(e)}"

def load_llm(provider: str) -> Dict[str, tool]:
    """
    Load the appropriate language model based on the configuration.
    Supports OpenAI, Anthropic Claude, and local models via Ollama.
    """
    if provider == "openai":
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY is missing in the .env file")
        return ChatOpenAI(
            model="gpt-4o",
            temperature=0.1
        )
    elif provider == "claude":
        if not os.getenv("ANTHROPIC_API_KEY"):
            raise ValueError("ANTHROPIC_API_KEY is missing in the .env file")
        return ChatAnthropic(
            model="claude-3-5-sonnet-20240620",
            temperature=0.1,
            max_tokens=8192
        )
    elif provider == "local":
        return ChatOllama(
            model="qwen2.5-coder:14b",
            temperature=0.1,
            # num_ctx=32768,
        )
    else:
        raise ValueError("Invalid provider specified. Choose from 'openai', 'claude', or 'local'.")
