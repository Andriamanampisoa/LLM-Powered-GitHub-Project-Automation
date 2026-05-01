## 
## Filename: Github-Project-AI-Agent/src/utils/parser.py
## Created Date: Thursday, April 30th 2026, 11:08:42 pm
## Author: Toa
## Description: Parser functions for the Github Project AI Agent application.
## 

import argparse
import json

from dotenv import parser

def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments for the Github Project AI Agent application.
    """
    parser = argparse.ArgumentParser(description="GitHub Project AI Agent")
    parser.add_argument("-o", "--openai", action="store_true", help="Use OpenAI's API")
    parser.add_argument("-c", "--claude", action="store_true", help="Use Anthropic's Claude API")
    parser.add_argument("-l", "--local", action="store_true", help="Use a local LLM (default)")
    return parser.parse_args()

def parse_system_prompt() -> str:
    """
    Parse the system prompt from a JSON file.
    """
    try:
        with open("prompts/system_prompt.json", "r") as f:
            data = json.load(f)
        return data.get("system_prompt", "")
    except FileNotFoundError:
        print("Error: System prompt file not found.")
        return ""
    except json.JSONDecodeError:
        print("Error: Invalid JSON in system prompt file.")
        return ""

def define_provider(args: argparse.Namespace) -> str:
    """
    Define the LLM provider based on the parsed command-line arguments.
    """
    if args.openai:
        return "openai"
    elif args.claude:
        return "claude"
    elif args.local:
        return "local"
    else:
        return "local"

