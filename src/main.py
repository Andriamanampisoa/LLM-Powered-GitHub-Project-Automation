## 
## Filename: Github-Project-AI-Agent/src/main.py
## Created Date: Thursday, April 30th 2026, 7:58:23 pm
## Author: Toa
## Description: Main entry point for the Github Project AI Agent application.
## 

from langchain.messages import HumanMessage
from utils.parser import parse_args, parse_system_prompt, define_provider
from utils.tools import load_llm
from utils.agent import create_agent
from dotenv import dotenv_values

def main():
    """
    Main entry point for the Github Project AI Agent application.
    """
    parser = parse_args()
    config = dotenv_values("../.env")
    system_prompt = parse_system_prompt()
    repoName = input("Enter the repository name (e.g., user/repo): ") \
                or "your_github_username/your_repository_name"
    user_request = input("Describe the project you want to create: ") \
                or "Create a GitHub project for a new e-commerce website with features like product management, shopping cart, online payment, and customer accounts."

    if not config.get("GITHUB_TOKEN") or not config.get("OWNER"):
        print("Please set GITHUB_TOKEN and OWNER in the .env file.")
        return
    if not system_prompt:
        print("System prompt is empty. Please check the system_prompt.json file.")
        return

    provider = define_provider(parser)
    llm = load_llm(provider)
    agent = create_agent(llm, config, repoName, system_prompt)
    initial_state = {"messages": [HumanMessage(content=user_request)]}

    print("\n" + "="*80)
    print(f"\nRequest: {user_request}")
    print(f"\nSelected LLM Provider: {provider}\n")
    print("Processing your request...\n")
    result = agent.invoke(initial_state)
    print("\n" + "="*80)
    print(result.get("final_result", "Aucun résultat"))

if __name__ == "__main__":
    main()
