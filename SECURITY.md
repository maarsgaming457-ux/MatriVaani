# Security Policy

## Reporting Vulnerabilities
If you discover a security vulnerability or an accidentally exposed credential (API key, token, etc.), please report it immediately to the repository maintainers. Do not open a public issue for an exposed credential.

## Secret Handling Rules
- **Use Environment Variables:** All API keys, authorization tokens, and backend configurations must be managed via `.env` files locally or secret storage in your deployment provider.
- **No Hardcoded Keys:** Do not place API keys directly into Python scripts or Flutter Dart files.
- **Git Tracking:** The `.env` file is heavily restricted by `.gitignore`. If you need to document a new environment variable, place a safe placeholder in `.env.example`.

## Credential Rotation
If an API key is accidentally pushed to the repository, it must be rotated (invalidated and regenerated) at the source provider (e.g., Sarvam, Hugging Face, Groq) immediately. Modifying the Git history to remove the key is not sufficient protection against automated scrapers.
