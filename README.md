# LLM-Powered GitHub Project Automation

An LLM-powered Python application that turns a natural-language request into a GitHub project. The application generates a structured project specification, creates a GitHub Project v2, creates the related issues in the target repository, and links them to the project. It supports multiple LLM providers so you can choose the backend that works best for you.

## Features

- Generate a project specification from a user prompt.
- Create a GitHub Project v2 using the GitHub GraphQL API.
- Automatically create issues in a target GitHub repository.
- Link each created issue to the project.
- Choose between OpenAI, Anthropic Claude, or a local Ollama model.

## Prerequisites

- Python installed on your machine.
- A GitHub account with a valid personal access token.
- A target GitHub repository accessible with that token.
- API keys for OpenAI or Anthropic if you plan to use those providers.

**Your GitHub token must have permission to create issues and projects (Scopes : repo, project, read:org, write:discussion)**

## Installation

1. Clone the repository.
2. Go to the project root.
3. Run the `create_env.sh` script to generate the `.env` file:

```bash
bash create_env.sh
```

4. Open the generated `.env` file at the project root and replace the placeholder values with your real credentials.
5. Install the Python dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

The `create_env.sh` script creates a `.env` file with the following variables:

- `GITHUB_TOKEN`: your GitHub personal access token.
- `OWNER`: the GitHub username or organization that owns the target repository.
- `GRAPHQL_ENDPOINT`: GitHub GraphQL endpoint.
- `OPENAI_API_KEY`: OpenAI API key, if you use OpenAI.
- `ANTHROPIC_API_KEY`: Anthropic API key, if you use Claude.

The application also reads a system prompt from `src/prompts/system_prompt.json`.

## Usage

Run the application from the `src` directory:

```bash
cd src
python main.py
```

When prompted, provide:

- the repository name, either as `owner/repo` or just `repo` if `OWNER` is set in `.env`;
- a description of the project you want to create.

### LLM provider selection

By default, the local model is used. You can explicitly choose a provider with one of these options:

```bash
python main.py --local
python main.py --openai
python main.py --claude
```

For the local provider, make sure you have **Ollama installed** and you have downloaded the required model (`qwen2.5-coder:14b`).

You can install Ollama by running:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

and then download the model with:

```bash
ollama pull qwen2.5-coder:14b
```

## Workflow

The main flow is:

1. Read the user request.
2. Generate a structured project specification with the LLM.
3. Create the GitHub Project.
4. Create the issues described in the specification.
5. Link each issue to the project.

## Example

Example prompt:

```text
Create an e-commerce project with product management, a shopping cart, online payment, and a customer account area.
```

The application will generate the corresponding GitHub project and repository issues.

## Troubleshooting

- Make sure the `.env` file exists at the project root.
- Check that `GITHUB_TOKEN` and `OWNER` are set correctly.
- Make sure the target repository exists and is accessible with your token.
- If you use OpenAI or Claude, verify the corresponding API key is present.

## License

See the `LICENSE` file.
