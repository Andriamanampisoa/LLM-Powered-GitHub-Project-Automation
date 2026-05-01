## 
## Filename: Github-Project-AI-Agent/src/utils/agent.py
## Created Date: Thursday, April 1th 2026, 5:13:51 pm
## Author: Toa
## Description: Agent logic for the Github Project AI Agent application, defining the workflow for planning
##              and executing GitHub project creation based on user requests.
##

from utils.tools import create_full_github_project
from langgraph.graph import StateGraph, END
from models.schemas import ProjectSpec
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

def planner_node(state: dict, llm: dict, system_prompt: str) -> dict:
    """
    Plan the next steps for the GitHub project creation.
    """
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    structured_llm = llm.with_structured_output(ProjectSpec)
    response = structured_llm.invoke(messages)

    return {
        "messages": state["messages"] + [AIMessage(content=response.model_dump_json(indent=2))],
        "project_spec": response
    }

def executor_node(state: dict, config: dict, repo: str) -> dict:
    """
    Execute the creation of the GitHub project based on the planned specification.
    """
    spec: ProjectSpec = state["project_spec"]
    result = create_full_github_project.func(spec, config, repo)

    return {
        "messages": state["messages"] + [AIMessage(content=result)],
        "final_result": result
    }

def create_agent(llm: dict, config: dict, repo: str, system_prompt: str) -> StateGraph:
    workflow = StateGraph(dict)

    def planner(state):
        return planner_node(state, llm, system_prompt)

    workflow.add_node("planner", planner)
    workflow.add_node("executor", lambda state: executor_node(state, config, repo))
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "executor")
    workflow.add_edge("executor", END)
    return workflow.compile()
