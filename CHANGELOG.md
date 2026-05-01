# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-05-01

### Added
- Initial stable release of the GitHub Project AI Agent.
- AI-driven generation of a structured project specification from a natural-language request.
- GitHub Project v2 creation through the GitHub GraphQL API.
- Automatic creation of repository issues from the generated project specification.
- Automatic linking of created issues to the project.
- Support for OpenAI, Anthropic Claude, and local Ollama models.
- Command-line provider selection for `--local`, `--openai`, and `--claude`.
- Progress display while issues are being created.
- Environment bootstrap script `create_env.sh` for generating the `.env` file.

### Changed
- Established the first versioned release of the project.

### Notes
- This is the first stable release of the project.
- Make sure the `.env` file is configured before running the application.
