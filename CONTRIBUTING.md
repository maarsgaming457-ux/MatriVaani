# Contributing to MatriVaani

We welcome contributions! Please follow these guidelines when submitting patches, features, or bug fixes.

## Branch Naming
- Features: `feature/<feature-name>`
- Bug Fixes: `fix/<bug-name>`
- Documentation: `docs/<name>`

## Pull Requests
1. Clone the repository and run `git lfs pull` to download the models.
2. Create your feature branch.
3. Commit your changes with descriptive messages.
4. Push to your branch and open a Pull Request against `main` or the integration branch.

## Commit Style
Use conventional commit prefixes: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`.

## ⚠️ Model Modification Restrictions
Do NOT modify, overwrite, or retrain the production model files (`backend/best_model_main2/` or `models/santhali_asr_final_5k/`) without explicit authorization. These represent the finalized, validated weights for the SIH submission.

## Secret Handling
**NEVER COMMIT SECRETS.**
- Never commit `.env` files.
- Never hardcode API keys (Sarvam, Groq, Bhashini) into the Python or Dart source code.
- Always load secrets dynamically using `os.getenv` or Flutter's environment definitions.

## Large Files & Git LFS
Never add large model checkpoints (`.pt`, `.safetensors`, `.bin`) as regular Git blobs. If you must add a new model, ensure it is tracked by Git LFS (`git lfs track "*.safetensors"`) before committing.
