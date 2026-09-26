# MatriVaani GitHub Workflow

## Overview
GitHub is the **Source of Truth** for the MatriVaani project. All codebase changes, documentation, tests, and configuration files must be version-controlled through Git and stored in this repository.

## The Separation of Code and Data
Because MatriVaani involves large machine learning models and extensive audio datasets, we strictly enforce a separation of concerns:

- **GitHub Stores:**
  - Source code (`ai/`, `scripts/`, `training/`, `data_modules/`)
  - Tests (`tests/`)
  - Documentation (`docs/`)
  - Configurations (`requirements.txt`, `.gitignore`)
  - Evaluation reports (`evaluation/`)

- **External Storage (DO NOT COMMIT):**
  - **Datasets** (Hugging Face `ai4bharat/IndicVoices`, local caches) -> Excluded via `.gitignore`.
  - **Model Checkpoints** (`models/`, `*.safetensors`, `*.pt`) -> Excluded via `.gitignore`.
  - **Audio Files** (`*.wav`, `*.flac`) -> Excluded via `.gitignore`.

## Standard Workflow

1. **Local Development**
   - Write code, scripts, or documentation in `C:\study files\sih project`.
   - Test locally using `pytest`.

2. **Git Commit**
   - `git add .`
   - `git status` (Verify no large binaries or `.env` files are accidentally staged).
   - `git commit -m "Your descriptive message"`

3. **Git Push**
   - `git push origin main`

4. **GPU Training (Google Colab / Cloud)**
   - Clone the GitHub repository onto the GPU instance:
     `git clone https://github.com/<username>/MatriVaani.git`
   - Install requirements: `pip install -r requirements.txt`
   - Authenticate with Hugging Face: `huggingface-cli login`
   - Run the training script on the GPU instance.
   
5. **Model Artifact Storage**
   - After GPU training completes, export the final `.safetensors` model weights.
   - Upload the weights to Google Drive or a private Hugging Face Model Hub. Do **not** push them back to GitHub.

6. **Local/Android Testing**
   - Download the trained weights to the local machine (`models/` folder).
   - Run inference/integration tests locally.
