#!/usr/bin/env bash

cat > .env <<'EOF'
# This .env file contains environment variables for the Github Project AI Agent application.

# Replace the placeholders with your actual GitHub token and username.
GITHUB_TOKEN=your_github_token
OWNER=your_github_username

# The GraphQL endpoint for GitHub's API.
GRAPHQL_ENDPOINT=https://api.github.com/graphql

# LLM Provider
# OpenAI
OPENAI_API_KEY=your_openai_api_key

# Claude (Anthropic)
ANTHROPIC_API_KEY=your_anthropic_api_key
EOF
