## 
## Filename: Github-Project-AI-Agent/src/utils/graphql_query.py
## Created Date: Thursday, April 30th 2026, 9:15:52 pm
## Author: Toa
## Description: Utility functions for the Github Project AI Agent application.
## 

import requests

from typing import Dict, Any

def graphql_query(query: str, variables: dict = None, config: Dict[str, Any] = None) -> dict:
    """
    Execute a GraphQL query against the GitHub API with the provided query, variables, and configuration.
    """
    headers = {
        "Authorization": f"Bearer {config.get('GITHUB_TOKEN')}",
        "Content-Type": "application/json"
    }
    response = requests.post(
        config.get('GRAPHQL_ENDPOINT'),
        json={"query": query, "variables": variables or {}},
        headers=headers
    )
    result = response.json()

    if "errors" in result:
        raise Exception(f"GraphQL Error: {result['errors']}")
    return result["data"]

def get_owner_id(login: str, config: Dict[str, Any]) -> str:
    """
    Retrieve the ID of a GitHub user or organization based on their login.
    """
    user_query = """
        query($login: String!) {
          user(login: $login) {
            id
          }
        }
    """
    organization_query = """
        query($login: String!) {
          organization(login: $login) {
            id
          }
        }
    """

    try:
        user_data = graphql_query(user_query, {"login": login}, config)
        user = user_data.get("user") if user_data else None
        if user and user.get("id"):
            return user["id"]
    except Exception:
        pass

    try:
        org_data = graphql_query(organization_query, {"login": login}, config)
        org = org_data.get("organization") if org_data else None
        if org and org.get("id"):
            return org["id"]
    except Exception:
        pass

    raise Exception(
        f"Owner '{login}' not found. Set OWNER to a valid GitHub user or organization login."
    )

def create_project(name: str, description: str, owner_id: str, config: Dict[str, Any]) -> dict:
    """
    Create a GitHub Project v2 with the given name and owner ID.

    Note: GitHub's CreateProjectV2Input does not accept a description field.
    """
    create_project_mutation = """
        mutation($input: CreateProjectV2Input!) {
          createProjectV2(input: $input) {
            projectV2 {
              id
              url
            }
          }
        }
        """
    project_input = {
        "ownerId": owner_id,
        "title": name,
    }
    project_result = graphql_query(create_project_mutation, {"input": project_input}, config)
    return project_result["createProjectV2"]["projectV2"]

def add_issue_to_project(issue_node_id: str, project_id: str, config: Dict[str, Any]) -> dict:
    """
    Add an existing issue to a GitHub Project v2 using the issue's node ID and the project's ID.
    """
    add_item_mutation = """
        mutation($input: AddProjectV2ItemByIdInput!) {
          addProjectV2ItemById(input: $input) {
            item { id }
          }
        }
        """
    add_result = graphql_query(add_item_mutation, {
        "input": {
            "projectId": project_id,
            "contentId": issue_node_id
        }
    }, config)
    return add_result["addProjectV2ItemById"]["item"]
